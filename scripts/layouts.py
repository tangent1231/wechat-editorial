"""Distinct editorial compositions. Inline fallback remains complete without CSS."""
from html import escape as E

DESCRIPTIONS={
 'corporate':'信息先行：导语摘要 → 封面 → 分栏编号章节',
 'editorial':'画面开篇：满幅封面 → 大标题 → 图文穿插特刊',
 'launch':'发布舞台：深色标题台 → 产品画面 → 功能说明条',
 'technology':'几何长卷：主题封面 → 导语浮卡 → 标题与正文分层',
 'education':'学习笔记：书页封面 → 导读 → 编号步骤与笔记框',
 'lifestyle':'生活画报：居中标题 → 拱形画面 → 大留白与双图',
 'interview':'人物侧写：图文并置封面 → 导语 → 边栏索引',
 'event':'活动邀请函：票券封面 → 信息条 → 节点卡与照片墙',
 'report':'观察报告：摘要与阅读索引 → 证据图 → 编号报告页',
 'nonprofit':'行动纪实：横幅画面 → 行动主线 → 连续时间轴',
 'minimal':'文字公告：紧凑标题 → 正文优先 → 补充封面在末尾',
 'luxury':'品牌画册：大留白刊头 → 全幅画面 → 展签式章节'
}

def box(content,style='',cls=''):
 return f'<div class="{cls}" style="box-sizing:border-box;{style}">{content}</div>'

def opening(tid,a,brand,title,sub,meta,hero,intro,accent,ink,ornament=''):
 def titleblock(size=36,color=None,align='left'):
  return f'<h1 style="font-size:{size}px;line-height:1.4;margin:16px 0 20px;color:{color or ink};text-align:{align};overflow-wrap:anywhere;">{E(a["title"])}</h1>'+ornament
 pad='padding:28px 7%;'
 introbox=box(intro,'padding:22px 7%;','intro-body') if intro else ''
 if tid=='corporate':
  return box(brand+titleblock(31)+sub+meta,pad+f'border-top:7px solid {accent};','cover cover-corporate')+box(intro,f'margin:0 7% 24px;padding:16px 5%;border-left:3px solid {accent};background-color:#f2f6f8;','intro-body')+box(hero,'padding:0 7% 30px;','cover-photo')
 if tid=='editorial':
  return box(brand,'padding:20px 7%;border-bottom:1px solid #cfc9bb;')+box(hero,'','cover-photo')+box(meta+titleblock(40)+sub,pad,'cover cover-editorial')+box(intro,'padding:0 9% 32px;border-bottom:1px solid #cfc9bb;margin-bottom:28px;','intro-body')
 if tid=='launch':
  return box(brand+titleblock(39,'#ffffff')+sub+box(hero,'padding:12px;background-color:#ffffff;border-radius:14px;margin:26px 0;','cover-photo')+meta,pad+'background-color:#202b47;color:#ffffff;','cover cover-launch')+box(intro,'padding:24px 8%;background-color:#ffffff;border-bottom:5px solid '+accent+';margin-bottom:30px;','intro-body')
 if tid=='technology':
  return box(brand+titleblock(40)+sub+meta,'padding:48px 7% 64px;','cover cover-technology')+box(hero,'width:86%;margin:0 auto;padding:8px;border:1px solid '+accent+';','cover-photo')+box(intro,'width:86%;margin:26px auto 32px;padding:23px 6%;background-color:white;border-radius:20px;','intro-body')
 if tid=='education':
  return box(box(brand+meta,'padding:14px 6%;background-color:#ecdfbf;')+box(titleblock(34)+sub,'padding:16px 7%;border-left:8px solid '+accent+';')+box(hero,'padding:10px 12% 28px;','cover-photo'),'padding:22px 5%;','cover cover-education')+box(intro,'margin:0 8% 34px;padding:24px 6%;border:1px dashed '+accent+';background-color:white;','intro-body')
 if tid=='lifestyle':
  return box(brand+sub+titleblock(34,align='center'),'padding:40px 10% 20px;text-align:center;','cover cover-lifestyle')+box(hero,'width:82%;margin:0 auto;','cover-photo')+box(meta+intro,'padding:30px 11% 48px;text-align:center;','intro-body')
 if tid=='interview':
  return box(brand,'padding:22px 7%;border-bottom:1px solid #bac5c2;')+box(box(hero,'','portrait-panel')+box(titleblock(34)+sub+meta,'padding:22px 7%;','portrait-title'),'','cover cover-interview')+box(intro,'margin:20px 8% 36px;padding:0 0 0 18px;border-left:4px solid '+accent+';','intro-body')
 if tid=='event':
  return box(brand+titleblock(36,align='center')+sub+box(meta,'padding:18px 8%;border-top:2px dashed '+accent+';margin-top:24px;'),'width:86%;margin:30px auto 0;padding:30px 7% 8px;background-color:white;border:1px solid '+accent+';text-align:center;','cover cover-event')+box(hero,'margin:22px 7% 0;padding:10px;background-color:white;','cover-photo')+box(intro,'margin:0 7% 38px;padding:24px 6%;background-color:white;border-bottom:3px dashed '+accent+';','intro-body')
 if tid=='report':
  toc=''.join(f'<p style="margin:10px 0;font-size:13px;line-height:1.7;">{i+1:02d}　{E(s["title"])}</p>' for i,s in enumerate(a['sections']))
  return box(brand+meta+titleblock(32)+sub,pad+'border-bottom:2px solid '+accent+';','cover cover-report')+box(intro+box(toc,'margin-top:20px;padding:12px 6%;border-top:1px solid '+accent+';','reading-index'),'padding:24px 7%;background-color:white;','intro-body')+box(hero,'padding:24px 7%;','cover-photo')
 if tid=='nonprofit':
  return box(brand,'padding:22px 7%;')+box(hero,'','cover-photo')+box(titleblock(34)+sub+meta,'margin:0 7%;padding:24px 0;border-bottom:3px solid '+accent+';','cover cover-nonprofit')+introbox
 if tid=='minimal':
  return box(brand+titleblock(28)+meta+sub,pad+'border-bottom:1px solid #d6d6d6;','cover cover-minimal')+introbox
 if tid=='luxury':
  return box(brand+box(sub,'margin:35px 0 12px;')+titleblock(39,'#f6eedc','center')+box(meta,'margin-top:36px;'),'padding:50px 12%;background-color:#302b25;color:#f6eedc;text-align:center;','cover cover-luxury')+box(hero,'','cover-photo')+box(intro,'padding:45px 13%;text-align:center;','intro-body')
 raise ValueError(tid)

