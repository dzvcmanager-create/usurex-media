import sys
from playwright.sync_api import sync_playwright
F="/home/claude/fonts"
CSS=f"""
@font-face{{font-family:BS;font-weight:900;src:url(file://{F}/fontsource-big-shoulders-display-5.3.0/files/big-shoulders-display-latin-900-normal.woff2)}}
@font-face{{font-family:BS;font-weight:800;src:url(file://{F}/fontsource-big-shoulders-display-5.3.0/files/big-shoulders-display-latin-800-normal.woff2)}}
@font-face{{font-family:CP;font-weight:700;src:url(file://{F}/fontsource-courier-prime-5.3.0/files/courier-prime-latin-700-normal.woff2)}}
@font-face{{font-family:AN;src:url(file://{F}/Anton-Regular.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;position:relative;font-family:Inter,sans-serif}}
.grain{{position:absolute;inset:0;opacity:.16;mix-blend-mode:overlay;pointer-events:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");z-index:50}}
.top{{position:absolute;top:56px;left:70px;right:70px;display:flex;justify-content:space-between;font:700 24px CP;letter-spacing:7px;z-index:20}}
.h{{font:900 128px/1.07 BS;text-transform:uppercase;letter-spacing:-1px}}
.blk{{background:#0b0a0a;color:#F3F0E9;padding:0 .07em;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.pk{{background:#ED0A84;color:#fff;padding:0 .07em;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.lm{{background:#C6EA12;color:#0b0a0a;padding:0 .07em}}
/* phone */
.ph{{position:absolute;width:520px;height:1060px;border-radius:70px;background:#0e0d0d;border:12px solid #1d1c1b;box-shadow:0 50px 100px rgba(0,0,0,.55),inset 0 0 0 2px #333;overflow:hidden}}
.ph .notch{{position:absolute;top:16px;left:50%;transform:translateX(-50%);width:150px;height:36px;border-radius:20px;background:#000}}
.ph .bar{{padding:78px 30px 18px;display:flex;justify-content:space-between;align-items:center;color:#F3F0E9;font:700 32px Inter;border-bottom:1px solid #222}}
.ph .bar span{{background:#ED0A84;color:#fff;font:700 22px Inter;border-radius:20px;padding:5px 14px}}
.row{{display:flex;gap:18px;align-items:center;padding:20px 28px;border-bottom:1px solid #1f1e1d;color:#F3F0E9}}
.av{{width:64px;height:64px;border-radius:50%;flex:none}}
.tx{{flex:1;min-width:0}}.n{{font:700 25px Inter}}.m{{font:400 23px Inter;color:#d8d4cb;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.t{{font:400 19px Inter;color:#8f8a80;text-align:right}}.dot{{width:16px;height:16px;border-radius:50%;background:#ED0A84;margin:8px 0 0 auto}}
.chat{{padding:24px 22px;display:flex;flex-direction:column;gap:16px}}
.b{{max-width:380px;padding:16px 20px 10px;border-radius:24px;font:400 25px/1.3 Inter;color:#F3F0E9}}
.b.in{{background:#262524;align-self:flex-start}} .b.out{{background:#1f3b2b;align-self:flex-end}}
.b .tm{{text-align:right;font-size:17px;color:#a9a59c;margin-top:4px}}
.stk{{position:absolute;font:900 64px/1 BS;text-transform:uppercase;padding:16px 26px 12px;z-index:30;box-shadow:8px 8px 0 #0b0a0a}}
.tape{{position:absolute;width:120px;height:34px;background:rgba(243,240,233,.75);z-index:31}}
.cta{{background:#0b0a0a;color:#F3F0E9;border-radius:22px;padding:30px 36px;font:800 50px/1 BS;text-transform:uppercase;display:inline-flex;gap:20px;align-items:center}}
.cta b{{color:#C6EA12}}
"""
def phone_list(x,y,rot,rows):
    r="".join(f'<div class="row"><div class="av" style="background:{c}"></div><div class="tx"><div class="n">{n}</div><div class="m">{m}</div></div><div><div class="t">{t}</div><div class="dot"></div></div></div>' for n,m,t,c in rows)
    return f'<div class="ph" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"><div class="notch"></div><div class="bar">Mensajes <span>14 sin leer</span></div>{r}</div>'
