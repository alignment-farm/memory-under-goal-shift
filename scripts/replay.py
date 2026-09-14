"""Optional full retraining into a new directory; preserve original evidence."""
import argparse,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--destination',type=Path,required=True);p.add_argument('--stage',choices=['development','evaluation'],default='evaluation');args=p.parse_args()
root=Path(__file__).resolve().parents[1];dest=args.destination.resolve()
if dest.exists():raise SystemExit('Destination must not already exist; existing evidence is never removed.')
dest.mkdir(parents=True)
for name in ['scripts/experiment.py','pyproject.toml','uv.lock','notes/DESIGN.md','notes/PROTOCOL.md']:
 target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/name,target)
subprocess.run([sys.executable,str(dest/'scripts/experiment.py'),args.stage],cwd=dest,check=True)
print('Replay retained at',dest)
