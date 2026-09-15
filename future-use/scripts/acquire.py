"""Pin accepted local artifacts; no network or external executable dependency."""
import hashlib,json,shutil,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]; old=root.parent
revision='0d516aaa82d30d07e239b44e88ac43b5fdbfddef'
paths=['sources/2407.04620v4.sections.txt','sources/official-ttt.py',
       'followup/scripts/experiment.py','followup/FINDINGS.md','uv.lock']
paths += [f'followup/analysis/{stage}/s{s}-r4-{obj}.json'
          for stage,seeds in [('development',[90,91]),('evaluation',range(5))]
          for s in seeds for obj in ['expected','broad']]
rows=[]
for p in paths:
    content=(old/p).read_bytes()
    pinned=subprocess.check_output(['git','show',f'{revision}:{p}'])
    assert content==pinned,p
    rows.append({'path':p,'sha256':hashlib.sha256(content).hexdigest(),'revision':revision})
    if p.endswith('.json'): shutil.copyfile(old/p,root/'donors'/Path(p).name)
(root/'sources/provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
