"""Regenerate tables, cost accounting and standalone figure."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from experiment import ROOT,TASKS,dump

def main():
    rows=[json.loads(p.read_text()) for p in sorted((ROOT/'analysis/evaluation').glob('s*.json'))]
    pop=json.loads((ROOT/'analysis/population.json').read_text());summary={}
    lines=['# Complete fresh-history results','','Five fixed donor seed blocks; 8192 histories each. MSE / complete-answer accuracy.','',
           '| State | Reader | '+ ' | '.join(TASKS)+' |','|---|---|'+'---|'*5]
    for obj in ['expected','broad','full_raw','parities']:
        group=[d for d in rows if d['objective']==obj];summary[obj]={}
        for reader in ['ordinary','clipped','fitted','exact']:
            v={t:{m:float(np.mean([d['result']['metrics'][reader][t][m] for d in group])) for m in ['mse','accuracy']} for t in TASKS}
            summary[obj][reader]=v
            lines.append('| '+obj+' | '+reader+' | '+' | '.join(f'{v[t]["mse"]:.6g} / {v[t]["accuracy"]:.4f}' for t in TASKS)+' |')
        summary[obj]['population_optimal_mse']={t:{'mean':float(np.mean([d['result']['population_optimal_mse'][t] for d in group])),
            'min':min(d['result']['population_optimal_mse'][t] for d in group),'max':max(d['result']['population_optimal_mse'][t] for d in group)} for t in TASKS}
        summary[obj]['meanonly_agreement_population_mse']=float(np.mean([pop[f'evaluation/s{d["seed"]}-{obj}']['agreement_meanonly_mse'] for d in group]))
        summary[obj]['meanonly_agreement_excess']=float(np.mean([pop[f'evaluation/s{d["seed"]}-{obj}']['agreement_meanonly_excess'] for d in group]))
    lines+=['','## Per-seed learned outcomes','','| Seed | State | Reader | '+' | '.join(TASKS)+' |','|---|---|---|'+'---|'*5]
    for d in rows:
        if d['objective'] not in ['expected','broad']:continue
        for reader in ['ordinary','clipped','fitted','exact']:
            v=d['result']['metrics'][reader]
            lines.append(f'| {d["seed"]} | {d["objective"]} | {reader} | '+' | '.join(f'{v[t]["mse"]:.6g} / {v[t]["accuracy"]:.4f}' for t in TASKS)+' |')
    (ROOT/'analysis/TABLES.md').write_text('\n'.join(lines)+'\n');dump(ROOT/'analysis/summary.json',summary)
    cost={'new_gradient_training_seconds':0,'teacher_calls':0,'external_model_calls':0,
          'evaluation_unique_histories':5*8192,'development_unique_histories':2*512,
          'evaluation_query_answers_per_representation':5*8192*5,
          'notes':'Times are single batch calls, exclude RNG, I/O, setup and verification. Alternative fit includes calibration write. Training costs are prior sunk donor costs; also listed for rebuild. Explicit controls need neither fitting nor support enumeration in deployment: formulas suffice.',
          'per_representation':{}}
    allrows=[json.loads(p.read_text()) for stage in ['development','evaluation'] for p in (ROOT/'analysis'/stage).glob('s*.json')]
    cost['donor_rebuild_training_seconds']=sum(d.get('donor_training_seconds',0) for d in allrows)
    cost['donor_rebuild_training_records']=sum(d.get('donor_training_records',0) for d in allrows)
    cost['new_measured_pipeline_seconds']=sum(sum(d['result']['seconds'].values()) for d in allrows)
    cost['verification_seconds']=json.loads((ROOT/'analysis/verification.json').read_text())['seconds']
    for obj in ['expected','broad','full_raw','parities']:
        group=[d for d in rows if d['objective']==obj]
        cost['per_representation'][obj]={'state_bytes':group[0]['result']['state_bytes'],
           'semantic_bits':group[0]['result']['state_bytes']//4,
           'shared_parameter_bytes':group[0]['shared_parameter_bytes'],
           'fitted_table_bytes':group[0]['result']['reader_table_bytes'],
           'fitting_count_bytes':group[0]['result']['reader_count_bytes'],
           'seconds_per_8192_histories_mean':{k:float(np.mean([d['result']['seconds'][k] for d in group])) for k in group[0]['result']['seconds']},
           'bundled_query_state_values_read':16 if obj!='parities' else 8,
           'standalone_query_state_values_needed':{'expected':4 if obj!='parities' else 2,'parity2':8 if obj!='parities' else 4,'parity4':16 if obj!='parities' else 8,'agree_ab':8 if obj!='parities' else 4}}
    dump(ROOT/'analysis/costs.json',cost)
    fig,axes=plt.subplots(1,2,figsize=(9,3.7))
    xs=np.arange(5)
    for task,offset,color in [('parity2',-.22,'#3974ad'),('parity4',0,'#bf613c'),('agree_ab',.22,'#608348')]:
        vals=[pop[f'evaluation/s{s}-expected']['exact'][task]['mse'] for s in range(5)]
        axes[0].bar(xs+offset,vals,.21,label=task,color=color)
    axes[0].set(xticks=xs,xlabel='Frozen expected-writer seed',ylabel='Exact irreducible MSE',ylim=(0,1.05))
    axes[0].legend(frameon=False,fontsize=8)
    for reader,offset,color in [('ordinary',-.24,'#bd5947'),('clipped',-.08,'#dcab72'),('fitted',.08,'#729bb9'),('exact',.24,'#456a80')]:
        vals=[summary['expected'][reader][t]['mse'] for t in TASKS[2:]]
        axes[1].bar(np.arange(3)+offset,vals,.16,label=reader,color=color)
    axes[1].set(xticks=np.arange(3),xticklabels=TASKS[2:],ylabel='Fresh-history MSE, five-seed mean')
    axes[1].legend(frameon=False,fontsize=8)
    fig.tight_layout();fig.savefig(ROOT/'analysis/comparison.png',dpi=180);fig.savefig(ROOT/'analysis/comparison.pdf');plt.close(fig)
    print(json.dumps({'summary':summary,'costs':cost},indent=2))
if __name__=='__main__':main()
