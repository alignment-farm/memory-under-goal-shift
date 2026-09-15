"""Independent target definitions, conditional grouping, exhaustive query support."""
import itertools,json,time
from pathlib import Path
import numpy as np
import torch
from experiment import ROOT,Memory,SUPPORT,TASKS,sha,digest,dump

def query(m):
    # Independent arrangement of conditional agreement probability.
    pa,pb=m[:,0],m[:,1]
    p_same=(1+pa[:,0]*pb[:,0]+pa[:,1]*pb[:,1]+pa[:,4]*pb[:,4])/4
    return np.column_stack((pa[:,4],pa[:,5],pa[:,0]*pb[:,0],
                             m[:,0,0]*m[:,1,0]*m[:,2,0]*m[:,3,0],2*p_same-1))
def truth(x):
    return np.column_stack((x[:,0,0]*x[:,0,1],x[:,0,2]*x[:,0,3],
                            x[:,0,0]*x[:,1,0],np.prod(x[:,:,0],axis=1),
                            np.where((x[:,0,0]==x[:,1,0])&(x[:,0,1]==x[:,1,1]),1.,-1.)))
def labels(x): return np.column_stack((x,x[:,0]*x[:,1],x[:,2]*x[:,3])).astype(float)
def codeid(z): return np.sum((z>0).astype(int)*np.left_shift(1,np.arange(z.shape[-1])),axis=-1)
def means(c,x,r):
    return np.array([labels(x)[c==j].mean(0) if np.any(c==j) else np.zeros(6) for j in range(2**r)])
def metrics(p,y): return {task:{'mse':float(np.mean((p[:,j]-y[:,j])**2)),
                                  'accuracy':float(np.mean(np.where(p[:,j]>=0,1.,-1.)==y[:,j]))}
                         for j,task in enumerate(TASKS)}

