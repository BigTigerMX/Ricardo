# -*- coding: utf-8 -*-
"""Currículum en PDF, una página, español e inglés.

Para quién se escribe: dos lectores a la vez.
 · El filtro automático (ATS): una sola columna, encabezados con las palabras
   de siempre, texto real en orden de lectura, fechas junto a su puesto, nada
   de tablas ni cajas de texto. La comprobación va al final del script y no es
   de fe: se extrae el texto del PDF y se revisa que cada puesto traiga sus
   fechas pegadas y que no haya caracteres de uso privado.
 · La persona: jerarquía clara, aire, y la misma paleta del sitio —gris oscuro
   y azul oscuro— para que se reconozca como la misma marca.

Tipografía: instancias ESTÁTICAS (ver hacer_fuentes.py). Con la fuente variable
Chromium incrusta Type 3, que es lo que un lector automático extrae peor.

El tamaño se ajusta solo: se prueba de mayor a menor hasta que cabe en una
página exacta, en vez de fijarlo a ojo y descubrir después que se fue a dos.
"""
import html, pathlib, re, subprocess, sys
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from contenido import DATOS, ES, EN   # noqa: E402
import json
G = json.loads((AQUI / "prueba/glifos.json").read_text())["romana"]
F = AQUI / "fuentes" / "pdf"
TRAB = AQUI / "cv-trabajo"; SALE = AQUI / "sitio" / "cv"
e = html.escape

CSS = """
@font-face { font-family: "Bodoni Moda CV"; src: url("file://%(F)s/BodoniModaCV-Bold.ttf"); font-weight: 700; }
@font-face { font-family: "Bodoni Moda CV"; src: url("file://%(F)s/BodoniModaCV-Medium.ttf"); font-weight: 500; }
@font-face { font-family: "Plex Sans CV"; src: url("file://%(F)s/PlexSansCV-Regular.ttf"); font-weight: 400; }
@font-face { font-family: "Plex Sans CV"; src: url("file://%(F)s/PlexSansCV-Medium.ttf"); font-weight: 500; }
@font-face { font-family: "Plex Sans CV"; src: url("file://%(F)s/PlexSansCV-SemiBold.ttf"); font-weight: 600; }
@page { size: 8.5in 11in; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { width: 8.5in; font: 400 calc(9.35pt * var(--k)) / 1.36 "Plex Sans CV", sans-serif; color: #2A2E35; font-feature-settings: "calt" 0, "liga" 0; }
.hoja { width: 8.5in; }
a { color: inherit; text-decoration: none; }

/* cabecera: banda azul oscuro a sangre */
.cab { position: relative; background: #0F1C31; color: #E8EBF0; padding: calc(.44in * var(--k)) .62in calc(.34in * var(--k)); overflow: hidden; }
.cab::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 3pt; background: #2A2E35; }
.mono { position: absolute; right: .5in; top: 50%%; width: 1.1in; transform: translateY(-50%%); }
h1 { font: 700 calc(27pt * var(--k)) / 1.02 "Bodoni Moda CV", serif; letter-spacing: -.012em; color: #FFFFFF; }
.titulo { margin-top: calc(5pt * var(--k)); font-weight: 600; font-size: calc(9.9pt * var(--k)); letter-spacing: .055em; text-transform: uppercase; color: #A9C4EE; }
.contacto { margin-top: calc(9pt * var(--k)); font-size: calc(8.9pt * var(--k)); color: #DCE1E9; max-width: 6.1in; }
.contacto span { white-space: nowrap; }
.cedula { margin-top: calc(3pt * var(--k)); font-size: calc(8.9pt * var(--k)); color: #DCE1E9; }
.cedula b { font-weight: 600; color: #A9C4EE; }
.contacto i { font-style: normal; color: #6F86AA; padding: 0 .42em; }

.cuerpo { padding: calc(.2in * var(--k)) .62in 0; }
h2 { display: flex; align-items: center; gap: 8pt; margin: calc(11.5pt * var(--k)) 0 calc(5pt * var(--k)); font: 600 calc(9.5pt * var(--k)) / 1 "Plex Sans CV", sans-serif; letter-spacing: .06em; text-transform: uppercase; color: #14284A; }
h2::after { content: ""; flex: 1; height: .6pt; background: #B9C0CC; }
.perfil { text-align: left; }
.comp p { margin-bottom: calc(1.6pt * var(--k)); }
.comp b, .idi b { font-weight: 600; color: #14284A; }
.puesto { margin-top: calc(7pt * var(--k)); break-inside: avoid; }
.puesto:first-of-type { margin-top: 0; }
.puesto__cab { display: flex; justify-content: space-between; align-items: baseline; gap: 12pt; }
h3 { font: 600 calc(10.4pt * var(--k)) / 1.25 "Plex Sans CV", sans-serif; color: #16181C; }
h3 span { font-weight: 500; color: #14284A; }
.fechas { flex: none; font-weight: 500; font-size: calc(8.9pt * var(--k)); color: #4A515C; white-space: nowrap; }
ul { list-style: none; margin-top: calc(2pt * var(--k)); }
li { position: relative; padding-left: 10.5pt; margin-top: calc(1.1pt * var(--k)); }
li::before { content: ""; position: absolute; left: 1.5pt; top: .56em; width: 3.4pt; height: 3.4pt; background: #14284A; transform: rotate(45deg); }
.edu p { display: flex; justify-content: space-between; align-items: baseline; gap: 12pt; margin-bottom: calc(1.8pt * var(--k)); }
.edu b { font-weight: 600; color: #16181C; }
.idi span + span::before { content: "   ·   "; color: #8A93A1; white-space: pre; }
"""

