#!/usr/bin/env python3
"""Optional Pillow utility: two original animated dividers with static fallbacks."""
from pathlib import Path
import math,json
from PIL import Image,ImageDraw
out=Path(__file__).resolve().parents[1]/'assets/motion';out.mkdir(exist_ok=True)
items=[]
for name,bg,fg,accent in [('signal-line',(240,246,255),(76,113,185),(93,197,197)),('warm-orbit',(250,247,239),(160,114,69),(123,147,106))]:
 frames=[]
 for k in range(60):
  im=Image.new('RGB',(720,96),bg);d=ImageDraw.Draw(im);t=2*math.pi*k/60
  if name=='signal-line':
   d.line((24,48,696,48),fill=tuple(int(v*.3+b*.7) for v,b in zip(fg,bg)),width=2)
   for i in range(7):
    x=72+i*96;r=4+2*math.sin(t-i*.5);d.ellipse((x-r,48-r,x+r,48+r),fill=fg)
   x=360+300*math.sin(t);d.ellipse((x-10,38,x+10,58),outline=accent,width=3)
   for x in (24,696):d.line((x-6,42,x,48,x-6,54),fill=fg,width=2)
  else:
   for x in (120,360,600):
    d.arc((x-34,14,x+34,82),0,360,fill=fg,width=2)
    xx=x+34*math.cos(t);yy=48+34*math.sin(t);d.ellipse((xx-5,yy-5,xx+5,yy+5),fill=accent)
   d.line((160,48,320,48),fill=fg,width=1);d.line((400,48,560,48),fill=fg,width=1)
  frames.append(im)
 frames[0].save(out/(name+'.png'))
 frames[0].save(out/(name+'.gif'),save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False,disposal=2)
 items.append({'file':name+'.gif','fallback':name+'.png','size':[720,96],'frames':60,'durationSeconds':6,'source':'Original procedural artwork; scripts/make_motion_assets.py','platformStatus':'Not imported or verified in Xiumi/WeChat'})
(out/'manifest.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
print(out)
