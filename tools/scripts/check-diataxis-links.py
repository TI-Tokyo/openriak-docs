#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
import argparse
parser=argparse.ArgumentParser(description="Check rendered article links and anchors within the modern OpenRiak KV versions.")
parser.add_argument('build_root', type=Path, help="Hugo output directory containing openriak-kv/")
root=parser.parse_args().build_root
host='https://www.openriak.org' 
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.links=[];self.depth=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.add(d['id'])
  if tag=='article':self.depth+=1
  if self.depth and tag=='a' and 'href' in d:self.links.append(d['href'])
 def handle_endtag(self,tag):
  if tag=='article':self.depth=max(0,self.depth-1)
cache={};errors=set();count=0
for version in ['3.4.0','3.4.1']:
 for file in (root/'openriak-kv'/version).rglob('index.html'):
  page=Page(file.read_text());cache[file]=page;count+=1
  url=host+'/docs/'+str(file.relative_to(root)).removesuffix('index.html')
  for link in page.links:
   dest=urlsplit(urljoin(url,link))
   if dest.netloc!='www.openriak.org' or not dest.path.startswith('/docs/openriak-kv/'+version+'/'):continue
   target=root/unquote(dest.path.removeprefix('/docs/'))
   if target.is_dir():target/='index.html'
   if not target.exists():errors.add((str(file.relative_to(root)),link,'missing page'));continue
   if dest.fragment and target.suffix=='.html':
    if target not in cache:cache[target]=Page(target.read_text())
    if unquote(dest.fragment) not in cache[target].ids:errors.add((str(file.relative_to(root)),link,'missing anchor'))
for e in sorted(errors):print('\t'.join(e))
print('PAGES',count,'ERRORS',len(errors))
if count < 700: raise SystemExit('Expected both modern version trees; build with drafts enabled first.')
raise SystemExit(1 if errors else 0)
