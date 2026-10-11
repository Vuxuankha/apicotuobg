#!/usr/bin/env python3
"""Build native Pikafish from official release source on Linux x86-64.
Downloads NNUE separately; fails loudly if an exact compatible net is unavailable.
"""
import json, os, pathlib, shutil, subprocess, tarfile, tempfile, urllib.request
API = 'https://api.github.com/repos/official-pikafish/Pikafish/releases/latest'
NET = 'https://github.com/official-pikafish/Networks/releases/download/master-net/pikafish.nnue'
OUT = pathlib.Path('/opt/pikafish')
HEAD = {'User-Agent':'pikafish-cloud-render-source-builder'}
def download(url, dest):
    req=urllib.request.Request(url,headers=HEAD)
    with urllib.request.urlopen(req,timeout=180) as r,open(dest,'wb') as f:
        shutil.copyfileobj(r,f)
def run():
    with tempfile.TemporaryDirectory() as tmp:
        tmp=pathlib.Path(tmp)
        rel=tmp/'release.json';download(API,rel)
        info=json.loads(rel.read_text())
        tag=info.get('tag_name'); print('Building official release',tag,flush=True)
        archive=tmp/'source.tar.gz';download(info['tarball_url'],archive)
        src_root=tmp/'src';src_root.mkdir()
        with tarfile.open(archive,'r:gz') as tar:
            for member in tar.getmembers():
                parts=pathlib.PurePosixPath(member.name).parts
                if len(parts)<2 or '..' in parts or not member.isfile():continue
                relpath=pathlib.Path(*parts[1:])
                if relpath.parts[0]!='src':continue
                target=src_root/relpath;target.parent.mkdir(parents=True,exist_ok=True)
                r=tar.extractfile(member)
                if r:
                    with open(target,'wb') as w:shutil.copyfileobj(r,w)
        builddir=src_root/'src'
        if not (builddir/'Makefile').exists():raise RuntimeError('Missing official src/Makefile')
        print('Compiling native x86-64 baseline build',flush=True)
        subprocess.run(['make','-j2','build','ARCH=x86-64'],cwd=builddir,check=True)
        exe=builddir/'pikafish'
        if not exe.is_file():raise RuntimeError('Pikafish build output missing')
        OUT.mkdir(parents=True,exist_ok=True)
        shutil.copy2(exe,OUT/'pikafish');os.chmod(OUT/'pikafish',0o755)
        print('Downloading official NNUE network',flush=True)
        download(NET,OUT/'pikafish.nnue')
        if (OUT/'pikafish.nnue').stat().st_size<1_000_000:raise RuntimeError('NNUE download unusually small')
        # Engine version and network compatibility must be tested after deployment.
        print('Installed source build and network; verify UCI startup and go movetime in Render',flush=True)
if __name__=='__main__':run()
