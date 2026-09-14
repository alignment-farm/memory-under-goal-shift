"""Post-evaluation algebraic explanation; no new fitting or changed states."""
import json
import numpy as np
from experiment import ROOT, dump, sha

rows=[]
for path in sorted((ROOT/'analysis/evaluation').glob('s*-r4-expected.json')):
    saved=json.loads(path.read_text());r=saved['result']
    codes=np.array(r['support_codes']);table=np.array(r['optimal_table'])
    indices=((codes>0)*(2**np.arange(4))).sum(-1).astype(int)
    conditional=table[indices]
    # The best raw-field estimates need not multiply to the best parity answer.
    product_of_means=np.column_stack((conditional[:,2]*conditional[:,3],conditional[:,4]*conditional[:,5]))
    support=np.array(list(__import__('itertools').product([-1.,1.],repeat=4)))
    parity=np.column_stack((support[:,0]*support[:,1],support[:,2]*support[:,3]))
    loss=float(((parity-product_of_means)**2).mean())
    ordinary=np.array(r['support_outputs'])
    mean_risk=float(((support-ordinary[:,2:])**2).mean())
    best_risk=float(((support-conditional[:,2:])**2).mean())
    excess=float(((ordinary[:,2:]-conditional[:,2:])**2).mean())
    assert abs(mean_risk-best_risk-excess)<1e-12
    rows.append({'seed':saved['seed'],'changed_ordinary':mean_risk,'changed_optimal':best_risk,
                 'reader_excess':excess,'expected_error_product_of_conditional_raw_means':loss,
                 'expected_error_conditional_parity_mean':float(((parity-conditional[:,:2])**2).mean()),
                 'donor_sha256':sha(path)})
dump(ROOT/'analysis/moments.json',{'status':'post-evaluation algebraic analysis; no additional data or tuning',
                                'script_sha256':sha(__file__),'rows':rows})
print(json.dumps(rows,indent=2))
