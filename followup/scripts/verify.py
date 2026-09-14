"""Reload all evidence; independently check finite-state conditional risks."""
import json
import numpy as np
import torch
from experiment import ROOT, SUPPORT, Memory, data, targets, controls, inspect, sha, digest, dump, audit

torch.set_num_threads(1)
torch.use_deterministic_algorithms(True)
checks=0
maximum=0.


def compare(saved, actual):
    global checks, maximum
    for key in ['ordinary','empirical_reader','optimal_reader','population_ordinary','population_optimal']:
        a,b=np.array(saved[key]['fields']),np.array(actual[key]['fields'])
        error=float(abs(a-b).max());maximum=max(maximum,error)
        assert np.allclose(a,b,atol=1e-10,rtol=1e-8),(key,error)
    assert saved['state_sha256']==actual['state_sha256']
    for key in ['support_codes','partition','fit_counts','support_counts']:
        assert saved[key]==actual[key],key
    assert np.allclose(saved['empirical_table'],actual['empirical_table'],atol=1e-12)
    # Independent grouping by tuples, not the runner's bit-index arithmetic.
    z=np.array(saved['support_codes']);x=SUPPORT.numpy().astype(np.float64)
    y=np.column_stack((x[:,0]*x[:,1],x[:,2]*x[:,3],x))
    pred=np.zeros_like(y)
    for code in set(map(tuple,z)):
        members=np.all(z==np.array(code),axis=1)
        pred[members]=y[members].mean(0)
    residual=((y-pred)**2).mean(0)
    assert np.allclose(residual,saved['population_optimal']['fields'],atol=1e-12)
    ordinary=np.array(saved['support_outputs'])
    # Conditional-mean orthogonality: total error = unavailable + reader excess.
    total=((y-ordinary)**2).mean(0)
    excess=((pred-ordinary)**2).mean(0)
    assert np.allclose(total,residual+excess,atol=1e-12)
    checks+=1


def restore(row):
    model=Memory(row.get('rank',2))
    model.load_state_dict({k:torch.tensor(v) for k,v in row['parameters'].items()})
    return model


for stage in ['development','evaluation']:
    folder=ROOT/'analysis'/stage
    manifest=json.loads((folder/'manifest.json').read_text())
    assert sha(ROOT/'scripts/experiment.py')==manifest['script_sha256']
    assert sha(ROOT.parent/'uv.lock')==manifest['lock_sha256']
    assert sha(ROOT/'notes'/('DESIGN.md' if stage=='development' else 'PROTOCOL.md'))==manifest['protocol_sha256']
    for seed in manifest['seeds']:
        fit,test=data(512,manifest['base']+100+seed),data(manifest['test_histories'],manifest['base']+seed)
        for path in sorted(folder.glob(f's{seed}-r*.json')):
            row=json.loads(path.read_text());model=restore(row)
            assert digest(fit)==row['fit_sha256'] and digest(test)==row['test_sha256']
            compare(row['result'],inspect(model.encode,model.read,row['rank'],fit,test))
        rows=json.loads((folder/f's{seed}-controls.json').read_text())
        for name,r,encode,read in controls():
            compare(rows[name],inspect(encode,read,r,fit,test))

diagnosis=json.loads((ROOT/'analysis/diagnosis.json').read_text())
assert sha(ROOT/'scripts/diagnose.py')==diagnosis['script_sha256']
assert sha(ROOT/'notes/DIAGNOSIS.md')==diagnosis['protocol_sha256']
for row in diagnosis['rows']:
    model=restore(row);seed=row['seed']
    encode=(lambda x:targets(x)[...,:2]) if row['kind']=='supplied_encoder' else model.encode
    compare(row['result'],inspect(encode,model.read,2,data(512,1990000+seed),data(256,1990100+seed)))

provenance=json.loads((ROOT/'sources/provenance.json').read_text())
for path,expected in provenance['files'].items(): assert sha(ROOT.parent/path)==expected
result={'representations_verified':checks,'maximum_metric_difference':maximum,
        'independent_numpy_conditional_means':True,'exact_risk_decomposition':True,
        'source_protocol_and_runner_hashes':True,'mechanics':audit()}
dump(ROOT/'analysis/verification.json',result)
print(json.dumps(result,indent=2))
