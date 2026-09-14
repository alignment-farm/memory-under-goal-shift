"""Linear TTT under a changed field query; see notes/DESIGN.md and PROTOCOL.md."""
import argparse, hashlib, json, platform, time
from pathlib import Path
import numpy as np
import torch
R=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(x.detach().cpu().numpy().tobytes()).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def data(n,rho,seed):
 g=torch.Generator().manual_seed(seed)
 z=torch.randn(n,8,8,generator=g)
 return torch.cat([z[...,:4],rho*z[...,:4]+(1-rho*rho)**.5*z[...,4:]],-1)
def covariance(rho):
 c=torch.eye(8,dtype=torch.float64);c[:4,4:]=rho*torch.eye(4);c[4:,:4]=rho*torch.eye(4);return c

def write(x,e,order=None):
 """Closed gradient of 1/2 squared loss, actual sequential state updates."""
 w=torch.zeros(x.shape[0],8,e.shape[1],dtype=x.dtype)
 for i in (range(8) if order is None else order):
  k=torch.eye(8,dtype=x.dtype)[i]
  err=torch.einsum('nkr,k->nr',w,k)-x[:,i]@e
  w=w-k[None,:,None]*err[:,None,:]
 return w

def metrics(pred,x):
 err=(pred-x).double().square().mean((0,1))
 return {'expected':err[:4].mean().item(),'changed':err[4:].mean().item(),'fields':err.tolist()}

def inspect(e,fit,test,rho):
 t=time.perf_counter();w=write(test,e).detach();writing=time.perf_counter()-t
 t=time.perf_counter();ordinary=w@e.T;reading=time.perf_counter()-t
 fitw=write(fit,e).reshape(-1,e.shape[1]).double()
 t=time.perf_counter();decoder=torch.linalg.lstsq(fitw,fit.reshape(-1,8).double(),rcond=1e-12,driver='gelsd').solution;fitting=time.perf_counter()-t
 pred=w.double()@decoder
 c=covariance(rho);ed=e.double();l=torch.linalg.cholesky(c)
 # SVD of whitened input-to-state map avoids squaring its condition number.
 u,s,v=torch.linalg.svd(l.T@ed,full_matrices=False)
 keep=s>s[0]*1e-12
 residual=l@(torch.eye(8,dtype=torch.float64)-u[:,keep]@u[:,keep].T)@l.T
 bound=residual.diag().clamp_min(0)
 return {'ordinary':metrics(ordinary,test),'probe':metrics(pred,test),
  'ideal_gaussian_mse':{'expected':bound[:4].mean().item(),'changed':bound[4:].mean().item(),'fields':bound.tolist()},
  'singular_values':s.tolist(),'numerical_rank_rcond_1e12':int(keep.sum()),
  'state_sha256':digest(w),'state_bytes_per_episode':w[0].numel()*w.element_size(),
  'seconds':{'write_test':writing,'read_all_test_fields':reading,'probe_fit_solve':fitting},
  'decoder':decoder.tolist()}

def train(rank,rho,objective,seed,steps):
 g=torch.Generator().manual_seed(seed);e=(.1*torch.randn(8,rank,generator=g)).requires_grad_();initial=e.detach().clone()
 opt=torch.optim.Adam([e],lr=.02,weight_decay=0)
 gen=torch.Generator().manual_seed(10000+seed)
 curve=[];t=time.perf_counter()
 for step in range(steps):
  z=torch.randn(32,8,8,generator=gen);x=torch.cat([z[...,:4],rho*z[...,:4]+(1-rho*rho)**.5*z[...,4:]],-1)
  pred=x@e@e.T
  loss=(pred[...,:4]-x[...,:4]).square().mean() if objective=='expected' else (pred-x).square().mean()
  opt.zero_grad();loss.backward();opt.step()
  assert torch.isfinite(loss)
  if step==0 or (step+1)%100==0:curve.append({'step':step+1,'loss':loss.item()})
 return initial,e.detach(),curve,time.perf_counter()-t

