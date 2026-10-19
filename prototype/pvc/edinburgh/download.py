"""Fetch public deposit files locally; never redistribute the downloaded corpus."""
import json,urllib.request,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'private/edinburgh'
BASE='https://datashare.ed.ac.uk/server/api/core/'
def get(url):
    return urllib.request.urlopen(url,timeout=120)
def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    bundles=json.load(get(BASE+'items/e0d78c30-c38d-41a5-947c-b03186a50a97/bundles'))['_embedded']['bundles']
    for b in bundles:
      if b['name'] not in ('ORIGINAL','LICENSE'):continue
      items=json.load(get(b['_links']['bitstreams']['href']+'?size=100'))['_embedded']['bitstreams']
      for f in items:
        name=Path(f['name']).name
        if name.endswith('.wav'):continue # samples duplicate archive contents
        target=ROOT/name
        if not target.exists() or target.stat().st_size!=f['sizeBytes']:
          print('Downloading',name,flush=True)
          with get(f['_links']['content']['href']) as response: target.write_bytes(response.read())
        if target.suffix=='.zip':
          with zipfile.ZipFile(target) as z:
            dest=ROOT/target.stem
            for member in z.infolist():
              resolved=(dest/member.filename).resolve()
              if not resolved.is_relative_to(dest.resolve()):raise ValueError('Unsafe archive path')
            z.extractall(dest)
    print('Local corpus ready:',ROOT)
if __name__=='__main__':main()
