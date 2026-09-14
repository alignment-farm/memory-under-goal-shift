"""Sequential cached source acquisition; one arXiv API request, no retries."""
import hashlib,json,urllib.request,urllib.error,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]; out=R/'sources'; records=[]
urls={'metadata.xml':'https://export.arxiv.org/api/query?id_list=2407.04620v4,2507.06415v3,2608.01672v1,2607.09415v1&max_results=4',
'2507.06415v3.html':'https://arxiv.org/html/2507.06415v3','2608.01672v1.html':'https://arxiv.org/html/2608.01672v1','2607.09415v1.html':'https://arxiv.org/html/2607.09415v1',
'official-repo.json':'https://api.github.com/repos/test-time-training/ttt-lm-pytorch/commits/main'}
for name,url in urls.items():
 p=out/name
 if p.exists():continue
 req=urllib.request.Request(url,headers={'User-Agent':'MemoryUnderGoalShift/0.1 (bounded academic methods study; sequential cached requests)'})
 rec={'url':url,'time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 try:
  with urllib.request.urlopen(req,timeout=30) as r: data=r.read();rec.update(status=r.status,headers=dict(r.headers))
 except urllib.error.HTTPError as e:data=e.read();rec.update(status=e.code,headers=dict(e.headers))
 except Exception as e:data=str(e).encode();rec.update(error=str(e))
 p.write_bytes(data);rec.update(path=str(p.relative_to(R)),sha256=hashlib.sha256(data).hexdigest());records.append(rec)
 print(name,rec.get('status',rec.get('error')),flush=True)
 (out/'retrieval.json').write_text(json.dumps(records,indent=2)+'\n')
