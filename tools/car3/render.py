"""Renderer USUREX car3: chat de WhatsApp + palabra clave destacada. Uso: python3 render.py slides.json outdir prefix"""
import json, sys, html, pathlib
from playwright.sync_api import sync_playwright

F = "/home/claude/fonts"
FONTS = f"""
@font-face{{font-family:BS;font-weight:800;src:url(file://{F}/fontsource-big-shoulders-display-5.3.0/files/big-shoulders-display-latin-800-normal.woff2)}}
@font-face{{font-family:BS;font-weight:900;src:url(file://{F}/fontsource-big-shoulders-display-5.3.0/files/big-shoulders-display-latin-900-normal.woff2)}}
@font-face{{font-family:CP;font-weight:700;src:url(file://{F}/fontsource-courier-prime-5.3.0/files/courier-prime-latin-700-normal.woff2)}}
"""

def hl(s):
    """[[texto]] = rosado, {{texto}} = lima."""
    s = html.escape(s)
    s = s.replace("[[", '<mark class="p">').replace("]]", "</mark>")
    s = s.replace("{{", '<mark class="l">').replace("}}", "</mark>")
    return s

def bubble(b):
    cls = "in" if b.get("in") else "out"
    ticks = "" if b.get("in") else ' <span class="tk">✓✓</span>'
    return f'<div class="bub {cls}"><div>{hl(b["t"])}</div><div class="tm">{html.escape(b.get("time",""))}{ticks}</div></div>'

