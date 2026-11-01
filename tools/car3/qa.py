"""Control obligatorio antes de subir. Si falla, NO se sube. Uso: python3 qa.py slides.json outdir prefix"""
import json, re, sys, glob
import numpy as np
from PIL import Image
spec = json.load(open(sys.argv[1])); out, pre = sys.argv[2], sys.argv[3]
err = []
# 1. el número de la portada debe calzar con lo que trae el carrusel
for s in spec[:1]:
    m = re.search(r'\b(\d+)\b', s.get("title", ""))
    if m:
        n = int(m.group(1))
        steps = sum(1 for x in spec if x["type"] == "step")
        items = len(s.get("items", [])) if s["type"] == "steps" else steps
        if n != items: err.append(f"Portada dice {n} y el contenido trae {items}")
# 2. frases prohibidas (relleno, chanterío, CTA que nadie pesca)
BAN = ["etiqueta", "menciona a", "millonario", "por ti", "voy en camino", "sígueme si", "comparte con tu"]
txt = json.dumps(spec, ensure_ascii=False).lower()
for b in BAN:
    if b in txt: err.append(f"Frase prohibida: '{b}'")
# 3. zonas seguras TikTok (arriba flecha/música, abajo textos, derecha íconos)
for f in sorted(glob.glob(f"{out}/{pre}_tt_*.jpg")):
    a = np.asarray(Image.open(f).convert("L")).astype(int)
    z = {"arriba": a[:345], "abajo": a[1460:], "derecha": a[345:1460, 924:]}
    for k, r in z.items():
        if (r > 150).sum(): err.append(f"{f.split('/')[-1]}: contenido en zona {k}")
print("\n".join(err) if err else "QA OK"); sys.exit(1 if err else 0)
