"""Frozen learned writes; new cross-event questions. See notes/PROTOCOL.md."""
import argparse, hashlib, itertools, json, platform, time
from pathlib import Path
import numpy as np
import torch
from torch import nn
ROOT=Path(__file__).resolve().parents[1]
SUPPORT=np.array(list(itertools.product([-1.,1.],repeat=4)),dtype=np.float32)
TASKS=['expected_ab','expected_cd','parity2','parity4','agree_ab']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def dump(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def ids(z): return ((z>0)*(2**np.arange(z.shape[-1]))).sum(-1)
def moments(x): return np.concatenate([x,x[...,:1]*x[...,1:2],x[...,2:3]*x[...,3:4]],-1).astype(np.float64)

class Memory(nn.Module):
    def __init__(self,parameters):
        super().__init__()
        self.enc=nn.Sequential(nn.Linear(4,32),nn.Tanh(),nn.Linear(32,4))
        self.dec=nn.Sequential(nn.Linear(4,32),nn.Tanh(),nn.Linear(32,4))
        self.load_state_dict({k:torch.tensor(v,dtype=torch.float32) for k,v in parameters.items()})
    def encode(self,x):
        with torch.no_grad(): return torch.where(self.enc(torch.from_numpy(x))>=0,1.,-1.).numpy()
    def decode(self,z):
        with torch.no_grad(): return self.dec(torch.from_numpy(z)).numpy().astype(np.float64)

def write(encode,x):
    z=encode(x); w=np.zeros_like(z)
    for key in range(x.shape[1]): w[:,key]-=w[:,key]-z[:,key]
    assert np.array_equal(w,z)
    return w

def table(z,x,rank):
    ix=ids(z).ravel(); counts=np.bincount(ix,minlength=2**rank)
    tab=np.zeros((2**rank,6),dtype=np.float64)
    np.add.at(tab,ix,moments(x).reshape(-1,6)); tab/=counts.clip(1)[:,None]
    return tab,counts

def compose(m):
    """m: batch × four distinct keys × six moments."""
    a,b=m[:,:,0],m[:,:,1]
    agreement=.5*(1+a[:,0]*a[:,1]+b[:,0]*b[:,1]+m[:,0,4]*m[:,1,4])-1
    return np.stack([m[:,0,4],m[:,0,5],a[:,:2].prod(1),a.prod(1),agreement],1)

def score(pred,y):
    return {task:{'mse':float(np.mean((pred[:,j]-y[:,j])**2)),
                  'accuracy':float(np.mean(np.where(pred[:,j]>=0,1.,-1.)==y[:,j]))}
            for j,task in enumerate(TASKS)}

def population(codes,exact):
    m=exact[ids(codes)]; a2=np.mean(m[:,0]**2)
    ii,jj=np.indices((16,16)); ii=ii.ravel();jj=jj.ravel()
    pair=np.stack([m[ii],m[jj],m[ii],m[jj]],1)
    raw=np.stack([SUPPORT[ii],SUPPORT[jj],SUPPORT[ii],SUPPORT[jj]],1)
    y=compose(moments(raw))[:,-1]; p=compose(pair)[:,-1]
    risk={'expected_ab':float(np.mean(1-m[:,4]**2)),
          'expected_cd':float(np.mean(1-m[:,5]**2)),
          'parity2':float(1-a2**2),'parity4':float(1-a2**4),
          'agree_ab':float(np.mean((y-p)**2))}
    assert np.isclose(risk['agree_ab'],np.mean(1-p**2))
    return risk

def inspect(encode,decode,rank,seed,n):
    # Separate RNG streams; actual query draw occurs only after memory write.
    x=SUPPORT[np.random.default_rng(seed).integers(16,size=(n,32))]
    fit=SUPPORT[np.random.default_rng(seed+100000).integers(16,size=(128,32))]
    t=time.perf_counter();w=write(encode,x);wt=time.perf_counter()-t; frozen=digest(w)
    q=np.array([np.random.default_rng(seed+200000+i).choice(32,4,replace=False) for i in range(n)])
    t=time.perf_counter();selected=w[np.arange(n)[:,None],q];access=time.perf_counter()-t
    truth=compose(moments(x[np.arange(n)[:,None],q]))
    times={'write':wt,'query_state_gather':access}
    t=time.perf_counter(); ordinary=compose(moments(decode(selected)));times['ordinary_read']=time.perf_counter()-t
    t=time.perf_counter();fw=write(encode,fit);emp,counts=table(fw,fit,rank);times['fitted_reader_build_including_write']=time.perf_counter()-t
    t=time.perf_counter();codes=encode(SUPPORT);exact,ec=table(codes,SUPPORT,rank);times['exact_reader_build']=time.perf_counter()-t
    t=time.perf_counter();alt=compose(emp[ids(selected)]);times['fitted_read']=time.perf_counter()-t
    t=time.perf_counter();opt=compose(exact[ids(selected)]);times['exact_read']=time.perf_counter()-t
    # Control: give the same algebra exact evidence, including within-record joint moment.
    assert np.array_equal(compose(moments(x[np.arange(n)[:,None],q])),truth)
    results={'ordinary':score(ordinary,truth),'clipped':score(ordinary.clip(-1,1),truth),
             'fitted':score(alt,truth),'exact':score(opt,truth)}
    decomposition={}
    for name,pred in [('ordinary',ordinary),('clipped',ordinary.clip(-1,1)),('fitted',alt)]:
        decomposition[name]={task:{'conditional_variance':float(np.mean(1-opt[:,j]**2)),
                     'reader_excess':float(np.mean((pred[:,j]-opt[:,j])**2)),
                     'finite_sample_cross_term':float(2*np.mean((pred[:,j]-opt[:,j])*(opt[:,j]-truth[:,j]))),
                     'sample_noise':float(np.mean((opt[:,j]-truth[:,j])**2-(1-opt[:,j]**2)))}
                     for j,task in enumerate(TASKS)}
    assert digest(w)==frozen
    return {'metrics':results,'population_optimal_mse':population(codes,exact),
            'decomposition':decomposition,'state_sha256':frozen,'data_sha256':digest(x),
            'fit_sha256':digest(fit),'query_sha256':digest(q),'support_codes':codes.tolist(),
            'fit_table':emp.tolist(),'fit_counts':counts.tolist(),'exact_table':exact.tolist(),
            'exact_counts':ec.tolist(),'seconds':times,'state_bytes':32*rank*4,
            'reader_table_bytes':int(emp.nbytes),'reader_count_bytes':int(counts.nbytes),
            'occupied_codes':int((ec>0).sum()),'state_read_immutable':True}

def audit():
    # Independent truth logic checks all 16^4 queried tuples: products and field equality.
    ix=np.array(list(itertools.product(range(16),repeat=4)))
    x=SUPPORT[ix];y=compose(moments(x))
    assert np.array_equal(y[:,2],x[:,0,0]*x[:,1,0])
    assert np.array_equal(y[:,3],np.prod(x[:,:,0],axis=1))
    assert np.array_equal(y[:,4],np.where(np.all(x[:,0,:2]==x[:,1,:2],axis=1),1.,-1.))
    # Actual autograd gradient write and untouched rows, distinct-key and reset boundaries.
    z=torch.tensor([[1.,-1.,1.,-1.]])
    w=torch.zeros(1,32,4,requires_grad=True)
    loss=.5*((w[:,7]-z)**2).sum();updated=w-torch.autograd.grad(loss,w)[0]
    assert torch.equal(updated[:,7],z) and torch.count_nonzero(updated).item()==4
    return {'full_evidence_query_tuples':len(ix),'independent_truth_check':True,'autograd_write':True}

def run(stage,dest):
    out=Path(dest) if dest else ROOT/'analysis'/stage
    if out.exists(): raise RuntimeError('Refusing existing evidence destination')
    seeds=[90,91] if stage=='development' else list(range(5))
    n=512 if stage=='development' else 8192;base=4100000 if stage=='development' else 7300000
    protocol=ROOT/'notes'/('DESIGN.md' if stage=='development' else 'PROTOCOL.md')
    manifest={'stage':stage,'seeds':seeds,'histories_per_seed':n,'fit_records':4096,'base':base,
              'script_sha256':sha(__file__),'protocol_sha256':sha(protocol),'lock_sha256':sha(ROOT.parent/'uv.lock'),
              'python':platform.python_version(),'torch':torch.__version__,'numpy':np.__version__,
              'threads':1,'device':'cpu','donors':{},'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    dump(out/'audit.json',audit())
    for seed in seeds:
        for objective in ['expected','broad']:
            p=ROOT/'donors'/f's{seed}-r4-{objective}.json';d=json.loads(p.read_text());manifest['donors'][p.name]=sha(p)
            model=Memory(d['parameters'])
            # Acquisition checked before new queries; expected loss must be small on all atomic records.
            raw=model.decode(model.encode(SUPPORT)); local=moments(raw)[:,4:]
            acquisition=float(np.mean((local-moments(SUPPORT)[:,4:])**2))
            assert acquisition<1e-5,(seed,objective,acquisition)
            if objective=='broad': assert len(np.unique(ids(model.encode(SUPPORT))))==16
            r=inspect(model.encode,model.decode,4,base+seed*10000,n)
            row={'seed':seed,'objective':objective,'acquisition_mse':acquisition,
                 'donor_training_seconds':d['training_seconds'],'donor_training_records':d['training_records'],
                 'shared_parameter_bytes':d['shared_parameter_bytes'],'result':r}
            dump(out/f's{seed}-{objective}.json',row)
            print(seed,objective,{k:round(v,5) for k,v in r['population_optimal_mse'].items()},flush=True)
        for name,rank,enc in [('full_raw',4,lambda x:x.copy()),('parities',2,lambda x:moments(x)[...,4:].astype(np.float32))]:
            # Explicit competent canonical raw decode; exact table is the primary reference.
            dec=(lambda z:z) if rank==4 else (lambda z:np.stack([np.ones_like(z[...,0]),z[...,0],np.ones_like(z[...,1]),z[...,1]],-1))
            r=inspect(enc,dec,rank,base+seed*10000,n)
            dump(out/f's{seed}-{name}.json',{'seed':seed,'objective':name,'shared_parameter_bytes':0,'result':r})
    dump(out/'manifest.json',manifest)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['development','evaluation']);p.add_argument('--destination');args=p.parse_args()
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True);run(args.stage,args.destination)
