"""Finite nonlinear memory. See ../notes/DESIGN.md; no original-study imports."""
import argparse
import hashlib
import itertools
import json
import platform
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = torch.tensor(list(itertools.product([-1., 1.], repeat=4)))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(x):
    return hashlib.sha256(x.detach().numpy().tobytes()).hexdigest()


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')


def data(n, seed):
    g = torch.Generator().manual_seed(seed)
    return SUPPORT[torch.randint(16, (n, 8), generator=g)]


def targets(x):
    return torch.cat((x[..., :1] * x[..., 1:2], x[..., 2:3] * x[..., 3:4], x), -1)


def metrics(pred, y):
    e = (pred.double() - y.double()).square().reshape(-1, 6).mean(0)
    return dict(expected=e[:2].mean().item(), changed=e[2:].mean().item(), fields=e.tolist())


class Memory(nn.Module):
    def __init__(self, rank):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(4, 32), nn.Tanh(), nn.Linear(32, rank))
        self.dec = nn.Sequential(nn.Linear(rank, 32), nn.Tanh(), nn.Linear(32, 4))

    def encode(self, x):
        smooth = self.enc(x).tanh()
        hard = torch.where(smooth >= 0, 1., -1.)
        return hard + (smooth - smooth.detach())

    def read(self, z):
        return targets(self.dec(z))


def write(z):
    """Unit SGD on 1/2 ||W[key]-z||², fixed orthogonal keys."""
    w = torch.zeros_like(z)
    for k in range(8):
        w[:, k] = w[:, k] - (w[:, k] - z[:, k])
    return w


def ids(z):
    return (((z > 0).long()) * (2 ** torch.arange(z.shape[-1]))).sum(-1)


def lookup(z, y, rank):
    flat, labels = ids(z).reshape(-1), y.reshape(-1, 6).double()
    counts = torch.bincount(flat, minlength=2**rank)
    table = torch.zeros(2**rank, 6, dtype=torch.float64)
    table.index_add_(0, flat, labels)
    table /= counts.clamp_min(1)[:, None]
    return table, counts


@torch.no_grad()
def inspect(encode, read, rank, fit, test):
    t = time.perf_counter(); w = write(encode(test)); write_seconds = time.perf_counter() - t
    frozen = w.clone()
    t = time.perf_counter(); pred = read(w); read_seconds = time.perf_counter() - t
    t = time.perf_counter(); fitw = write(encode(fit))
    table, counts = lookup(fitw, targets(fit), rank); fit_seconds = time.perf_counter() - t
    codes = encode(SUPPORT)
    exact, exact_counts = lookup(codes, targets(SUPPORT), rank)
    code_ids = ids(codes)
    assert torch.equal(w, frozen)
    assert torch.all((w == 1) | (w == -1))
    return {'ordinary': metrics(pred, targets(test)),
            'empirical_reader': metrics(table[ids(w)], targets(test)),
            'optimal_reader': metrics(exact[ids(w)], targets(test)),
            'population_ordinary': metrics(read(codes), targets(SUPPORT)),
            'population_optimal': metrics(exact[code_ids], targets(SUPPORT)),
            'support_codes': codes.tolist(), 'support_outputs': read(codes).tolist(),
            'partition': [[i for i, c in enumerate(code_ids.tolist()) if c == j]
                          for j in range(2**rank)],
            'empirical_table': table.tolist(), 'fit_counts': counts.tolist(),
            'optimal_table': exact.tolist(), 'support_counts': exact_counts.tolist(),
            'state_sha256': digest(w), 'state_bytes_per_history': w[0].numel()*4,
            'semantic_bits_per_history': 8*rank, 'occupied_codes': int((exact_counts > 0).sum()),
            'read_preserves_state': True,
            'seconds': {'write': write_seconds, 'ordinary_read': read_seconds, 'reader_fit_including_write': fit_seconds}}


def train(rank, objective, seed, steps):
    torch.manual_seed(seed)
    model = Memory(rank)
    optimizer = torch.optim.Adam(model.parameters(), lr=.01)
    gen = torch.Generator().manual_seed(10000+seed)
    curve = []
    t = time.perf_counter()
    for step in range(steps):
        x = SUPPORT[torch.randint(16, (128,), generator=gen)]
        pred, y = model.read(model.encode(x)), targets(x)
        loss = ((pred[..., :2]-y[..., :2])**2).mean() if objective == 'expected' else ((pred[..., 2:]-x)**2).mean()
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        assert torch.isfinite(loss)
        if step == 0 or (step+1) % 100 == 0:
            with torch.no_grad():
                curve.append({'step':step+1, 'loss':loss.item(),
                              **metrics(model.read(model.encode(SUPPORT)),targets(SUPPORT))})
    return model, curve, time.perf_counter()-t


