# -*- coding: utf-8 -*-
"""Prepara las tipografías: woff2 recortados para la web e instancias
estáticas TTF para el PDF.

Por qué instancias estáticas para el PDF: el motor de PDF de Chromium no
recorta bien las fuentes variables y las incrusta como Type 3 (trazos), que
es justo lo que un lector automático lee peor. Con una instancia fija sale
CID TrueType, que es lo que se comprobó que extrae limpio.
"""
import pathlib, subprocess, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

AQUI = pathlib.Path(__file__).resolve().parent
ORIG = AQUI / "fuentes" / "orig"
WEB = AQUI / "sitio" / "fuentes"; WEB.mkdir(parents=True, exist_ok=True)
PDF = AQUI / "fuentes" / "pdf"; PDF.mkdir(parents=True, exist_ok=True)

# Latín básico + Latin-1 + la puntuación que de verdad se usa en el sitio.
UNICODES = "U+0020-007E,U+00A0-00AC,U+00AE-00FF,U+0131,U+0152-0153,U+2013-2014,U+2018-201A,U+201C-201E,U+2022,U+2026,U+2030,U+2039-203A,U+20AC,U+2116,U+2190-2193,U+2197,U+2212,U+2713"

def recortar(font, destino, woff2=True):
    # Bodoni Moda trae glifos vacíos (espacio, guion blando) sin entrada en
    # gvar y el recortador revienta al buscarlos: se les da una lista vacía.
    if "gvar" in font:
        gv = font["gvar"].variations
        for g in font.getGlyphOrder():
            try: gv[g]
            except KeyError: gv[g] = []
    opts = subset.Options()
    opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
    opts.flavor = "woff2" if woff2 else None
    s = subset.Subsetter(opts); s.populate(unicodes=subset.parse_unicodes(UNICODES)); s.subset(font)
    font.flavor = "woff2" if woff2 else None
    font.save(str(destino)); print(f"{destino.name:38s} {destino.stat().st_size:>8,} bytes")

# ── web: variables (se conserva el eje de peso; Bodoni conserva también opsz)
recortar(TTFont(ORIG / "BodoniModa-VF.ttf"), WEB / "bodoni-moda.woff2")
recortar(TTFont(ORIG / "BodoniModa-Italic-VF.ttf"), WEB / "bodoni-moda-cursiva.woff2")
plex = instancer.instantiateVariableFont(TTFont(ORIG / "IBMPlexSans-VF.ttf"), {"wdth": 100})
recortar(plex, WEB / "plex-sans.woff2")
for w in ("Regular", "Medium"):
    recortar(TTFont(ORIG / f"IBMPlexMono-{w}.ttf"), WEB / f"plex-mono-{w.lower()}.woff2")

# ── pdf: instancias estáticas
def estatica(origen, ejes, nombre, familia, estilo):
    f = instancer.instantiateVariableFont(TTFont(ORIG / origen), ejes)
    for rec in f["name"].names:
        if rec.nameID == 1: rec.string = familia
        elif rec.nameID == 2: rec.string = estilo
        elif rec.nameID == 4: rec.string = f"{familia} {estilo}"
        elif rec.nameID == 6: rec.string = f"{familia}-{estilo}".replace(" ", "")
        elif rec.nameID in (16, 17, 25): rec.string = familia if rec.nameID != 17 else estilo
    recortar(f, PDF / nombre, woff2=False)

estatica("BodoniModa-VF.ttf", {"opsz": 28, "wght": 500}, "BodoniModaCV-Medium.ttf", "Bodoni Moda CV", "Medium")
estatica("BodoniModa-VF.ttf", {"opsz": 28, "wght": 700}, "BodoniModaCV-Bold.ttf", "Bodoni Moda CV", "Bold")
estatica("BodoniModa-Italic-VF.ttf", {"opsz": 28, "wght": 500}, "BodoniModaCV-MediumItalic.ttf", "Bodoni Moda CV", "Medium Italic")
for w, n in ((400, "Regular"), (500, "Medium"), (600, "SemiBold")):
    estatica("IBMPlexSans-VF.ttf", {"wdth": 100, "wght": w}, f"PlexSansCV-{n}.ttf", "Plex Sans CV", n)
estatica("IBMPlexSans-Italic-VF.ttf", {"wdth": 100, "wght": 400}, "PlexSansCV-Italic.ttf", "Plex Sans CV", "Italic")
for w in ("Regular", "Medium"):
    recortar(TTFont(ORIG / f"IBMPlexMono-{w}.ttf"), PDF / f"PlexMonoCV-{w}.ttf", woff2=False)
