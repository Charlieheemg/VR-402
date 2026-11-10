"""Check the authoritative report, visible word budget and linked local HTML.

The conservative 4,000-word count includes headings, table/diagram text, captions,
inline citations and the full reference list inside main. Appendices are separate.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 4000

class Report(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.main = False
        self.ignore = 0
        self.bucket = None
        self.text = []
        self.by_bucket = {k: [] for k in ('shared', 'charlie', 'kang_zhe', 'references')}
        self.ids = []
        self.links = []
        self.images = []
        self.main_images = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'main':
            self.main = True
        if self.main and a.get('data-part'):
            self.bucket = a['data-part']
            assert self.bucket in self.by_bucket, self.bucket
        if tag in ('script', 'style'):
            self.ignore += 1
        if tag in ('a', 'link') and 'href' in a:
            self.links.append(a['href'])
        if tag in ('img', 'script') and 'src' in a:
            self.links.append(a['src'])
        if tag == 'img':
            assert a.get('alt'), 'Image lacks alt text'
            self.images.append(a)
            if self.main:
                self.main_images.append((a, self.bucket))

    def handle_endtag(self, tag):
        if tag == 'main':
            self.main = False
        if tag in ('script', 'style'):
            self.ignore -= 1

    def handle_data(self, data):
        if self.main and not self.ignore:
            assert self.bucket is not None or not data.strip(), 'Unallocated main text'
            self.text.append(data)
            if self.bucket:
                self.by_bucket[self.bucket].append(data)


def parse(path):
    p = Report()
    p.feed(path.read_text(encoding='utf-8'))
    assert len(p.ids) == len(set(p.ids)), f'Duplicate IDs: {path.relative_to(ROOT)}'
    return p


def local_links(path, parsed):
    checked = 0
    for link in parsed.links:
        u = urlsplit(link)
        if u.scheme or u.netloc:
            continue
        target = (path.parent / unquote(u.path)).resolve() if u.path else path
        assert target.is_relative_to(ROOT), f'Link escapes repository: {link}'
        assert target.exists(), f'{path.relative_to(ROOT)} → missing {link}'
        if target.name == 'interim-report.html':
            target = ROOT / 'index.html'
        if u.fragment and target.suffix == '.html':
            # Non-report historical pages do not allocate their main text.
            q = HTMLIds(); q.feed(target.read_text(encoding='utf-8'))
            assert unquote(u.fragment) in q.ids, f'{path.relative_to(ROOT)} → missing anchor {link}'
        checked += 1
    return checked

class HTMLIds(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag in ('a','link') and 'href' in a: self.links.append(a['href'])
        if tag in ('img','script') and 'src' in a: self.links.append(a['src'])
        if tag=='img': assert a.get('alt'), 'Image lacks alt text'


def check():
    path = ROOT / 'index.html'
    p = parse(path)
    words = lambda items: len(re.findall(r'\S+', ' '.join(items)))
    counts = {k: words(v) for k, v in p.by_bucket.items()}
    html_words = words(p.text)
    figure_words = 0
    for a, bucket in p.main_images:
        image_path = ROOT / a['src']
        if image_path.suffix == '.svg':
            root = ET.parse(image_path).getroot()
            n = sum(words([''.join(el.itertext())]) for el in root.iter() if el.tag.endswith('}text'))
        else:
            transcript = image_path.with_suffix('.txt')
            assert transcript.exists(), f'Raster figure needs visible-text transcript: {a["src"]}'
            n = words([transcript.read_text()])
        counts[bucket] += n
        figure_words += n
    total = html_words + figure_words
    assert total == sum(counts.values())
    assert total <= LIMIT, f'{total} words exceeds {LIMIT}'
    html = path.read_text()
    assert all(s in html for s in ('Paediatric VR Speech Analysis and Feedback', 'VR-405', 'Charlie Hee Ming Guan', 'Ang Kang Zhe', 'A/Prof Khoo Eng Tat'))
    assert 'VR-402' not in ' '.join(p.text), 'Incorrect official code in main text'
    assert counts['charlie'] > 0 and counts['kang_zhe'] > 0
    checked = local_links(path, p)
    pages = ['docs/project-design.html', 'docs/evidence.html', 'docs/speech-evidence.html', 'docs/feedback/report-evidence.html', 'docs/feedback/evaluation-v01.html', 'docs/feedback/output-v01.html']
    for name in pages:
        q = HTMLIds(); q.feed((ROOT/name).read_text())
        assert len(q.ids) == len(set(q.ids)), f'Duplicate IDs: {name}'
        checked += local_links(ROOT/name, q)
    alias = (ROOT/'interim-report.html').read_text()
    assert "location.replace('index.html'+location.search+location.hash)" in alias
    result = dict(authoritative_report='index.html', main_words=total,
                  html_main_words=html_words, visible_figure_words=figure_words,
                  limit=LIMIT, section_words=counts, headroom=LIMIT-total,
                  method='Whitespace tokens inside main, including references, headings, tables, HTML diagrams and captions, plus visible embedded-image labels; excludes masthead/navigation/footer and separate appendices',
                  local_links='passed', local_link_checks=checked, duplicate_ids='none',
                  image_alt='passed', metadata='passed', compatibility_page='interim-report.html preserves query and fragment')
    (ROOT/'docs/results/report-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result

if __name__ == '__main__':
    check()
