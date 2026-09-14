"""Privileged factorization diagnosis, not goal-blind task performance."""
import time
import torch
from experiment import Memory, SUPPORT, ROOT, data, targets, dump, inspect, sha

torch.set_num_threads(1)
torch.use_deterministic_algorithms(True)
out = ROOT/'analysis'/'diagnosis.json'
if out.exists(): raise RuntimeError('Preserve existing diagnosis')
rows=[]
for seed in [90,91]:
    for kind in ['supplied_encoder','supervised_encoder']:
        torch.manual_seed(seed)
        model=Memory(2)
        phases=[]
        if kind=='supervised_encoder':
            opt=torch.optim.Adam(model.enc.parameters(),lr=.01)
            t=time.perf_counter()
            for step in range(1000):
                loss=(model.encode(SUPPORT)-targets(SUPPORT)[:,:2]).square().mean()
                opt.zero_grad();loss.backward();opt.step()
            phases.append({'name':'encoder','steps':1000,'records':16000,'seconds':time.perf_counter()-t,'final_loss':loss.item()})
        encode=(lambda x: targets(x)[...,:2]) if kind=='supplied_encoder' else model.encode
        opt=torch.optim.Adam(model.dec.parameters(),lr=.01)
        t=time.perf_counter()
        z=encode(SUPPORT).detach()
        for step in range(1000):
            loss=(model.read(z)[:,:2]-targets(SUPPORT)[:,:2]).square().mean()
            opt.zero_grad();loss.backward();opt.step()
        phases.append({'name':'decoder','steps':1000,'records':16000,'seconds':time.perf_counter()-t,'final_loss':loss.item()})
        rows.append({'seed':seed,'kind':kind,'phases':phases,
                     'parameters':{k:v.tolist() for k,v in model.state_dict().items()},
                     'result':inspect(encode,model.read,2,data(512,1990000+seed),data(256,1990100+seed))})
        print(seed,kind,rows[-1]['result']['population_ordinary'],flush=True)
dump(out,{'rows':rows,'script_sha256':sha(__file__),'protocol_sha256':sha(ROOT/'notes/DIAGNOSIS.md')})
