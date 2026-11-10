"""Check local links in published documentation and prohibited tracked file types."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser
import json,re,subprocess
from check_report import ROOT, HTMLIds

def markdown_anchors(text):
    ids=set(); seen={}
    for line in text.splitlines():
        if not line.startswith('#'): continue
        heading=re.sub(r'#+\s*','',line,count=1).strip().strip('#').strip().lower()
        slug=re.sub(r'[^\w\-\s]','',heading,flags=re.UNICODE).replace(' ','-')
        n=seen.get(slug,0); seen[slug]=n+1
        ids.add(slug if not n else f'{slug}-{n}')
    return ids

def check():
    failures=[]; checked=0; external=set()
    paths=[ROOT/'README.md',ROOT/'WORKFLOW.md',ROOT/'index.html',ROOT/'interim-report.html']
    paths+=sorted((ROOT/'docs').rglob('*.md'))+sorted((ROOT/'docs').rglob('*.html'))
    for path in paths:
        text=path.read_text(encoding='utf-8')
        if path.suffix=='.html':
            p=HTMLIds();p.feed(text);links=p.links
            if len(p.ids)!=len(set(p.ids)):failures.append(f'{path.relative_to(ROOT)}: duplicate IDs')
        else:
            text=re.sub(r'```.*?```','',text,flags=re.S)
            links=re.findall(r'\[[^\]]*\]\(([^\s]+?)(?:\s+"[^"]*")?\)',text)
        for link in links:
            link=link.strip('<>');u=urlsplit(link)
            if u.scheme or u.netloc:
                if u.scheme in ('http','https'):external.add(link)
                continue
            target=(path.parent/unquote(u.path)).resolve() if u.path else path
            checked+=1
            if not target.is_relative_to(ROOT) or not target.exists():
                failures.append(f'{path.relative_to(ROOT)}: missing {link}');continue
            if target.name=='interim-report.html':target=ROOT/'index.html'
            if u.fragment:
                if target.suffix=='.html':
                    p=HTMLIds();p.feed(target.read_text());ids=set(p.ids)
                elif target.suffix=='.md':ids=markdown_anchors(target.read_text())
                else:continue
                if unquote(u.fragment) not in ids:failures.append(f'{path.relative_to(ROOT)}: missing anchor {link}')
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    forbidden={'.wav','.mp3','.mp4','.xlsx','.xls','.joblib','.pkl','.pem','.key','.pdf'}
    sensitive=[p for p in tracked if p and (Path(p).suffix.lower() in forbidden or '/private/' in '/'+p or Path(p).name=='.env')]
    failures += ['Prohibited tracked raw/private type: '+p for p in sensitive]
    result={'documentation_files':len(paths),'local_link_checks':checked,'external_urls':len(external),'failures':failures,'tracked_raw_or_private_files':sensitive,'scope':'Root and docs HTML/Markdown links; tracked prohibited extensions/private paths. No claim of comprehensive content de-identification or external source verification.'}
    (ROOT/'docs/results/submission-repository-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert not failures, f'{len(failures)} repository checks failed'
    return result
if __name__=='__main__':check()
