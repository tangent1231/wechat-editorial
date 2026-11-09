#!/usr/bin/env python3
"""Flag fragile constructs in a safe, editable article export; not a platform validator."""
import argparse,json,re
from html.parser import HTMLParser
from pathlib import Path
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.errors=[];self.notes=[];self.images=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);s=a.get('style','')
  if tag in ('script','style','iframe','details','summary'):self.errors.append('Requires external/editor behavior: '+tag)
  if tag=='link' and a.get('rel')=='stylesheet':self.errors.append('External stylesheet')
  if re.search(r'(?:^|;)\s*width\s*:\s*\d+(?:\.\d+)?px',s):self.errors.append('Fixed pixel width')
  if re.search(r'display\s*:\s*(grid|flex)|overflow-x\s*:',s):self.errors.append('Experimental layout in safe export')
  if tag=='svg':self.notes.append('SVG needs target-editor validation')
  if tag=='table':self.notes.append('Table requires mobile and editor checks')
  if tag=='img':
   self.images+=1;src=a.get('src','')
   if src.startswith('file:') or '127.0.0.1' in src or src.startswith('blob:'):self.errors.append('Nonportable image URL')
   if src.startswith('data:'):self.notes.append('Embedded image may be filtered by target editor')
   elif not src.startswith(('https://','http://')):self.notes.append('Relative image requires uploaded/replaced media')
p=argparse.ArgumentParser();p.add_argument('html');a=p.parse_args();v=Audit();v.feed(Path(a.html).read_text());result={'errors':sorted(set(v.errors)),'notes':sorted(set(v.notes)),'images':v.images,'platform_status':'unverified'};print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(1 if v.errors else 0)