def preflight():
 torch.manual_seed(99);e=torch.randn(8,4,dtype=torch.float64,requires_grad=True);x=torch.randn(2,8,8,dtype=torch.float64)
 order=[6,2,0,7,5,1,4,3]
 w=write(x,e,order);direct=x@e
 assert torch.allclose(w,direct,atol=1e-12)
 grad=torch.autograd.grad((w@e.T).square().sum(),e)[0]
 directgrad=torch.autograd.grad((direct@e.T).square().sum(),e)[0]
 assert torch.allclose(grad,directgrad,atol=1e-10)
 # Independent autograd inner gradient, with repeat key and a changed last value.
 k=torch.eye(8,dtype=torch.float64)[2];prev=torch.randn(2,8,4,dtype=torch.float64,requires_grad=True);v=x[:,2]@e
 loss=.5*(torch.einsum('nkr,k->nr',prev,k)-v).square().sum()
 actual=prev-torch.autograd.grad(loss,prev,create_graph=True)[0]
 explicit=prev-k[None,:,None]*(prev[:,2]-v)[:,None,:]
 assert torch.allclose(actual,explicit)
 assert torch.allclose(actual[:,2],v)
 other=[0,1,3,4,5,6,7];assert torch.equal(actual[:,other],prev[:,other])
 # State cannot depend on future read/query; repeated reads don't mutate it.
 frozen=w.detach().clone();a=w@e.T;b=w@e.T;assert torch.equal(w,frozen)
 zero=write(x,e*0);assert torch.count_nonzero(zero)==0
 assert torch.equal(write(x,e),write(x,e))
 out={'gradient_max_error':(grad-directgrad).abs().max().item(),'write_max_error':(w-direct).abs().max().item(),
      'autograd_update_max_error':(actual-explicit).abs().max().item(),'overwrite_and_other_rows_preserved':True,
      'read_preserves_state':True,'zero_projection_ablation':True,'reset_deterministic':True,'script_sha256':sha(__file__)}
 dump(R/'analysis/preflight.json',out)
 print(json.dumps(out))

def run(stage):
 folder=R/'analysis'/stage
 if (folder/'manifest.json').exists():raise RuntimeError('Preserve previous run: output already exists')
 seeds=[90,91] if stage=='development' else list(range(5))
 rhos=[0.] if stage=='development' else [0.,.8]
 steps=1200;neval=256 if stage=='development' else 2048;nfit=1024
 base=900000 if stage=='development' else 700000
 manifest={'stage':stage,'seeds':seeds,'rhos':rhos,'ranks':[2,4,8],'steps':steps,'lr':.02,'optimizer':'Adam, no weight decay',
 'batch_episodes':32,'records_per_episode':8,'eval_episodes':neval,'probe_fit_episodes':nfit,'data_seed_base':base,
 'torch':torch.__version__,'torch_revision':torch.version.git_version,'numpy':np.__version__,'python':platform.python_version(),
 'device':'cpu','threads':1,'dtype':'float32','probe_dtype':'float64','script_sha256':sha(__file__),
 'protocol_sha256':sha(R/'notes'/('DESIGN.md' if stage=='development' else 'PROTOCOL.md')),
 'lock_sha256':sha(R/'uv.lock'),'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 dump(folder/'manifest.json',manifest)
 for rho in rhos:
  for seed in seeds:
   test=data(neval,rho,base+seed);fit=data(nfit,rho,base+100+seed)
   for rank in [2,4,8]:
    for objective in ['expected','broad']:
     initial,e,curve,elapsed=train(rank,rho,objective,seed,steps)
     row={'rho':rho,'seed':seed,'rank':rank,'objective':objective,'initial_e':initial.tolist(),'final_e':e.tolist(),
       'curve':curve,'training_seconds':elapsed,'training_records':steps*32*8,'shared_parameter_bytes':e.numel()*4,
       'test_data_sha256':digest(test),'fit_data_sha256':digest(fit),'zero_predictor':metrics(torch.zeros_like(test),test),
       'initial':inspect(initial,fit,test,rho),'final':inspect(e,fit,test,rho)}
     name=f'rho{rho}-s{seed}-r{rank}-{objective}'
     dump(folder/(name+'.json'),row)
     print(name,json.dumps(row['final']['ordinary']),flush=True)
    controls={}
    for name,order in [('expected_first',list(range(8))),('balanced',[0,4,1,5,2,6,3,7]),('changed_known',[4,5,6,7,0,1,2,3])]:
     enc=torch.eye(8)[:,order[:rank]];controls[name]=inspect(enc,fit,test,rho)
    g=torch.Generator().manual_seed(seed+500);random=torch.linalg.qr(torch.randn(8,rank,generator=g)).Q
    controls['random_orthogonal']=inspect(random,fit,test,rho)
    controls['full_records']=inspect(torch.eye(8),fit,test,rho)
    dump(folder/f'rho{rho}-s{seed}-r{rank}-controls.json',{'rho':rho,'seed':seed,'rank':rank,'controls':controls})

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['preflight','development','evaluation']);args=p.parse_args()
 torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
 preflight() if args.stage=='preflight' else run(args.stage)