def slide(s, i, n, fmt):
    tt = fmt == "tt"
    W, H = 1080, (1920 if tt else 1350)
    padT, padB, padR = (230, 430, 170) if tt else (80, 70, 90)
    glow = s.get("glow", "pink")
    g = {"pink": "rgba(237,10,132,.30)", "wine": "rgba(109,16,48,.55)", "lime": "rgba(198,234,18,.22)"}[glow]
    gpos = s.get("gpos", "85% 8%")
    ghost = f'<div class="ghost">{html.escape(s["ghost"])}</div>' if s.get("ghost") else ""
    kick = f'<div class="kick {s.get("kcol","p")}">{html.escape(s["kicker"])}</div>' if s.get("kicker") else ""
    body = ""
    if s["type"] == "cover":
        body = f'''<div class="chat">{"".join(bubble(b) for b in s["chat"])}</div>
        <div class="bottom">{kick}<h1 class="big">{hl(s["title"])}</h1>
        <p class="sub">{hl(s["sub"])}</p><div class="swipe">DESLIZA &nbsp;&nbsp; →</div></div>'''
    elif s["type"] == "step":
        quote = f'<div class="bub in q"><div>{hl(s["quote"])}</div><div class="tm">{html.escape(s.get("qtime","cliente"))}</div></div>' if s.get("quote") else ""
        why = f'<p class="why">{hl(s["why"])}</p>' if s.get("why") else ""
        reply = ""
        if s.get("reply"):
            reply = f'<div class="lab">{html.escape(s.get("rlabel","RESPONDE ASÍ:"))}</div>{bubble({"t": s["reply"], "time": s.get("rtime","11:15")})}'
        foot = f'<p class="foot">{hl(s["foot"])}</p>' if s.get("foot") else ""
        body = f'{kick}{ghost}<h2>{hl(s["title"])}</h2>{quote}{why}<div class="spacer"></div>{reply}{foot}' if reply else f'<div class="spacer"></div>{kick}{ghost}<h2>{hl(s["title"])}</h2>{why}{foot.replace("class=\"foot\"","class=\"foot punch\"")}<div class="spacer" style="flex:1.4"></div>'
    elif s["type"] == "close":
        body = f'''{kick}<h2 class="close">{hl(s["title"])}</h2><p class="sub2">{hl(s["sub"])}</p>
        <div class="spacer"></div>{('<div class="cta">'+hl(s["cta"])+'</div>') if s.get("cta") else ""}
        <div class="sig">— BILLY · USUREX</div><div class="mk">MARKETING PARA NO CAGARLA</div>'''
    cover_ghost = f'<div class="cghost">{html.escape(s["cghost"])}</div>' if s.get("cghost") else ""
    return f'''<!doctype html><html><head><meta charset="utf8"><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:#0b0a0a;font-family:Inter,sans-serif;color:#F3F0E9;position:relative}}
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse 75% 55% at {gpos},{g},transparent 70%),radial-gradient(ellipse 60% 40% at 10% 100%,rgba(109,16,48,.35),transparent 70%),linear-gradient(180deg,#0f0d0d,#070606)}}
.grain{{position:absolute;inset:0;opacity:.18;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
.wrap{{position:absolute;inset:{padT}px {padR}px {padB}px 90px;display:flex;flex-direction:column}}
.top{{position:absolute;top:{padT-0}px;left:90px;right:{padR}px;display:flex;justify-content:space-between;font:700 24px CP,monospace;letter-spacing:7px}}
.top .b{{color:#ED0A84}} .top .b:before{{content:"■";margin-right:18px}}
.inner{{margin-top:80px;flex:1;display:flex;flex-direction:column;position:relative}}
mark{{color:inherit;padding:0 .08em;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
mark.p{{background:#ED0A84;color:#fff}} mark.l{{background:#C6EA12;color:#0b0a0a}}
.kick{{font:700 27px CP,monospace;letter-spacing:7px;margin-bottom:22px;text-transform:uppercase}}
.kick.p{{color:#ED0A84}} .kick.l{{color:#C6EA12}} .kick.g{{color:#8f8a80}}
h1.big{{font:900 {122 if not tt else 132}px/1.04 BS,sans-serif;text-transform:uppercase;letter-spacing:-1px}}
h2{{font:900 {104 if not tt else 100}px/0.98 BS,sans-serif;text-transform:uppercase;position:relative;z-index:2;margin-bottom:34px}}
h2.close{{font-size:{118 if not tt else 112}px;line-height:1.04}}
.ghost{{font:900 250px/.8 BS,sans-serif;color:rgba(237,10,132,.20);margin:0 0 -95px -6px;position:relative;z-index:1}}
.cghost{{position:absolute;left:-40px;bottom:{170 if not tt else 420}px;font:900 760px/1 BS,sans-serif;color:rgba(109,16,48,.45);transform:skewX(-8deg)}}
.chat{{display:flex;flex-direction:column;gap:26px;margin-top:10px}} .chat .bub{{font-size:37px;padding:22px 30px 14px}}
.bub{{max-width:780px;padding:26px 32px 18px;border-radius:30px;font:400 40px/1.3 Inter,sans-serif;box-shadow:0 18px 40px rgba(0,0,0,.45)}}
.bub.out{{background:#1f3b2b;align-self:flex-end}}
.bub.in{{background:#262524;align-self:flex-start}}
.step-wrap .bub.out,.bub.out.full{{align-self:stretch;max-width:none}}
.bub .tm{{text-align:right;font-size:26px;color:#a9a59c;margin-top:6px}} .tk{{color:#a9a59c;margin-left:10px;letter-spacing:-6px}}
.bub.q{{align-self:flex-start;margin:0 0 6px;font-size:42px;background:#262524;max-width:860px}}
.bottom{{margin-top:auto}} .sub{{font:500 40px/1.3 Inter;margin-top:26px;color:#e9e5dc}}
.swipe{{font:700 26px CP,monospace;letter-spacing:7px;margin-top:30px}}
.why{{font:400 42px/1.38 Inter;color:#d8d4cb;margin-top:28px;max-width:880px}}
.spacer{{flex:1}} .punch{{border-left:6px solid #C6EA12;padding-left:28px;font-weight:600;color:#F3F0E9;margin-top:50px}}
.lab{{text-transform:uppercase;font:700 25px CP,monospace;letter-spacing:7px;color:#8f8a80;margin-bottom:24px}}
.inner > .bub.out{{align-self:stretch;max-width:none}}
.foot{{font:400 40px/1.35 Inter;color:#e9e5dc;margin-top:40px}}
.sub2{{font:400 46px/1.35 Inter;color:#e9e5dc;margin-top:10px;max-width:880px}}
.cta{{font:600 37px/1.35 Inter;border:3px solid #C6EA12;border-radius:20px;padding:28px 32px;margin-bottom:60px}}
.sig{{font:900 80px/1 BS,sans-serif;color:#ED0A84}}
.mk{{font:700 25px CP,monospace;letter-spacing:7px;margin-top:22px}}
</style></head><body><div class="bg"></div>{cover_ghost}<div class="grain"></div>
<div class="top"><span class="b">USUREX</span><span>{(f"{i:02d} / {n:02d}" if n > 1 else "")}</span></div>
<div class="wrap"><div class="inner">{body}</div></div></body></html>'''

def main():
    spec = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]).resolve(); pre = sys.argv[3]
    out.mkdir(parents=True, exist_ok=True)
    n = len(spec)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for fmt, H in (("ig", 1350), ("tt", 1920)):
            pg = b.new_page(viewport={"width": 1080, "height": H})
            for i, s in enumerate(spec, 1):
                f = out / f"{pre}_{fmt}_{i:02d}.html"
                f.write_text(slide(s, i, n, fmt))
                pg.goto(f"file://{f}"); pg.wait_for_timeout(250)
                pg.screenshot(path=str(out / f"{pre}_{fmt}_{i:02d}.jpg"), type="jpeg", quality=92)
        b.close()

main()
