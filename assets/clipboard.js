// Shared payload: copy, manual selection, download, and copy-preview use exportHtml.
function copyPayload(){return variants[current].exportHtml;}
function readableText(html){const el=document.createElement('div');el.innerHTML=html;el.querySelectorAll('p,section,li,figcaption').forEach(n=>n.append(document.createTextNode('\n')));return el.textContent.replace(/\n{3,}/g,'\n\n').trim();}
function nativeCopy(html,text){
 const holder=document.createElement('div');holder.contentEditable='true';holder.setAttribute('aria-hidden','true');holder.style.cssText='position:fixed;left:-10000px;top:0;width:430px;background:white;';holder.innerHTML=html;document.body.append(holder);
 const selection=window.getSelection();const saved=Array.from({length:selection.rangeCount},(_,i)=>selection.getRangeAt(i).cloneRange());const previous=document.activeElement;
 holder.focus();const range=document.createRange();range.selectNodeContents(holder);selection.removeAllRanges();selection.addRange(range);
 const handler=e=>{if(e.clipboardData){e.clipboardData.setData('text/html',html);e.clipboardData.setData('text/plain',text);e.preventDefault()}};
 document.addEventListener('copy',handler);let success=false;
 try{success=document.execCommand('copy')}catch(e){}finally{document.removeEventListener('copy',handler);holder.remove();selection.removeAllRanges();saved.forEach(r=>selection.addRange(r));previous?.focus({preventScroll:true})}
 return success;
}
function download(){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([copyPayload()],{type:'text/html;charset=utf-8'}));a.download=variants[current].id+'-wechat.html';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),5000)}
document.getElementById('download').onclick=download;
document.getElementById('copy').onclick=async()=>{
 const html=copyPayload(),text=readableText(html);let method='原生富文本';let success=nativeCopy(html,text);
 if(!success){try{await navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([html],{type:'text/html'}),'text/plain':new Blob([text],{type:'text/plain'})})]);success=true;method='HTML 剪贴板'}catch(e){}}
 if(success){document.getElementById('exact').checked=true;show();document.getElementById('status').textContent='已复制公众号版（'+method+'）。当前显示即复制版：背景、字体已内联；请使用普通粘贴 ⌘V / Ctrl+V。';}
 else{document.getElementById('status').textContent='浏览器未允许自动复制。请点击“手动选择排版”，再按 ⌘C / Ctrl+C。';}
};
document.getElementById('manualCopy').onclick=()=>{const modal=document.getElementById('copyDialog');const paper=document.getElementById('manualPaper');paper.innerHTML=copyPayload();modal.showModal();paper.focus();const range=document.createRange();range.selectNodeContents(paper);window.getSelection().removeAllRanges();window.getSelection().addRange(range);};
document.getElementById('closeCopy').onclick=()=>document.getElementById('copyDialog').close();
