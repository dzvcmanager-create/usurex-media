import re
from playwright.sync_api import sync_playwright
BG={1:"#ED0A84",2:"#0b0a0a",3:"#C6EA12",4:"#F3F0E9"}
MASK=set()
S=0.8148
GR={2:';background-image:radial-gradient(ellipse 55% 28% at 45% 38%,rgba(237,10,132,.22),transparent 70%)'}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    for i in range(1,5):
        h=open(f's{i}.html').read()
        css=re.search(r'<style>(.*)</style>',h,re.S).group(1)
        body=re.search(r'<body([^>]*)>(.*)</body>',h,re.S)
        battr,inner=body.group(1),body.group(2)
        st=re.search(r'style="([^"]*)"',battr).group(1)
        inner=inner.replace('<div class="grain"></div>','')
        st=re.sub(r'background:[^;]*;?','',st)
        mask='-webkit-mask-image:linear-gradient(to bottom,#000 86%,transparent);mask-image:linear-gradient(to bottom,#000 86%,transparent);' if i in MASK else ''
        if i==2: inner=inner.replace('<div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 50% at 80% 30%,rgba(237,10,132,.28),transparent 70%)"></div>','')
        css2=css.replace('body{width:1080px;height:1350px;','body{width:1080px;height:1920px;')
        page=f'''<!doctype html><html><head><meta charset="utf8"><style>{css2}
.wrap .ph{{-webkit-mask-image:linear-gradient(to bottom,#000 52%,transparent 70%);mask-image:linear-gradient(to bottom,#000 52%,transparent 70%)}}
.wrap{{position:absolute;left:40px;top:350px;width:1080px;height:1350px;transform:scale({S});transform-origin:0 0;overflow:hidden;{st};{mask}}}</style></head>
<body style="background:{BG[i]}{GR.get(i,"")}"><div class="wrap">{inner}</div><div class="grain"></div></body></html>'''
        open(f't{i}.html','w').write(page)
        pg.goto(f'file:///home/claude/ad2/t{i}.html'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'redes_tt_0{i}.jpg',type='jpeg',quality=93)
    b.close()
# QA: nada distinto al fondo en zonas tapadas
import numpy as np
from PIL import Image
ok=True
for i in range(1,5):
    a=np.asarray(Image.open(f'redes_tt_0{i}.jpg').convert('RGB')).astype(int)
    bg=np.array([int(BG[i][k:k+2],16) for k in (1,3,5)])
    d=np.abs(a-bg).sum(axis=2)>90
    z={'arriba':d[:345].sum(),'abajo':d[1460:].sum(),'derecha':d[345:1460,924:].sum()}
    print(i,z); ok=ok and not any(z.values())
print('QA OK' if ok else 'QA FALLÓ')
