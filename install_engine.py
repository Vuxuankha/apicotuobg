#!/usr/bin/env python3
"""Fetch official Pikafish latest Linux x64 release; require bundled matching NNUE."""
import json,urllib.request,zipfile,tarfile,io,os,stat,shutil,tempfile,pathlib
api='https://api.github.com/repos/official-pikafish/Pikafish/releases/latest'
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'co-tuong-cloud-build','Accept':'application/vnd.github+json'})
 with urllib.request.urlopen(req,timeout=120) as resp:return resp.read()
release=json.loads(fetch(api)); assets=release.get('assets',[])
candidates=[a for a in assets if 'linux' in a['name'].lower() and any(s in a['name'].lower() for s in ['x64','x86-64','x86_64']) and a['name'].lower().endswith(('.zip','.tar.gz','.tgz'))]
if not candidates:raise SystemExit('Official release has no supported Linux x64 archive; provide matching binary and NNUE manually.')
a=sorted(candidates,key=lambda a: ('universal' not in a['name'].lower(),len(a['name'])))[0]
print('Downloading official:',a['name'],flush=True)
data=fetch(a['browser_download_url']); dest=pathlib.Path('/opt/pikafish'); dest.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
 root=pathlib.Path(tmp)
 if zipfile.is_zipfile(io.BytesIO(data)):
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   for entry in z.infolist():
    p=pathlib.PurePosixPath(entry.filename)
    if '..' in p.parts or p.is_absolute():continue
    if not entry.is_dir():
     target=root.joinpath(*p.parts);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(entry))
 else:
  with tarfile.open(fileobj=io.BytesIO(data),mode='r:*') as t:
   for m in t.getmembers():
    p=pathlib.PurePosixPath(m.name)
    if not m.isfile() or '..' in p.parts or p.is_absolute():continue
    target=root.joinpath(*p.parts);target.parent.mkdir(parents=True,exist_ok=True);f=t.extractfile(m)
    if f:target.write_bytes(f.read())
 files=list(root.rglob('*'))
 nets=[p for p in files if p.is_file() and p.suffix.lower()=='.nnue']
 bins=[p for p in files if p.is_file() and 'pikafish' in p.name.lower() and p.suffix.lower() not in ('.nnue','.txt','.md','.dll','.exe','.so')]
 if not nets or not bins:raise SystemExit('Archive lacks matching NNUE or Linux engine binary; refusing potentially mismatched engine.')
 bins=sorted(bins,key=lambda p:(not p.name.lower().startswith('pikafish'),len(p.name)))
 shutil.copyfile(bins[0],dest/'pikafish'); shutil.copyfile(nets[0],dest/'pikafish.nnue')
 os.chmod(dest/'pikafish',0o755)
 print('Installed engine + paired network',flush=True)
