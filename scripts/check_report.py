"""Reproducible conservative main word count and local HTML/link checks (stdlib)."""
from pathlib import Path
from html.parser import HTMLParser
import re,json
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
class Report(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.main=False;self.text=[];self.ids=[];self.links=[];self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='main':self.main=True
  if tag in ['a','link'] and 'href' in a:self.links.append(a['href'])
  if tag=='img':self.images.append(a);assert a.get('alt'),'Image lacks alt'
 def handle_endtag(self,tag):
  if tag=='main':self.main=False
 def handle_data(self,data):
  if self.main:self.text.append(data)
def check():
 p=Report();html=(ROOT/'index.html').read_text();p.feed(html)
 assert len(p.ids)==len(set(p.ids)),'Duplicate IDs'
 for link in p.links+[a['src'] for a in p.images]:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  if not u.path:
   assert not u.fragment or u.fragment in p.ids,link
  else:
   target=(ROOT/unquote(u.path)).resolve();assert target.is_relative_to(ROOT) and (target.exists() or u.path=='docs/results/report-checks.json'),link
 text=' '.join(p.text)
 # Count all whitespace words including section headings, citations, figure captions and draft Part B.
 words=re.findall(r"\S+",text)
 assert len(words)<=4000,f'{len(words)} main words exceeds 4000'
 assert all(s in html for s in ['Paediatric VR Speech Analysis and Feedback','VR-405','Charlie Hee Ming Guan','Ang Kang Zhe','A/Prof Khoo Eng Tat'])
 assert 'VR-402' not in text,'Old official code in main report'
 result=dict(main_words=len(words),limit=4000,method='Whitespace tokens of text inside main, including headings/captions/Part B draft; excludes title/navigation/references/appendices',part_b_status='Awaiting author evidence; target final group 3600–3800',local_links='passed',duplicate_ids='none',image_alt='passed',metadata='passed',figures=len(p.images))
 out=ROOT/'docs/results/report-checks.json';out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return result
if __name__=='__main__':check()
