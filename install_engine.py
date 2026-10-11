#!/usr/bin/env python3
"""Install matched official Pikafish Linux x86-64 engine and NNUE from GitHub release."""
import io, json, os, pathlib, shutil, stat, tarfile, tempfile, urllib.request, zipfile
API = 'https://api.github.com/repos/official-pikafish/Pikafish/releases/latest'
DEST = pathlib.Path('/opt/pikafish')
HEADERS = {'User-Agent':'xiangqi-cloud-render-installer', 'Accept':'application/vnd.github+json'}
def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=180) as response:
        return response.read()
def unpack(data, name, dest):
    if zipfile.is_zipfile(io.BytesIO(data)):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for item in z.infolist():
                part=pathlib.PurePosixPath(item.filename)
                if item.is_dir() or '..' in part.parts or part.is_absolute(): continue
                out=dest.joinpath(*part.parts);out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(z.read(item))
    elif name.lower().endswith(('.tar.gz','.tgz','.tar.xz')):
        with tarfile.open(fileobj=io.BytesIO(data),mode='r:*') as t:
            for item in t.getmembers():
                part=pathlib.PurePosixPath(item.name)
                if not item.isfile() or '..' in part.parts or part.is_absolute():continue
                out=dest.joinpath(*part.parts);out.parent.mkdir(parents=True,exist_ok=True)
                f=t.extractfile(item)
                if f:out.write_bytes(f.read())
    else:
        (dest/name).write_bytes(data)
def engine_priority(p):
    s=p.name.lower(); full=str(p).lower()
    if s.endswith(('.exe','.dll','.so','.nnue','.txt','.md','.json')) or not s.startswith('pikafish'):return -1
    if 'windows' in full or 'android' in full or 'macos' in full:return -1
    if 'linux' in full and ('x86-64' in full or 'x64' in full or 'x86_64' in full):return 100
    if 'linux' in full:return 80
    if 'universal' in full:return 40
    return 20
def run():
    release=json.loads(fetch(API)); assets=release.get('assets',[])
    print('Release:',release.get('tag_name'),'Assets:',*[a['name'] for a in assets], sep='\n',flush=True)
    if not assets:raise RuntimeError('Release without downloadable assets')
    with tempfile.TemporaryDirectory() as tmp:
        root=pathlib.Path(tmp)
        # Latest release may bundle all platforms in a single archive. Inspect its content.
        candidates=sorted(assets,key=lambda a:(0 if a['name'].lower().endswith(('.zip','.tar.gz','.tgz')) else 1, 0 if 'linux' in a['name'].lower() else 1))
        for asset in candidates:
            nm=asset['name'];low=nm.lower()
            if low.endswith(('.exe','.dmg','.apk')):continue
            if not (low.endswith(('.zip','.tgz','.tar.gz','.tar.xz','.nnue')) or ('pikafish' in low and ('linux' in low or 'x86-64' in low))):continue
            print('Downloading:',nm,flush=True)
            folder=root/('asset_'+str(len(list(root.iterdir()))));folder.mkdir()
            unpack(fetch(asset['browser_download_url']),nm,folder)
        files=[p for p in root.rglob('*') if p.is_file()]
        bins=sorted((p for p in files if engine_priority(p)>0),key=engine_priority,reverse=True)
        nets=[p for p in files if p.suffix.lower()=='.nnue']
        if not bins or not nets:raise RuntimeError('Unable to locate Linux x86-64 binary and NNUE in release assets: '+', '.join(a['name'] for a in assets))
        # Prefer a network next to the executable if present.
        exe=bins[0]; net=min(nets,key=lambda p:0 if p.parent==exe.parent else 1)
        DEST.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(exe,DEST/'pikafish');shutil.copyfile(net,DEST/'pikafish.nnue')
        os.chmod(DEST/'pikafish',0o755)
        print('Installed binary:',exe,'NNUE:',net,'size:',(DEST/'pikafish.nnue').stat().st_size,flush=True)
if __name__=='__main__':run()
