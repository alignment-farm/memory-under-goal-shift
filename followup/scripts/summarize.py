"""Generate tables, cost accounting and an exportable risk decomposition."""
import json
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from experiment import ROOT, dump

groups=defaultdict(list)
for path in sorted((ROOT/'analysis/evaluation').glob('s*-r*.json')):
    row=json.loads(path.read_text());groups[f"learned_{row['objective']}_r{row['rank']}"] .append(row['result'])
for path in sorted((ROOT/'analysis/evaluation').glob('s*-controls.json')):
    for name,result in json.loads(path.read_text()).items():groups[name].append(result)
summary={}
table=['# Fresh nonlinear comparison','',
       'MSE; five seed blocks. Lower is better. Population values enumerate all 16 record types.', '',
       '| Representation | Expected ordinary | Changed ordinary | Changed fitted reader | Changed optimal (population) | Occupied codes |',
       '| --- | ---: | ---: | ---: | ---: | ---: |']
for name,rows in groups.items():
    result={}
    for reader in ['ordinary','empirical_reader','optimal_reader','population_ordinary','population_optimal']:
        result[reader]={}
        for family in ['expected','changed']:
            values=[r[reader][family] for r in rows]
            result[reader][family]={'mean':float(np.mean(values)),'min':min(values),'max':max(values),'seeds':values}
    result['occupied_codes']=[r['occupied_codes'] for r in rows]
    summary[name]=result
    cells=[result[k][f]['mean'] for k,f in [('ordinary','expected'),('ordinary','changed'),('empirical_reader','changed'),('population_optimal','changed')]]
    table.append('| '+name+' | '+' | '.join(f'{x:.6g}' for x in cells)+' | '+str(result['occupied_codes'])+' |')
table+=['','## Per-seed population risks','','| Representation | Seed index | Expected ordinary | Changed ordinary | Changed optimal | Reader excess |','| --- | ---: | ---: | ---: | ---: | ---: |']
for name,rows in groups.items():
    for seed,row in enumerate(rows):
        ordinary=row['population_ordinary'];best=row['population_optimal']
        table.append(f"| {name} | {seed} | {ordinary['expected']:.6g} | {ordinary['changed']:.6g} | {best['changed']:.6g} | {ordinary['changed']-best['changed']:.6g} |")
dump(ROOT/'analysis/summary.json',summary)
(ROOT/'analysis/TABLES.md').write_text('\n'.join(table)+'\n')

costs={}
for stage in ['development','evaluation']:
    rows=[json.loads(p.read_text()) for p in (ROOT/'analysis'/stage).glob('s*-r*.json')]
    costs[stage]={'fits':len(rows),'training_records':sum(r['training_records'] for r in rows),
                  'training_loop_seconds':sum(r['training_seconds'] for r in rows),
                  'shared_parameter_bytes':sorted(set(r['shared_parameter_bytes'] for r in rows))}
diag=json.loads((ROOT/'analysis/diagnosis.json').read_text())
phases=[p for r in diag['rows'] for p in r['phases']]
costs['diagnosis']={'optimizer_phases':len(phases),'training_records':sum(p['records'] for p in phases),'training_loop_seconds':sum(p['seconds'] for p in phases)}
costs['matching']={'r2_state_bytes':64,'r4_state_bytes':128,'r2_semantic_bits':16,'r4_semantic_bits':32,
                   'lookup_table_bytes_r2':192,'lookup_table_bytes_r4':768,'fitted_reader_labeled_records':4096,
                   'exact_reader_support_records':16,'teacher_compute':0,'external_model_calls':0,
                   'scope':'episodic payload matched; total bytes and compute not matched'}
dump(ROOT/'analysis/costs.json',costs)

fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True)
for ax,rank in zip(axes,[2,4]):
    names=[f'learned_expected_r{rank}',f'learned_broad_r{rank}']
    unavailable=[summary[n]['population_optimal']['changed']['mean'] for n in names]
    total=[summary[n]['population_ordinary']['changed']['mean'] for n in names]
    ax.bar([0,1],unavailable,label='Uncertainty from code collisions',color='#4379aa')
    ax.bar([0,1],np.array(total)-unavailable,bottom=unavailable,label='Ordinary reader excess error',color='#dc9d43')
    for i,n in enumerate(names):
        ax.scatter([i]*5,summary[n]['population_ordinary']['changed']['seeds'],s=18,c='black',zorder=3)
    ax.set_xticks([0,1],['Expected objective','Broad reconstruction'])
    ax.set_title(f'{rank} binary slots per record')
    ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Changed-use population MSE')
handles,labels=axes[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='upper center',ncol=2,frameon=False)
fig.tight_layout(rect=(0,0,1,.91))
fig.savefig(ROOT/'analysis/decomposition.png',dpi=180)
fig.savefig(ROOT/'analysis/decomposition.pdf')
print('\n'.join(table[:16]));print(json.dumps(costs,indent=2))
