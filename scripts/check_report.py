"""Reproducible conservative main word count and local HTML/link checks (stdlib)."""
from pathlib import Path
from html.parser import HTMLParser
import re,json
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
class Report(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.main=False;self.text=[];self.ids=[];self.links=[];self.images=[];self.image_buckets=[];self.bucket=None;self.by_bucket={k:[] for k in ["shared","charlie","kang_zhe"]}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='main':self.main=True
  if tag=='section' and self.main and a.get('id') in ['introduction','conclusion','part-b','part-a']:
   self.bucket='shared' if a.get('id') in ['introduction','conclusion'] else 'kang_zhe' if a.get('id')=='part-b' else 'charlie'
  if tag in ['a','link'] and 'href' in a:self.links.append(a['href'])
  if tag=='img':
   self.images.append(a);self.image_buckets.append(self.bucket if self.main else None);assert a.get('alt'),'Image lacks alt'
 def handle_endtag(self,tag):
  if tag=='main':self.main=False
 def handle_data(self,data):
  if self.main:
   self.text.append(data)
   if self.bucket:self.by_bucket[self.bucket].append(data)
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
 counts={k:len(re.findall(r"\S+",' '.join(v))) for k,v in p.by_bucket.items()}
 html_counts=counts.copy()
 import xml.etree.ElementTree as ET
 figure_words=0
 for a,bucket in zip(p.images,p.image_buckets):
  if bucket and a['src'].endswith('.svg'):
   root=ET.parse(ROOT/a['src']).getroot()
   n=sum(len(re.findall(r"\S+",''.join(e.itertext()))) for e in root.iter() if e.tag.endswith('}text'))
   counts[bucket]+=n;figure_words+=n
 assert len(words)+figure_words<=4000,'Main report including visible figure labels exceeds 4000 words'
 non_b=counts['shared']+counts['charlie']
 assert sum(counts.values())==len(words)+figure_words
 assert non_b+1800<=4000,'Insufficient room for a substantive 1800-word Part B'
 result=dict(main_words=len(words)+figure_words,html_main_words=len(words),visible_svg_words=figure_words,limit=4000,section_words=counts,html_section_words=html_counts,non_part_b_words=non_b,part_b_replacement_capacity=4000-non_b,completed_group_with_1500_word_part_b=non_b+1500,completed_group_with_1800_word_part_b=non_b+1800,method='Whitespace tokens inside main plus visible SVG text labels; includes tables, headings, captions and draft Part B; excludes masthead/navigation/references/appendices and SVG accessibility titles',part_b_status='Author review draft: theory-informed design, conceptual examples and proposed evaluation; no empirical results',local_links='passed',duplicate_ids='none',image_alt='passed',metadata='passed',figures=len(p.images))
 out=ROOT/'docs/results/report-checks.json';out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return result
if __name__=='__main__':check()
