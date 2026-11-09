"""Serialize a fully inline, editable WeChat copy edition (no browser CSS needed)."""
from html.parser import HTMLParser
from html import escape

FONT = "'PingFang SC','Microsoft YaHei',Arial,sans-serif"
INHERITED = ('font-family','font-size','line-height','font-weight','color','letter-spacing','text-align')
TEXT_STYLE = ('font-family','font-size','line-height','font-weight','color','letter-spacing')

def declarations(value):
    return dict((k.strip(),v.strip()) for part in value.split(';') if ':' in part for k,v in [part.split(':',1)])
def css(d):
    return ';'.join(f'{k}:{v}' for k,v in d.items())+';'

class InlineEdition(HTMLParser):
    def __init__(self,theme,bg,ink):
        super().__init__(convert_charrefs=True)
        self.theme,self.bg,self.ink=theme,bg,ink
        self.stack=[];self.output=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);own=declarations(attrs.get('style',''))
        parent=self.stack[-1][1] if self.stack else {'font-family':FONT,'font-size':'16px','line-height':'1.9','font-weight':'400','color':self.ink,'letter-spacing':'0px','text-align':'left'}
        style={k:parent[k] for k in INHERITED if k in parent};style.update(own)
        style['font-family']=FONT;style['box-sizing']='border-box'
        # Font shorthand in chapter numbers must not override the Chinese-safe family.
        if 'font' in style:
            style.pop('font');style.update({'font-size':'36px','line-height':'1.2','font-weight':'600'})
        if tag in ('h1','h2','h3'):
            size=int(float(own.get('font-size','24px').replace('px','')))
            style['font-size']=str(min(size,32 if tag=='h1' else 23))+'px'
            style['font-weight']='600';style['line-height']='1.5';style['letter-spacing']='0px'
        if tag in ('p','li','h1','h2','h3','figcaption','span'):
            style['word-break']='normal';style['overflow-wrap']='break-word'
        if tag=='article':
            style.update({'background-color':self.bg,'width':'100%','max-width':'100%','text-align':'left'})
            if self.theme=='technology':style['background-image']='linear-gradient(140deg,#e3f1ff 0%,#eef4ff 50%,#ede8fa 100%)'
        # Repeat the base colour on top-level containers; no dependence on a page body.
        if len(self.stack)==1 and tag not in ('img','br','hr'):
            style.setdefault('background-color',self.bg)
        if tag=='img':
            style.update({'max-width':'100%','height':'auto','vertical-align':'middle'})
        # Paragraph headings survive editor normalization; text remains editable.
        newtag='p' if tag in ('h1','h2','h3','figcaption') else ('section' if tag in ('article','div','footer','figure') else tag)
        attrs={k:v for k,v in attrs.items() if k in ('class','href','src','alt','title')}
        attrs['style']=css(style)
        self.output.append('<'+newtag+''.join(' '+k+'="'+escape(v,quote=True)+'"' for k,v in attrs.items())+'>')
        if tag not in ('img','br','hr'):self.stack.append((newtag,style))
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in ('img','br','hr'):self.handle_endtag(tag)
    def handle_endtag(self,tag):
        if tag not in ('img','br','hr') and self.stack:self.output.append('</'+self.stack.pop()[0]+'>')
    def handle_data(self,data):
        if not data:return
        if not data.strip():self.output.append(data);return
        style=self.stack[-1][1] if self.stack else {}
        self.output.append('<span style="'+escape(css({k:style[k] for k in TEXT_STYLE if k in style}),quote=True)+'">'+escape(data)+'</span>')

def export_html(content,theme,bg,ink):
    parser=InlineEdition(theme,bg,ink);parser.feed(content);parser.close()
    return ''.join(parser.output)
