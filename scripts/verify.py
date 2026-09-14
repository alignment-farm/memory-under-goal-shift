"""Reload all evidence without retraining; independent NumPy algebra checks."""
import json,math
from pathlib import Path
import numpy as np
import torch
import experiment as ex

def compare(a,b):
 if isinstance(a,dict):
  for k in a:compare(a[k],b[k])
 elif isinstance(a,list):
  for x,y in zip(a,b):compare(x,y)
 else:assert math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-12),(a,b)

def verify_one(e,fit,test,rho,saved):
 w=ex.write(test,e)
 assert ex.digest(w)==saved['state_sha256']
 compare(saved['ordinary'],ex.metrics(w@e.T,test))
 d=torch.tensor(saved['decoder'],dtype=torch.float64)
 compare(saved['probe'],ex.metrics(w.double()@d,test))
 # independent vectorized writer, and a different covariance formulation
 wn=test.numpy().astype(np.float64)@e.numpy().astype(np.float64)
 maxerr=float(np.max(np.abs(wn-w.numpy())))
 assert maxerr<3e-6,maxerr
 c=ex.covariance(rho).numpy();en=e.numpy().astype(np.float64)
 residual=c-c@en@np.linalg.pinv(en.T@c@en,rcond=1e-14)@en.T@c
 err=float(np.max(np.abs(np.diag(residual)-saved['ideal_gaussian_mse']['fields'])))
 assert err<1e-6,err
 # Verify fitted coefficients satisfy the normal equations on probe-only data.
 fw=ex.write(fit,e).reshape(-1,e.shape[1]).double();fy=fit.reshape(-1,8).double()
 normal=(fw.T@(fw@d-fy))/len(fw)
 assert normal.abs().max()<1e-10
 return maxerr,err

def main():
 torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
 counts={};worst=[0.,0.];files={};acquisition=[]
 for stage in ['development','evaluation']:
  folder=ex.R/'analysis'/stage;m=json.loads((folder/'manifest.json').read_text())
  assert m['script_sha256']==ex.sha(ex.__file__)
  assert m['protocol_sha256']==ex.sha(ex.R/'notes'/('DESIGN.md' if stage=='development' else 'PROTOCOL.md'))
  assert m['lock_sha256']==ex.sha(ex.R/'uv.lock')
  assert m['torch']==torch.__version__
  count=0
  for p in sorted(folder.glob('rho*.json')):
   files[str(p.relative_to(ex.R))]=ex.sha(p);r=json.loads(p.read_text())
   test=ex.data(m['eval_episodes'],r['rho'],m['data_seed_base']+r['seed'])
   fit=ex.data(m['probe_fit_episodes'],r['rho'],m['data_seed_base']+100+r['seed'])
   rank=r['rank']
   if 'controls' in r:
    maps={'expected_first':list(range(8)),'balanced':[0,4,1,5,2,6,3,7],'changed_known':[4,5,6,7,0,1,2,3]}
    encs={name:torch.eye(8)[:,order[:rank]] for name,order in maps.items()}
    g=torch.Generator().manual_seed(r['seed']+500);encs['random_orthogonal']=torch.linalg.qr(torch.randn(8,rank,generator=g)).Q
    encs['full_records']=torch.eye(8)
    assert r['controls']['full_records']['ordinary']['expected']==0
    assert r['controls']['full_records']['ordinary']['changed']==0
    for name,e in encs.items():
     errors=verify_one(e,fit,test,r['rho'],r['controls'][name]);worst=[max(a,b) for a,b in zip(worst,errors)];count+=1
   else:
    assert ex.digest(test)==r['test_data_sha256'];assert ex.digest(fit)==r['fit_data_sha256']
    for state in ['initial','final']:
     e=torch.tensor(r[state+'_e']);errors=verify_one(e,fit,test,r['rho'],r[state]);worst=[max(a,b) for a,b in zip(worst,errors)];count+=1
    if r['objective']=='expected' and rank>=4:
     assert r['final']['ordinary']['expected']<.01;acquisition.append(r['final']['ordinary']['expected'])
    assert len(r['curve'])==13
  counts[stage]=count
 sources=json.loads((ex.R/'sources/provenance.json').read_text())
 for path,h in sources['files'].items():assert ex.sha(ex.R/path)==h,path
 out={'passed':True,'representations_reloaded':counts,'max_numpy_write_difference':worst[0],
 'max_covariance_formulation_difference':worst[1],'max_expected_acquisition_mse_r_ge_4':max(acquisition),
 'source_hashes_verified':len(sources['files']),'result_hashes':files,'script_sha256':ex.sha(__file__),
 'checks':['frozen runner/protocol/lock hashes','all stored-state hashes','all ordinary/probe metrics',
 'full record exact recovery','probe normal equations on fit histories','independent NumPy writer and covariance',
 'every sufficient-capacity expected fit acquired','source cache hashes'],'training_reruns':0}
 ex.dump(ex.R/'analysis/verification.json',out);print(json.dumps({k:v for k,v in out.items() if k!='result_hashes'},indent=2))
if __name__=='__main__':main()