def controls():
    def parity(x): return targets(x)[..., :2]
    def canonical(z): return targets(torch.stack((torch.ones_like(z[...,0]), z[...,0], torch.ones_like(z[...,0]), z[...,1]),-1))
    def balanced_read(z): return targets(torch.stack((z[...,0], torch.zeros_like(z[...,0]), z[...,1], torch.zeros_like(z[...,0])),-1))
    def hybrid_read(z): return targets(torch.stack((torch.ones_like(z[...,0]),z[...,0],z[...,1],torch.zeros_like(z[...,0])),-1))
    def invertible(x): return torch.stack((x[...,0]*x[...,1],x[...,0],x[...,2]*x[...,3],x[...,2]),-1)
    return [('parities',2,parity,canonical),
            ('balanced_raw',2,lambda x:x[..., [0,2]],balanced_read),
            ('hybrid',2,lambda x:torch.stack((x[...,0]*x[...,1],x[...,2]),-1),hybrid_read),
            ('full_raw',4,lambda x:x,targets),
            ('invertible_nonlinear_canonical',4,invertible,lambda z:canonical(z[..., [0,2]]))]


def audit():
    torch.manual_seed(77)
    model = Memory(2)
    x = data(3, 909)
    z = model.encode(x)
    w = write(z)
    assert torch.equal(w, z)
    g1 = torch.autograd.grad(model.read(w).square().sum(), tuple(model.parameters()), retain_graph=True)
    g2 = torch.autograd.grad(model.read(z).square().sum(), tuple(model.parameters()))
    assert all(torch.allclose(a,b) for a,b in zip(g1,g2))
    prev = torch.randn(3,8,2,requires_grad=True)
    loss = .5 * (prev[:,3]-z.detach()[:,3]).square().sum()
    actual = prev-torch.autograd.grad(loss,prev)[0]
    assert torch.allclose(actual[:,3], z.detach()[:,3], atol=2e-7)
    assert torch.equal(actual[:,[0,1,2,4,5,6,7]],prev[:,[0,1,2,4,5,6,7]])
    for name,r,enc,read in controls():
        result = inspect(enc,read,r,data(512,999),data(128,998))
        if name == 'parities':
            assert result['population_optimal']['expected'] == 0
            assert result['population_optimal']['changed'] == 1
        if name == 'full_raw' or name == 'invertible_nonlinear_canonical':
            assert result['population_optimal']['changed'] == 0
    return {'sequential_matches_direct': True, 'outer_gradients_match': True,
            'autograd_inner_update_matches': True, 'overwrite_other_rows_unchanged': True,
            'analytic_control_checks': True, 'script_sha256': sha(__file__)}


def run(stage, destination=None):
    folder = Path(destination) if destination else ROOT/'analysis'/stage
    if folder.exists(): raise RuntimeError('Refusing to overwrite existing evidence directory')
    seeds = [90,91] if stage == 'development' else list(range(5))
    base = 1900000 if stage == 'development' else 1700000
    steps = 2000
    manifest = {'stage':stage,'seeds':seeds,'ranks':[2,4],'steps':steps,'batch_records':128,
                'lr':.01,'optimizer':'Adam defaults','fit_histories':512,
                'test_histories':256 if stage=='development' else 4096,'base':base,
                'script_sha256':sha(__file__),'lock_sha256':sha(ROOT.parent/'uv.lock'),
                'protocol_sha256':sha(ROOT/'notes'/('DESIGN.md' if stage=='development' else 'PROTOCOL.md')),
                'torch':torch.__version__,'numpy':np.__version__,'python':platform.python_version(),
                'threads':1,'device':'cpu','dtype':'float32','diagnostic_dtype':'float64',
                'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    dump(folder/'manifest.json',manifest); dump(folder/'audit.json',audit())
    for seed in seeds:
        fit, test = data(512,base+100+seed),data(manifest['test_histories'],base+seed)
        for rank in [2,4]:
            for objective in ['expected','broad']:
                model,curve,seconds=train(rank,objective,seed,steps)
                result=inspect(model.encode,model.read,rank,fit,test)
                row={'seed':seed,'rank':rank,'objective':objective,'curve':curve,
                     'training_seconds':seconds,'training_records':steps*128,
                     'shared_parameter_bytes':sum(p.numel()*p.element_size() for p in model.parameters()),
                     'parameters':{k:v.tolist() for k,v in model.state_dict().items()},
                     'fit_sha256':digest(fit),'test_sha256':digest(test),'result':result}
                name=f's{seed}-r{rank}-{objective}'
                dump(folder/(name+'.json'),row)
                print(name,json.dumps({k:result[k] for k in ['ordinary','population_optimal']}),flush=True)
        rows={name:inspect(enc,read,r,fit,test) for name,r,enc,read in controls()}
        dump(folder/f's{seed}-controls.json',rows)


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['development','evaluation'])
    parser.add_argument('--destination');args=parser.parse_args()
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
    run(args.stage,args.destination)