def main():
    t=time.perf_counter();checks=0;maxdiff=0.;allpop={}
    tuples=np.array(list(itertools.product(range(16),repeat=4)))
    full_y=truth(SUPPORT[tuples])
    for stage in ['development','evaluation']:
        folder=ROOT/'analysis'/stage;man=json.loads((folder/'manifest.json').read_text())
        assert man['script_sha256']==sha(ROOT/'scripts/experiment.py')
        assert man['lock_sha256']==sha(ROOT.parent/'uv.lock')
        assert man['protocol_sha256']==sha(ROOT/'notes'/('DESIGN.md' if stage=='development' else 'PROTOCOL.md'))
        for name,h in man['donors'].items(): assert sha(ROOT/'donors'/name)==h
        for path in sorted(folder.glob('s*.json')):
            d=json.loads(path.read_text());r=d['result'];obj=d['objective'];seed=man['base']+d['seed']*10000;n=man['histories_per_seed']
            if obj in ['expected','broad']:
                donor=json.loads((ROOT/'donors'/f's{d["seed"]}-r4-{obj}.json').read_text());model=Memory(donor['parameters']);enc=model.encode;dec=model.decode;rank=4
            else:
                rank=4 if obj=='full_raw' else 2
                enc=(lambda x:x.copy()) if rank==4 else (lambda x:np.stack((x[...,0]*x[...,1],x[...,2]*x[...,3]),-1))
                dec=(lambda z:z) if rank==4 else (lambda z:np.stack((np.ones_like(z[...,0]),z[...,0],np.ones_like(z[...,1]),z[...,1]),-1))
            codes=enc(SUPPORT);ci=codeid(codes); exact=means(ci,SUPPORT,rank)
            assert np.array_equal(codes,r['support_codes']) and np.allclose(exact,r['exact_table'],atol=0,rtol=0)
            x=SUPPORT[np.random.default_rng(seed).integers(16,size=(n,32))]
            fit=SUPPORT[np.random.default_rng(seed+100000).integers(16,size=(128,32))]
            q=np.array([np.random.default_rng(seed+200000+i).choice(32,4,replace=False) for i in range(n)])
            w=enc(x);assert digest(w)==r['state_sha256'] and digest(x)==r['data_sha256'] and digest(q)==r['query_sha256'] and digest(fit)==r['fit_sha256']
            assert np.all(np.sort(q,axis=1)[:,1:]!=np.sort(q,axis=1)[:,:-1])
            fc=codeid(enc(fit)).ravel();emp=means(fc,fit.reshape(-1,4),rank)
            assert np.array_equal(emp,r['fit_table'])
            assert np.array_equal(np.bincount(fc,minlength=2**rank),r['fit_counts'])
            selected=w[np.arange(n)[:,None],q];sc=codeid(selected)
            y=truth(x[np.arange(n)[:,None],q]); raw=dec(selected)
            ordinary=query(labels(raw.reshape(-1,4)).reshape(n,4,6))
            preds={'ordinary':ordinary,'clipped':ordinary.clip(-1,1),'fitted':query(emp[sc]),'exact':query(exact[sc])}
            for reader,p in preds.items():
                current=metrics(p,y)
                for task in TASKS:
                    for measure in ['mse','accuracy']:
                        diff=abs(current[task][measure]-r['metrics'][reader][task][measure]);maxdiff=max(maxdiff,diff);assert diff<1e-12
                if reader!='exact':
                    for j,task in enumerate(TASKS):
                        parts=r['decomposition'][reader][task]
                        assert abs(sum(parts.values())-current[task]['mse'])<1e-10
            # Enumerate all queried inputs; group directly by joint stored code tuple.
            joint=np.sum(ci[tuples]*(2**rank)**np.arange(4),axis=1)
            counts=np.bincount(joint,minlength=(2**rank)**4)
            optimal=np.zeros_like(full_y)
            for j in range(5):
                totals=np.bincount(joint,weights=full_y[:,j],minlength=len(counts))
                optimal[:,j]=(totals/counts.clip(1))[joint]
            analytical=query(exact[ci[tuples]])
            assert np.allclose(optimal,analytical,atol=1e-14,rtol=0)
            risks=metrics(optimal,full_y)
            for task in TASKS: assert abs(risks[task]['mse']-r['population_optimal_mse'][task])<1e-12
            meanonly=exact.copy();meanonly[:,4]=exact[:,0]*exact[:,1]
            ablate=query(meanonly[ci[tuples]])[:,-1]
            # Compute population reader risks and decomposition with full support.
            rawfull=dec(codes)[tuples];ordfull=query(labels(rawfull.reshape(-1,4)).reshape(-1,4,6))
            population={'exact':risks,'ordinary':metrics(ordfull,full_y),
                        'clipped':metrics(ordfull.clip(-1,1),full_y),'fitted':metrics(query(emp[ci[tuples]]),full_y),
                        'agreement_meanonly_mse':float(np.mean((ablate-full_y[:,-1])**2)),
                        'agreement_meanonly_excess':float(np.mean((ablate-optimal[:,-1])**2))}
            for p in [ordfull,ordfull.clip(-1,1),query(emp[ci[tuples]])]:
                assert np.allclose(np.mean((p-full_y)**2,0),np.mean((optimal-full_y)**2,0)+np.mean((p-optimal)**2,0),atol=1e-10)
            allpop[f'{stage}/{path.stem}']=population;checks+=1
    # Provenance validates retained copies as well as originals, all read-only.
    for row in json.loads((ROOT/'sources/provenance.json').read_text()):
        assert sha(ROOT.parent/row['path'])==row['sha256']
    dump(ROOT/'analysis/population.json',allpop)
    dump(ROOT/'analysis/verification.json',{'representations':checks,'exhaustive_tuples_each':len(tuples),
        'max_metric_difference':maxdiff,'independent_conditional_grouping':True,
        'population_decomposition':True,'data_fit_query_state_hashes':True,
        'script_sha256':sha(__file__),'seconds':time.perf_counter()-t})
    print('Verified',checks,'representations;',len(tuples),'query tuples each; max metric difference',maxdiff)

if __name__=='__main__':
    torch.set_num_threads(1);torch.use_deterministic_algorithms(True);main()