def pagina(d, k):
    c = DATOS
    mono = (f'<svg class="mono" viewBox="-60 -330 2570 2180" aria-hidden="true">'
            f'<path d="{G["R"]["d"]}" transform="translate(0 1250) scale(1 -1)" fill="#E8EBF0" fill-opacity=".16"/>'
            f'<path d="{G["M"]["d"]}" transform="translate(760 1750) scale(1 -1)" fill="#8FB1E6" fill-opacity=".26"/></svg>')
    sep = " <i>|</i> "
    contacto = sep.join([
        f'<span><a href="{c["tel_href"]}">{e(c["tel"])}</a></span>',
        f'<span><a href="mailto:{c["correo"]}">{e(c["correo"])}</a></span>',
        f'<span><a href="{c["linkedin_href"]}">{e(c["linkedin"])}</a></span>'])
    comp = "".join(f"<p><b>{e(r)}:</b> {e(v)}</p>" for r, v in d["comp"])
    exp = ""
    for p in d["exp"]:
        puntos = "".join(f"<li>{e(x)}</li>" for x in p["puntos"])
        exp += (f'<div class="puesto"><div class="puesto__cab"><h3>{e(p["puesto"])} <span>| {e(p["empresa"])}</span></h3>'
                f'<p class="fechas">{e(p["fechas"])}</p></div><ul>{puntos}</ul></div>')
    edu = "".join(f'<p><span><b>{e(a)}</b> | {e(b)}</span><span class="fechas">{e(f)}</span></p>' for a, b, f in d["edu"])
    idi = "".join(f"<span><b>{e(a)}:</b> {e(b)}</span>" for a, b in d["idi"])
    return f"""<!doctype html><html lang="{d['lang']}"><head><meta charset="utf-8">
<title>{e(c['nombre'])} — {e(d['titulo'])}</title><meta name="author" content="{e(c['nombre'])}">
<style>:root {{ --k: {k}; }}{CSS % {'F': F}}</style></head><body><div class="hoja">
<header class="cab">{mono}<h1>{e(c['nombre'])}</h1><p class="titulo">{e(d['titulo'])} | {e(d['bajada'])}</p><p class="contacto">{contacto}</p><p class="cedula"><b>{e(d['cedula_r'])}:</b> {c['cedula']}</p></header>
<main class="cuerpo">
<section><h2>{e(d['h_perfil'])}</h2><p class="perfil">{e(d['perfil'])}</p></section>
<section class="comp"><h2>{e(d['h_comp'])}</h2>{comp}</section>
<section><h2>{e(d['h_exp'])}</h2>{exp}</section>
<section class="edu"><h2>{e(d['h_edu'])}</h2>{edu}</section>
<section class="idi"><h2>{e(d['h_idi'])}</h2><p>{idi}</p></section>
</main></div></body></html>"""

