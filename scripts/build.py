#!/usr/bin/env python3
"""Build editable inline HTML variants and a self-contained comparison workbench."""
import argparse,base64,hashlib,html,json,mimetypes,re,shutil
from pathlib import Path
from layouts import opening, chapter, DESCRIPTIONS
from export_html import export_html

THEMES=[
 ('corporate','商务简报','#ffffff','#173d65','#263849','left','line'),
 ('editorial','人文特刊','#faf7ef','#984e3e','#303a3b','left','open'),
 ('launch','产品发布','#eff3fc','#555ed4','#1c2945','dark','card'),
 ('technology','科技长卷','#eef4ff','#5075c7','#223655','left','card'),
 ('education','知识课堂','#fff9ed','#ad6e22','#453d31','left','step'),
 ('lifestyle','生活方式','#fff5f1','#ae6e78','#4c3c40','center','open'),
 ('interview','人物访谈','#f8f8f6','#50605d','#303b39','left','quote'),
 ('event','活动庆典','#f8f0ff','#8a54b5','#46365b','center','timeline'),
 ('report','数据观察','#f0f5f8','#236f87','#203b49','left','line'),
 ('nonprofit','公益纪实','#f0f7f0','#4e7955','#304b35','left','timeline'),
 ('minimal','极简公告','#ffffff','#202020','#252525','left','open'),
 ('luxury','品牌画册','#f8f4ed','#8a734d','#463c30','dark','open')]
E=lambda v:html.escape(str(v),quote=True)