ROWS=[("Camila","¿Tienen stock en talla M?","23:47","#c86b98"),("Javiera","Hola, ¿hacen envíos?","23:12","#6b8ec8"),("Pedro","¿Cuánto sale?","22:58","#8ec86b"),("Fernanda","¿Siguen abiertos?","22:31","#c8a96b"),("Matías","Quiero cotizar 3","21:40","#9b6bc8"),("Daniela","¿Hola? 😕","20:05","#6bc8b8"),("Ignacio","¿Aceptan transferencia?","19:22","#c86b6b")]

def top(n,dark=True):
    c="#0b0a0a" if dark else "#F3F0E9"
    return f'<div class="top" style="color:{c}"><span>■ USUREX</span><span>0{n} / 04</span></div>'

S=[]
# 1 PROBLEMA — rosado
S.append(f'''<body style="background:#ED0A84">{top(1)}
<div class="h" style="position:absolute;left:70px;top:130px;width:900px;color:#0b0a0a">Anoche te escribieron <span class="blk">14 clientes.</span></div>
{phone_list(470,580,7,ROWS)}
<div class="stk" style="left:90px;top:610px;background:#C6EA12;color:#0b0a0a;transform:rotate(-7deg)">En visto 👀</div>
<div class="tape" style="left:120px;top:596px;transform:rotate(-20deg)"></div>
<div style="position:absolute;left:70px;top:860px;width:380px;font:800 54px/1.05 BS;text-transform:uppercase;color:#0b0a0a">¿A cuántos les respondiste?</div>
<div style="position:absolute;left:70px;bottom:70px;font:700 24px CP;letter-spacing:6px;color:#0b0a0a">DESLIZA &nbsp;→</div>
<div class="grain"></div></body>''')

# 2 DOLOR — negro
def loss(t,y,x,rot,name):
    return f'''<div style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg)"><div class="b in" style="font-size:30px;padding:20px 26px 12px;max-width:520px;box-shadow:0 20px 40px rgba(0,0,0,.5)">{t}<div class="tm">{name}</div></div>
<div style="position:absolute;left:calc(100% + 18px);top:6px;white-space:nowrap;background:#ED0A84;color:#fff;font:900 46px/1 BS;padding:10px 16px 6px;transform:rotate(8deg);box-shadow:5px 5px 0 #000">−$15.000</div></div>'''
S.append(f'''<body style="background:#0b0a0a;color:#F3F0E9">
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 50% at 80% 30%,rgba(237,10,132,.28),transparent 70%)"></div>
{top(2,False)}
<div class="h" style="position:absolute;left:70px;top:130px;width:940px;font-size:112px">Cada mensaje sin responder es una <span class="pk">venta perdida.</span></div>
{loss("¿Tienen stock en talla M?",560,70,-3,"Camila · 23:47")}
{loss("¿Cuánto sale?",690,150,2,"Pedro · 22:58")}
{loss("Quiero cotizar 3",820,90,-2,"Matías · 21:40")}
<div style="position:absolute;left:70px;top:985px;font:800 54px/1 BS;text-transform:uppercase;color:#a9a59c">14 mensajes × $15.000 =</div>
<div style="position:absolute;left:66px;top:1045px;font:900 190px/1 BS;color:#ED0A84">$210.000</div>
<div style="position:absolute;left:70px;top:1235px;font:800 46px/1 BS;text-transform:uppercase">que se llevó tu competencia.</div>
<div style="position:absolute;right:70px;top:1250px;font:400 20px Inter;color:#8f8a80;text-align:right">Ejemplo con una compra<br>promedio de $15.000.</div>
<div class="grain"></div></body>''')