def paginas(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1))

def construir(d):
    base = f"cv-luis-ricardo-garrido-mendoza-{d['lang']}"
    h = TRAB / f"{base}.html"; pdf = SALE / f"{base}.pdf"
    # 11 in = 1056 px a 96 ppp. Se busca el mayor tamaño que quepa dejando un margen inferior digno.
    for paso in range(0, 30):
        k = round(1.10 - paso * 0.01, 2)
        h.write_text(pagina(d, k))
        alto = int(subprocess.run(["node", str(AQUI / "pdf.cjs"), str(h), str(pdf), str(TRAB / f"{base}.png")], capture_output=True, text=True).stdout.strip() or 0)
        if alto <= 1056 - 34 and paginas(pdf) == 1: break
    return pdf, k, alto

def comprobar(pdf, d):
    """Lo que leería un ATS: texto extraído en orden, sin maquetación."""
    txt = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, text=True).stdout
    lineas = [l.strip() for l in txt.splitlines() if l.strip()]
    fallas = []
    if any(0xE000 <= ord(ch) <= 0xF8FF for ch in txt): fallas.append("caracteres de uso privado")
    for dato in (DATOS["tel"], DATOS["correo"], DATOS["cedula"], DATOS["nombre"], DATOS["linkedin"], d["titulo"].upper(), d["bajada"].upper()):
        if dato not in txt: fallas.append(f"no se extrae: {dato}")
    # nada puede salirse de la hoja: se compara el ancho de trazo de cada renglón con la página
    cajas = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True).stdout
    fuera = [m for m in re.findall(r'xMax="([\d.]+)"', cajas) if float(m) > 612 - 20]
    if fuera: fallas.append(f"{len(fuera)} palabras tocan o pasan el borde derecho")
    for p in d["exp"]:
        # el puesto y sus fechas deben quedar a lo más a dos renglones de distancia, y antes de su primera viñeta
        try:
            i = next(n for n, l in enumerate(lineas) if p["puesto"] in l)
            j = next(n for n, l in enumerate(lineas) if p["fechas"] in l and n >= i - 1)
            b = next(n for n, l in enumerate(lineas) if p["puntos"][0][:40] in l)
            if not (abs(j - i) <= 2 and j < b + 1): fallas.append(f"fechas lejos de «{p['puesto']}» ({i},{j},{b})")
        except StopIteration: fallas.append(f"no se encontró «{p['puesto']}» o sus fechas")
    orden = [next((n for n, l in enumerate(lineas) if t.upper() in l.upper()), -1) for t in (d["h_perfil"], d["h_comp"], d["h_exp"], d["h_edu"], d["h_idi"])]
    if orden != sorted(orden) or -1 in orden: fallas.append(f"encabezados fuera de orden {orden}")
    fuentes = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout
    tipos = sorted(set(re.findall(r"(Type 3|CID TrueType|TrueType|CID Type 0C|Type 1C?)", fuentes)))
    if "Type 3" in tipos: fallas.append("hay fuentes Type 3")
    return fallas, tipos, len(txt.split())

if __name__ == "__main__":
    for d in (ES, EN):
        pdf, k, alto = construir(d)
        fallas, tipos, palabras = comprobar(pdf, d)
        print(f"{pdf.name}  {pdf.stat().st_size:,} bytes · {paginas(pdf)} pág · escala {k} · alto {alto}/1056 px · {palabras} palabras · fuentes {tipos} · ATS: {'OK' if not fallas else fallas}")
