# Saca los contornos de R y M de Bodoni Moda como trazados SVG, para poder
# construir el monograma con trazos reales (y animar su dibujo), no con texto.
import json, pathlib, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
AQUI = pathlib.Path(__file__).resolve().parent
def sacar(archivo, ejes, letras):
    f = instancer.instantiateVariableFont(TTFont(AQUI / "fuentes/orig" / archivo), ejes)
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); out = {"upm": f["head"].unitsPerEm, "asc": f["OS/2"].sCapHeight}
    for ch in letras:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs, ntos=lambda v: str(round(v, 1))); gs[g].draw(pen)
        bp = BoundsPen(gs); gs[g].draw(bp)
        out[ch] = {"d": pen.getCommands(), "adv": gs[g].width, "bounds": bp.bounds}
    return out
datos = {
  "romana": sacar("BodoniModa-VF.ttf", {"opsz": 96, "wght": 500}, "RM"),
  "romana_fina": sacar("BodoniModa-VF.ttf", {"opsz": 96, "wght": 400}, "RM"),
  "cursiva": sacar("BodoniModa-Italic-VF.ttf", {"opsz": 96, "wght": 500}, "RM"),
}
(AQUI / "prueba/glifos.json").write_text(json.dumps(datos))
for k, v in datos.items():
    print(k, v["upm"], v["asc"], {c: (v[c]["adv"], v[c]["bounds"], len(v[c]["d"])) for c in "RM"})