def chapter(tid,i,s,paragraphs,photos,extras,links,accent,ink,serif):
 n=f'{i+1:02d}';label=E(s.get('label',''))
 small=f'<p style="font-size:11px;letter-spacing:2px;color:{accent};margin:0 0 10px;">{n} / {label}</p>'
 title=f'<h2 style="font-family:{serif};font-size:24px;line-height:1.5;margin:0 0 18px;color:{ink};overflow-wrap:anywhere;">{E(s["title"])}</h2>'
 large=f'<span style="display:block;font:52px Georgia,serif;color:{accent};line-height:1.1;margin-bottom:12px;">{n}</span>'
 photo_group=lambda ps:box(''.join(ps),'width:100%;','photo-group') if ps else ''
 text=box(paragraphs+extras,'','chapter-text')
 heading=small+title
 content=text+photo_group(photos)+links
 style='width:86%;margin:0 auto 32px;padding:22px 0;'
 if tid=='corporate':
  heading=box(large,'','chapter-index')+box(title+small,'','chapter-heading-text')
  content=text+photo_group(photos)+links;style+='border-top:1px solid '+accent+';'
 elif tid=='editorial':
  heading=large+title+small
  content=photo_group(photos[:1])+text+photo_group(photos[1:])+links;style='width:100%;margin:0 auto 45px;padding:0;'
  heading=box(heading,'padding:0 8%;');content=box(content,'padding:0 8%;')
 elif tid=='launch':
  heading=box(small,'display:inline-block;padding:7px 12px;background-color:#e5eafa;border-radius:20px;margin-bottom:12px;')+title
  content=photo_group(photos[:1])+text+photo_group(photos[1:])+links;style+='padding:24px 6%;background-color:white;border-radius:22px;'
 elif tid=='technology':
  heading=large+title+small
  content=box(text+photo_group(photos)+links,'padding:24px 6%;background-color:white;border-radius:20px;border:1px solid #cedded;','chapter-panel')
 elif tid=='education':
  heading=box(n,'display:inline-block;padding:9px 14px;border:2px solid '+accent+';border-radius:50%;font-size:22px;margin-bottom:14px;')+title+small
  content=box(text,'padding:20px 6%;border-left:3px solid '+accent+';background-color:#ffffff;')+photo_group(photos)+links
 elif tid=='lifestyle':
  heading=box(small+title,'text-align:center;margin:28px 0;')
  content=photo_group(photos[:1])+text+photo_group(photos[1:])+links;style='width:82%;margin:0 auto 48px;padding:0;'
 elif tid=='interview':
  heading=box(small,'','chapter-index')+title
  content=box(text+links,'padding:0 0 0 6%;border-left:2px solid '+accent+';','interview-answer')+photo_group(photos);style+='border-top:1px solid #c5cfca;'
 elif tid=='event':
  heading=box(large+small,'text-align:center;','event-date')+title
  content=photo_group(photos)+text+links;style+='padding:24px 6%;background-color:white;border-top:3px dashed '+accent+';border-bottom:3px dashed '+accent+';border-radius:18px;'
 elif tid=='report':
  heading=large+title+small
  content=text+box(photo_group(photos),'padding:14px 5%;background-color:#e7eff3;','evidence-panel')+links if photos else text+links
  style+='border-top:4px solid '+accent+';'
 elif tid=='nonprofit':
  heading=box(n,'display:inline-block;border:1px solid '+accent+';padding:8px 12px;border-radius:50%;margin-bottom:14px;')+title+small
  content=photo_group(photos[:1])+text+photo_group(photos[1:])+links;style='width:82%;margin:0 6% 0 12%;padding:16px 0 38px 7%;border-left:2px solid '+accent+';'
 elif tid=='minimal':
  heading=title;content=text+photo_group(photos)+links;style='width:86%;margin:24px auto;padding:0 0 20px;border-bottom:1px solid #dedede;'
 elif tid=='luxury':
  heading=box(small+title,'text-align:center;border-top:1px solid '+accent+';padding-top:22px;')
  content=photo_group(photos)+box(text+links,'padding:24px 7%;');style='width:90%;margin:0 auto 52px;padding:0;'
 return f'<section class="article-section chapter-{tid}" style="box-sizing:border-box;{style}">'+box(heading,'','section-heading')+box(content,'','section-content')+'</section>'