def build(article_path,brand_path,out):
 a=json.loads(article_path.read_text(encoding='utf-8'));b=json.loads(brand_path.read_text(encoding='utf-8')) if brand_path else {}
 if not a.get('title') or not isinstance(a.get('sections'),list):raise ValueError('title and sections are required')
 for field in ('primary','accent'):
  if b.get(field) and not re.fullmatch(r'#[0-9a-fA-F]{6}',b[field]):raise ValueError(field+' must be #RRGGBB')
 out.mkdir(parents=True,exist_ok=True);(out/'media').mkdir(exist_ok=True)
 media=[];cache={}
 def img(file,alt='',width='100%',brand=False):
  if not file:return ''
  path=Path(file);path=path if path.is_absolute() else ((brand_path.parent if brand and brand_path else article_path.parent)/path)
  path=path.resolve()
  if path not in cache:
   raw=path.read_bytes();mime=mimetypes.guess_type(path.name)[0]
   if mime not in ('image/png','image/jpeg','image/webp','image/gif'):raise ValueError('Use a PNG/JPG/WebP/GIF for export: '+path.name)
   name=hashlib.sha256(raw).hexdigest()[:10]+path.suffix.lower();shutil.copyfile(path,out/'media'/name)
   cache[path]=('data:'+mime+';base64,'+base64.b64encode(raw).decode(),'media/'+name)
   media.append({'file':'media/'+name,'originalName':path.name,'alt':alt,'source': 'provided input'})
  return f'<img src="{cache[path][0]}" alt="{E(alt)}" style="display:block;width:{width};height:auto;margin:0 auto;border:0;"/>'
 def para(t,color,extra=''):return f'<p style="font-size:16px;line-height:1.9;margin:0 0 18px;color:{color};overflow-wrap:anywhere;{extra}">{E(t)}</p>'
 def link(url,label,color):
  if not re.match(r'^https?://',url):raise ValueError('Only http(s) content links are supported')
  return f'<a href="{E(url)}" style="color:{color};text-decoration:underline;overflow-wrap:anywhere;">{E(label)}</a>'
 variants=[]
 for tid,name,bg,accent,ink,align,layout in THEMES:
  accent=b.get('primary') or accent
  serif="Georgia,'Songti SC',serif" if tid in ('editorial','luxury','interview') else "-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif"
  dark=align=='dark';hero_bg=('#25283c' if tid=='launch' else '#322c28') if dark else bg
  titlecolor='#ffffff' if dark else ink
  brand=img(b.get('logo'),b.get('name',''),'22%',True)
  if b.get('name'):brand+=para(b['name'],titlecolor,'font-size:12px;letter-spacing:2px;')
  sub=para(a['subtitle'],titlecolor,'font-size:13px;') if a.get('subtitle') else ''
  meta=para(a['meta'],titlecolor,'font-size:12px;margin-bottom:0;') if a.get('meta') else ''
  cover=a.get('variantCovers',{}).get(tid,a.get('cover'))
  hero=img(cover,a.get('coverAlt',''))
  if a.get('coverMotionSafe'):hero=hero.replace('<img ','<img class="motion-safe" ',1)
  adorn=a.get('coverOrnaments',{}).get(tid)
  ornament='<div class="cover-ornament" style="text-align:right;padding:6px 0 12px;">'+img(adorn['file'],adorn.get('alt','装饰插画'),'20%')+'</div>' if adorn else ''
  intro=para(a['intro'],ink) if a.get('intro') else ''
  top=opening(tid,a,brand,a['title'],sub,meta,hero,intro,accent,ink,ornament)
  body=''
  for i,s in enumerate(a['sections']):
   paragraphs=s.get('paragraphs',[])
   if not isinstance(paragraphs,list):raise ValueError('paragraphs must be a list')
   text=''.join(para(t,ink) for t in paragraphs)
   extras=''
   if s.get('quote'):extras+=f'<blockquote style="margin:20px 0;padding:12px 5%;border-left:3px solid {accent};">'+para(s['quote'],ink,'font-size:18px;')+(para(s['attribution'],accent,'font-size:12px;') if s.get('attribution') else '')+'</blockquote>'
   if s.get('bullets'):extras+='<ul style="padding-left:22px;line-height:1.9;">'+''.join(f'<li style="margin:8px 0;color:{ink};">{E(t)}</li>' for t in s['bullets'])+'</ul>'
   photos=[]
   for im in s.get('images',[]):
    pic='<figure class="'+('ornament-figure' if im.get('role')=='ornament' else 'editorial-figure')+'" style="margin:18px 0;">'+img(im['file'],im.get('alt',im.get('caption','')), '28%' if im.get('role')=='ornament' else '100%')
    if im.get('caption'):pic+=f'<figcaption style="font-size:12px;line-height:1.7;margin-top:8px;color:{ink};">{E(im["caption"])}</figcaption>'
    photos.append(pic+'</figure>')
   links=''.join('<p style="font-size:14px;line-height:1.8;">'+link(item['url'],item['label'],accent)+'</p>' for item in s.get('links',[]))
   body+=chapter(tid,i,s,text,photos,extras,links,accent,ink,serif)
  if tid=='minimal' and hero:body+='<div style="padding:20px 7%;">'+hero+'</div>'
  foot='<footer style="padding:26px 7%;text-align:center;">'
  if a.get('closing'):foot+=para(a['closing'],ink,'font-size:20px;')
  if b.get('website'):foot+=para('官网',ink,'font-size:12px;')+link(b['website'],b.get('name') or b['website'],accent)
  if b.get('qr'):foot+='<div style="padding:24px 0;">'+img(b['qr'],'品牌二维码','56%',True)+para(b.get('qrCaption',''),ink,'font-size:12px;margin-top:12px;')+'</div>'
  for line in b.get('credits',[]):foot+=para(line,ink,'font-size:12px;margin:8px 0;')
  foot+='</footer>'
  content=f'<article style="padding:1px 0;width:100%;box-sizing:border-box;background-color:{bg};color:{ink};font-family:{serif};">{top}{body}{foot}</article>'
  export_content=export_html(content,tid,bg,ink)
  (out/(tid+'.html')).write_text(export_content,encoding='utf-8')
  variants.append({'id':tid,'name':name,'description':DESCRIPTIONS[tid],'html':content,'exportHtml':export_content})
 # Markdown uses the canonical cover even when every theme overrides it.
 if a.get('cover'):img(a['cover'],a.get('coverAlt',''))
 md=['# '+a['title'],'',a.get('subtitle',''),'']
 if a.get('cover'):md+=['!['+a.get('coverAlt','')+']('+cache[(article_path.parent/a['cover']).resolve()][1]+')','']
 md += [a.get('intro',''),'']
 for s in a['sections']:
  md+=['## '+s['title'],'']
  for t in s.get('paragraphs',[]):md += [t,'']
  if s.get('quote'):md+=['> '+s['quote']+(' — '+s['attribution'] if s.get('attribution') else ''),'']
  md += ['- '+t for t in s.get('bullets',[])]+['']
  for im in s.get('images',[]):
   q=(article_path.parent/im['file']).resolve();md+=['!['+im.get('caption','')+']('+cache[q][1]+')','']
  for item in s.get('links',[]):md+=['['+item['label']+']('+item['url']+')','']
 md += [a.get('closing',''),'']
 if b.get('website'):md+=['['+(b.get('name') or b['website'])+']('+b['website']+')','']
 if b.get('qr'):
  q=Path(b['qr']);q=q.resolve() if q.is_absolute() else ((brand_path.parent if brand_path else article_path.parent)/q).resolve()
  md+=['!['+b.get('qrCaption','品牌二维码')+']('+cache[q][1]+')','']
 md += b.get('credits',[])
 (out/'article.md').write_text('\n'.join(md),encoding='utf-8')
 (out/'media-manifest.json').write_text(json.dumps(media,ensure_ascii=False,indent=2),encoding='utf-8')
 template=(Path(__file__).resolve().parents[1]/'assets/workbench.html').read_text(encoding='utf-8')
 template=template.replace('__PREVIEW_CSS__',(Path(__file__).resolve().parents[1]/'assets/preview.css').read_text())
 template=template.replace('__CLIPBOARD_JS__',(Path(__file__).resolve().parents[1]/'assets/clipboard.js').read_text())
 (out/'preview.html').write_text(template.replace('__VARIANTS__',json.dumps(variants,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
 shutil.copyfile(Path(__file__).resolve().parents[1]/'assets/paste-check.html',out/'paste-check.html')
 print(str(out/'preview.html'))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('article',type=Path);p.add_argument('--brand',type=Path);p.add_argument('--output',required=True,type=Path);args=p.parse_args();build(args.article.resolve(),args.brand.resolve() if args.brand else None,args.output.resolve())