# 3 SOLUCIÓN — lima
S.append(f'''<body style="background:#C6EA12">{top(3)}
<div class="h" style="position:absolute;left:70px;top:130px;width:960px;color:#0b0a0a;font-size:124px">Nosotros respondemos.<br><span class="blk" style="display:inline-block;margin-top:18px;line-height:1">Tú vendes.</span></div>
<div class="ph" style="left:575px;top:540px;transform:rotate(-5deg)"><div class="notch"></div>
<div class="bar" style="justify-content:flex-start;gap:16px"><div class="av" style="background:#c86b98;width:52px;height:52px"></div>Camila</div>
<div class="chat">
<div class="b in">Hola, ¿tienen stock en talla M?<div class="tm">23:47</div></div>
<div class="b out">¡Hola Camila! Sí, nos queda 🙌 ¿Te la reservo?<div class="tm">23:49 ✓✓</div></div>
<div class="b in">Sí porfa 😍 ¿Cómo pago?<div class="tm">23:50</div></div>
<div class="b out">Te mando los datos y queda lista para mañana 💖<div class="tm">23:51 ✓✓</div></div>
</div></div>
<div class="stk" style="left:430px;top:1210px;background:#ED0A84;color:#fff;transform:rotate(-6deg)">Venta cerrada ✓</div>
<div style="position:absolute;left:70px;top:640px;display:flex;flex-direction:column;gap:18px;width:420px">
<div style="background:#0b0a0a;color:#F3F0E9;font:600 30px/1.2 Inter;padding:20px 24px;border-radius:18px">Respondemos de <b style="color:#C6EA12">lunes a sábado</b></div>
<div style="background:#0b0a0a;color:#F3F0E9;font:600 30px/1.2 Inter;padding:20px 24px;border-radius:18px"><b style="color:#C6EA12">5 historias</b> a la semana</div>
<div style="background:#0b0a0a;color:#F3F0E9;font:600 30px/1.2 Inter;padding:20px 24px;border-radius:18px"><b style="color:#C6EA12">3 reels</b> al mes</div>
</div>
<div class="grain"></div></body>''')

# 4 OFERTA — papel
S.append(f'''<body style="background:#F3F0E9;color:#0b0a0a">{top(4)}
<div style="position:absolute;left:70px;top:150px;font:700 28px CP;letter-spacing:6px;color:#ED0A84">TU EQUIPO DE REDES</div>
<div style="position:absolute;left:62px;top:205px;font:900 240px/.9 BS">$150.000</div>
<div style="position:absolute;left:72px;top:430px;font:600 36px Inter">+ IVA al mes · 1 red social</div>
<div style="position:absolute;left:70px;top:520px;width:940px;font:800 62px/1.02 BS;text-transform:uppercase">Menos de lo que pierdes <span class="pk">en una noche</span> sin responder.</div>
<div style="position:absolute;left:70px;top:740px;display:flex;gap:22px">
<div style="border:4px solid #0b0a0a;border-radius:20px;padding:22px 26px;width:455px"><div style="font:900 52px/1 BS;color:#ED0A84">MES 1</div><div style="font:500 28px/1.25 Inter;margin-top:8px">Sin amarre. Si no te convence, cancelas.</div></div>
<div style="border:4px solid #0b0a0a;border-radius:20px;padding:22px 26px;width:455px"><div style="font:900 52px/1 BS;color:#ED0A84">72 H</div><div style="font:500 28px/1.25 Inter;margin-top:8px">Tu perfil renovado y listo para vender.</div></div>
</div>
<div class="stk" style="left:640px;top:960px;background:#C6EA12;color:#0b0a0a;transform:rotate(5deg);font-size:54px">Solo 3 cupos</div>
<div style="position:absolute;left:70px;top:1030px"><div class="cta">Escríbenos <b>REDES</b> por interno →</div></div>
<div style="position:absolute;left:70px;bottom:62px;right:70px;display:flex;justify-content:space-between;align-items:flex-end;border-top:3px solid #0b0a0a;padding-top:20px"><div style="font:900 56px/1 BS;color:#ED0A84">USUREX</div><div style="font:700 22px CP;letter-spacing:5px">TU EQUIPO DE REDES</div></div>
<div class="grain"></div></body>''')

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for i,s in enumerate(S,1):
        open(f's{i}.html','w').write(f'<!doctype html><html><head><meta charset="utf8"><style>{CSS}</style></head>{s}</html>')
        pg.goto(f'file:///home/claude/ad2/s{i}.html'); pg.wait_for_timeout(400)
        pg.screenshot(path=f'redes_ig_0{i}.jpg',type='jpeg',quality=93)
    b.close()
