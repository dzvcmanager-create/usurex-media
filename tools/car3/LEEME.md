# Carruseles USUREX (render)

1. `cp -r tools/car3/fonts /home/claude/fonts` (el renderer busca las fuentes en /home/claude/fonts).
2. `python3 tools/car3/render2.py <spec.json> <carpeta_salida> <prefijo>` genera `<prefijo>_ig_01..05.jpg` (1080x1350) y `<prefijo>_tt_01..05.jpg` (1080x1920) y corre `qa.py` (zonas seguras TikTok, número de portada = número de pasos, frases prohibidas). Si dice "QA FALLÓ", acortar textos y volver a renderizar.
3. Tipos de lámina: `cover` (con `chat`), `cover2` (cifra grande `fig`), `step` (con `quote`/`reply` o solo `why`+`foot`), `close`. Resaltado: `[[rosado]]`, `{{lima}}`. Campo opcional `src` para la fuente del dato.
4. Ejemplos: `tools/car3/w1/*.json` y `tools/car3/w1/cta/*.json` (cierre con CTA "Comenta REX").
5. Subir imágenes a `img/car3/<AAAA-MM-DD>/` y usar las URLs raw.githubusercontent.com en Zernio.
