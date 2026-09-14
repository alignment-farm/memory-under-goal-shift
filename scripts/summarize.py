"""All-condition descriptive summaries and a standalone publication figure."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import experiment as ex

def stat(v):return {'mean':float(np.mean(v)),'min':float(np.min(v)),'max':float(np.max(v)),'values':[float(x) for x in v]}
def main():
 folder=ex.R/'analysis/evaluation';rows=[];records=[]
 for p in sorted(folder.glob('rho*.json')):
  r=json.loads(p.read_text());records.append(r)
  reps=r['controls'] if 'controls' in r else {r['objective']:r['final']}
  for name,result in reps.items():
   rows.append({'rho':r['rho'],'seed':r['seed'],'rank':r['rank'],'condition':name,'result':result})
 groups=[]
 for rho in [0.,.8]:
  for rank in [2,4,8]:
   for cond in ['expected','broad','expected_first','balanced','random_orthogonal','changed_known','full_records']:
    subset=sorted([x for x in rows if x['rho']==rho and x['rank']==rank and x['condition']==cond],key=lambda x:x['seed'])
    assert len(subset)==5
    item={'rho':rho,'rank':rank,'condition':cond}
    for reader in ['ordinary','probe','ideal_gaussian_mse']:
     item[reader]={goal:stat([x['result'][reader][goal] for x in subset]) for goal in ['expected','changed']}
    groups.append(item)
 def group(rho,rank,cond):return next(g for g in groups if (g['rho'],g['rank'],g['condition'])==(rho,rank,cond))
 rng=np.random.default_rng(20260914);contrasts=[]
 for label,rho,rank,c1,reader1,goal1,c2,reader2,goal2 in [
  ('rank4 expected objective: changed minus expected',0.,4,'expected','ordinary','changed','expected','ordinary','expected'),
  ('rank8 expected objective: changed ordinary minus probe',0.,8,'expected','ordinary','changed','expected','probe','changed'),
  ('rank4 changed: narrow minus broad objective',0.,4,'expected','ordinary','changed','broad','ordinary','changed'),
  ('rank4 expected: broad minus narrow objective',0.,4,'broad','ordinary','expected','expected','ordinary','expected'),
  ('correlated rank4 changed: ordinary minus probe',.8,4,'expected','ordinary','changed','expected','probe','changed')]:
  a=group(rho,rank,c1)[reader1][goal1]['values'];b=group(rho,rank,c2)[reader2][goal2]['values'];d=np.array(a)-b
  boot=rng.choice(d,(10000,len(d)),replace=True).mean(1)
  contrasts.append({'label':label,**stat(d),'descriptive_seed_bootstrap_95':np.quantile(boot,[.025,.975]).tolist()})
 learned=[r for r in records if 'objective' in r]
 init_final=[]
 for rho in [0.,.8]:
  for rank in [2,4,8]:
   rr=[r for r in learned if r['rho']==rho and r['rank']==rank and r['objective']=='expected']
   init_final.append({'rho':rho,'rank':rank,**{state:stat([r[state]['probe']['changed'] for r in rr]) for state in ['initial','final']}})
 summary={'groups':groups,'contrasts':contrasts,'initial_final_changed_probes':init_final,
  'learned_fits':len(learned),'training_seconds':sum(r['training_seconds'] for r in learned),
  'training_records':sum(r['training_records'] for r in learned),
  'source_result_hashes':{p.name:ex.sha(p) for p in folder.glob('*.json')},'script_sha256':ex.sha(__file__)}
 ex.dump(ex.R/'analysis/summary.json',summary)
 lines=['# Evaluation tables','', 'Mean MSE over five seed/data blocks; all conditions shown. Lower is better.','']
 for rho in [0.,.8]:
  lines+=['## Correlation '+str(rho),'','| Slots | Condition | Expected ordinary | Changed ordinary | Changed probe | Changed ideal |','| --- | --- | ---: | ---: | ---: | ---: |']
  for g in groups:
   if g['rho']!=rho:continue
   lines.append(f"| {g['rank']} | {g['condition']} | {g['ordinary']['expected']['mean']:.6g} | {g['ordinary']['changed']['mean']:.6g} | {g['probe']['changed']['mean']:.6g} | {g['ideal_gaussian_mse']['changed']['mean']:.6g} |")
  lines+=['']
 lines+=['## Paired differences','','| Contrast | Mean | Seed bootstrap 95% |','| --- | ---: | --- |']
 for c in contrasts:lines.append(f"| {c['label']} | {c['mean']:.6g} | {c['descriptive_seed_bootstrap_95'][0]:.6g}, {c['descriptive_seed_bootstrap_95'][1]:.6g} |")
 (ex.R/'analysis/TABLES.md').write_text('\n'.join(lines)+'\n')
 fig,axes=plt.subplots(1,3,figsize=(12,3.7),layout='constrained')
 config=[(0.,4,'Four slots: independent fields'),(0.,8,'Eight slots: independent fields'),(.8,4,'Four slots: correlated fields')]
 conditions=['expected','broad','expected_first','balanced'];labels=['Learned\nexpected','Learned\nbroad','Explicit\nexpected','Explicit\nbalanced']
 for ax,(rho,rank,title) in zip(axes,config):
  for j,(reader,goal,label,color) in enumerate([('ordinary','expected','Expected / ordinary','#267099'),('ordinary','changed','Changed / ordinary','#d2743c'),('probe','changed','Changed / probe','#46834e')]):
   ss=[group(rho,rank,c)[reader][goal] for c in conditions];means=np.array([s['mean'] for s in ss]);errs=np.array([[s['mean']-s['min'] for s in ss],[s['max']-s['mean'] for s in ss]])
   ax.bar(np.arange(4)+(j-1)*.24,means,width=.23,yerr=errs,capsize=2,color=color,label=label)
  ax.set_xticks(range(4),labels,fontsize=9);ax.set_title(title,fontsize=11);ax.set_ylim(0,1.12);ax.set_ylabel('Mean squared error');ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 fig.legend(*axes[0].get_legend_handles_labels(),loc='outside lower center',ncol=3,fontsize=9)
 fig.suptitle('Goal-specific writing and reader failure are separable\nBars: five-seed means; whiskers: seed ranges',fontsize=12)
 fig.savefig(ex.R/'analysis/comparison.png',dpi=180);fig.savefig(ex.R/'analysis/comparison.pdf')
 print(json.dumps({'fits':summary['learned_fits'],'training_seconds':summary['training_seconds'],'contrasts':contrasts},indent=2))
if __name__=='__main__':main()
