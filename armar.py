# -*- coding: utf-8 -*-
"""Arma el sitio: mete los trazos del monograma en la plantilla, escribe el
favicon y, con --unico, una versión de un solo archivo (CSS, JS y fuentes
dentro) para compartir sin servidor."""
import base64, json, pathlib, re, sys
AQUI = pathlib.Path(__file__).resolve().parent
SITIO = AQUI / "sitio"
G = json.loads((AQUI / "prueba/glifos.json").read_text())["romana"]
OG = "https://bigtigermx.github.io/Ricardo/tarjeta-social.jpg"

html = (AQUI / "plantilla.html").read_text()
html = html.replace("{{R}}", G["R"]["d"]).replace("{{M}}", G["M"]["d"]).replace("{{OG}}", OG)
# huella del contenido en el enlace: un navegador que ya visitó el sitio guarda estilo.css y motor.js
# hasta diez minutos (GitHub Pages), y vería la página nueva con el movimiento viejo
import hashlib
huella = lambda f: hashlib.sha1((SITIO / f).read_bytes()).hexdigest()[:8]
(SITIO / "index.html").write_text(html.replace('href="estilo.css"', f'href="estilo.css?v={huella("estilo.css")}"')
                                      .replace('src="motor.js"', f'src="motor.js?v={huella("motor.js")}"'))

(SITIO / "favicon.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-260 -430 2970 2380">'
    '<rect x="-260" y="-430" width="2970" height="2380" rx="300" fill="#16181C"/>'
    f'<path d="{G["R"]["d"]}" transform="translate(0 1250) scale(1 -1)" fill="#E8EBF0"/>'
    f'<path d="{G["M"]["d"]}" transform="translate(760 1750) scale(1 -1)" fill="#8FB1E6"/></svg>')

if "--unico" in sys.argv:
    css = (SITIO / "estilo.css").read_text()
    def fuente(m):
        datos = base64.b64encode((SITIO / m.group(1)).read_bytes()).decode()
        return f'url("data:font/woff2;base64,{datos}")'
    css = re.sub(r'url\("(fuentes/[^"]+)"\)', fuente, css)
    js = (SITIO / "motor.js").read_text()
    u = html.replace('<link rel="stylesheet" href="estilo.css">', f"<style>\n{css}\n</style>")
    u = re.sub(r'<link rel="preload"[^>]+>\n', "", u)
    u = u.replace('<link rel="icon" href="favicon.svg" type="image/svg+xml">', "")
    u = u.replace('<script src="motor.js" defer></script>', f"<script>\n{js}\n</script>")
    # los currículums van dentro del archivo: sin esto los botones de descarga apuntarían a una carpeta que no viaja con él
    MIME = {".pdf": "application/pdf", ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
    for f in sorted((SITIO / "cv").iterdir()):
        if f.suffix not in MIME: continue
        uri = f"data:{MIME[f.suffix]};base64,{base64.b64encode(f.read_bytes()).decode()}"
        u = u.replace(f'data-en-href="cv/{f.name}" download', f'data-en-href="{uri}" download')
        u = u.replace(f'href="cv/{f.name}" download', f'href="{uri}" download="{f.name}"')
        u = u.replace(f'href="cv/{f.name}" data-en-href=', f'href="{uri}" data-en-href=')
    b = "cv-luis-ricardo-garrido-mendoza"
    v = 'download><span data-en="Download résumé">'
    assert u.count(v) == 1
    u = u.replace(v, f'download="{b}-es.pdf" data-en-download="{b}-en.pdf"><span data-en="Download résumé">')
    assert 'href="cv/' not in u, "quedó un enlace a cv/ sin incrustar"
    destino = AQUI / "sitio-ricardo-mendoza-un-archivo.html"
    destino.write_text(u); print(destino.name, f"{destino.stat().st_size:,} bytes")
print("index.html", f"{(SITIO / 'index.html').stat().st_size:,} bytes")
