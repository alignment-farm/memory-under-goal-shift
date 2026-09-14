"""Fresh-history check of a derived explicit record against frozen memories."""
import json,time
import torch
import experiment as ex

def main():
 torch.set_num_threads(1);torch.use_deterministic_algorithms(True)
 folder=ex.R/'analysis/supplement'
 if (folder/'manifest.json').exists():raise RuntimeError('Preserve existing supplement')
 source=ex.R/'analysis/evaluation';inputs={}
 for rho in [0.,.8]:
  for seed in range(5):
   for obj in ['expected','broad']:
    p=source/f'rho{rho}-s{seed}-r4-{obj}.json';inputs[str(p.relative_to(ex.R))]=ex.sha(p)
 ex.dump(folder/'manifest.json',{'protocol_sha256':ex.sha(ex.R/'notes/SUPPLEMENT_PROTOCOL.md'),
 'runner_sha256':ex.sha(__file__),'engine_sha256':ex.sha(ex.__file__),'seed_base':810000,'episodes':2048,
 'source_results':inputs,'torch':torch.__version__,'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
 rows=[]
 for rho in [0.,.8]:
  for seed in range(5):
   x=ex.data(2048,rho,810000+seed)
   reps={obj:torch.tensor(json.loads((source/f'rho{rho}-s{seed}-r4-{obj}.json').read_text())['final_e']) for obj in ['expected','broad']}
   reps['explicit_pair_sum']=torch.cat([torch.eye(4),torch.eye(4)],0)/2**.5
   for name,e in reps.items():
    w=ex.write(x,e);pred=w@e.T
    if name=='explicit_pair_sum':
     direct=(x[...,:4]+x[...,4:])/2
     assert torch.allclose(pred,torch.cat([direct,direct],-1),atol=1e-6)
    rows.append({'rho':rho,'seed':seed,'condition':name,'data_sha256':ex.digest(x),'state_sha256':ex.digest(w),'ordinary':ex.metrics(pred,x)})
 ex.dump(folder/'results.json',{'rows':rows,'outer_training_runs':0})
 summary=[]
 for rho in [0.,.8]:
  for name in ['expected','broad','explicit_pair_sum']:
   rr=[r for r in rows if r['rho']==rho and r['condition']==name]
   summary.append({'rho':rho,'condition':name,**{goal:sum(r['ordinary'][goal] for r in rr)/len(rr) for goal in ['expected','changed']}})
 ex.dump(folder/'summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
