# Renderer de carruseles USUREX (estilo chat, aprobado 27/10/2026)

Uso: `python3 render.py piezas.json out prefijo` -> genera `prefijo_ig_NN.jpg` (1080x1350) y `prefijo_tt_NN.jpg` (1080x1920). Zonas seguras TikTok verificadas: nada bajo y=1460 (caption y barra), nada sobre y=160 (pestañas), nada a la derecha de x=950 entre y=700-1460 (botones). Revisar SIEMPRE con overlay antes de subir.

Fuentes: `npm pack @fontsource/big-shoulders-display @fontsource/courier-prime` en /home/claude/fonts y descomprimir cada .tgz en una carpeta con su nombre (render.py apunta a esas rutas). Inter viene instalada en el sistema.

Tipos de lámina: `cover` (chat + título), `step` (kicker, ghost, title, quote/qtime, why, reply/rlabel o foot), `close` (title, sub, cta, firma).
Resaltado: `[[texto]]` rosado, `{{texto}}` lima. Un JSON de 1 lámina = post simple (sin contador).

Postura de marca (30/10/2026): Billy = "el antigurú". Marketero que no es millonario y va en camino; humor, tips reales, números reales. Nunca inventar datos.

## QA obligatorio (corre solo al final de render.py)
- El número de la portada debe calzar con los pasos/errores del carrusel.
- Frases prohibidas: etiqueta, menciona a, millonario, por ti, voy en camino, sígueme si, comparte con tu.
- Zonas seguras TikTok (1080x1920): nada en y<345 (flecha y música del editor), y>1460, ni x>924 entre 345 y 1460.
- Si el QA falla, no se sube nada.
