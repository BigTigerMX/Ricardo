# -*- coding: utf-8 -*-
"""Versión editable del currículum en Word (.docx), una por idioma.

Calibri y Georgia, no las tipografías del PDF: un Word editable tiene que
abrirse igual en la máquina de cualquiera, y Bodoni Moda o Plex no están
instaladas en ninguna. Con una fuente que falta, Word sustituye, el texto
cambia de ancho y el documento salta a dos páginas.

SIN TABLAS NI CUADROS DE TEXTO. Todo son párrafos en orden de lectura; las
fechas van en el mismo renglón que su puesto con un tabulador derecho, cuyo
tope se CALCULA del ancho útil (carta menos márgenes), no se escribe de memoria.
"""
import pathlib, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

AQUI = pathlib.Path(__file__).resolve().parent
SALE = AQUI / "sitio" / "cv"; SALE.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(AQUI))
from contenido import DATOS, ES, EN   # noqa: E402

MARGEN = 0.62
ANCHO = Inches(8.5 - MARGEN * 2)      # calculado, no recordado
MARINO = RGBColor(0x14, 0x28, 0x4A)
GRAFITO = RGBColor(0x16, 0x18, 0x1C)
CUERPO = RGBColor(0x2A, 0x2E, 0x35)
GRIS = RGBColor(0x4A, 0x51, 0x5C)


def filete(par, grosor=6, color="B9C0CC", espacio=3):
    pPr = par._p.get_or_add_pPr(); bdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", str(grosor)), ("w:space", str(espacio)), ("w:color", color)): b.set(qn(k), v)
    bdr.append(b); pPr.append(bdr)


def tramo(par, texto, tam=10, negrita=False, color=CUERPO, fuente="Calibri", mayus=False, espaciado=None):
    r = par.add_run(texto)
    r.font.size = Pt(tam); r.font.bold = negrita; r.font.color.rgb = color; r.font.name = fuente
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), fuente)
    if mayus: r.font.all_caps = True
    if espaciado is not None:
        sp = OxmlElement("w:spacing"); sp.set(qn("w:val"), str(espaciado)); r._element.get_or_add_rPr().append(sp)
    return r


def p(doc, antes=0, despues=2, interlineado=1.1, estilo=None, sangria=None, junto=False):
    par = doc.add_paragraph(style=estilo) if estilo else doc.add_paragraph()
    f = par.paragraph_format
    f.space_before = Pt(antes); f.space_after = Pt(despues); f.line_spacing = interlineado; f.keep_with_next = junto
    if sangria is not None: f.left_indent = Inches(sangria)
    return par


def encabezado(doc, texto):
    par = p(doc, antes=8, despues=4, junto=True)
    tramo(par, texto, tam=10, negrita=True, color=MARINO, mayus=True, espaciado=12)
    filete(par); return par


def construir(d, destino):
    doc = Document(); s = doc.sections[0]
    s.page_width = Inches(8.5); s.page_height = Inches(11)
    s.top_margin = Inches(0.5); s.bottom_margin = Inches(0.45)
    s.left_margin = s.right_margin = Inches(MARGEN)
    normal = doc.styles["Normal"]; normal.font.name = "Calibri"; normal.font.size = Pt(10)
    normal._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Calibri")
    doc.core_properties.author = DATOS["nombre"]; doc.core_properties.title = f"{DATOS['nombre']} — {d['titulo']}"
    doc.core_properties.language = d["lang"]

    par = p(doc, despues=1, interlineado=1.0); tramo(par, DATOS["nombre"], tam=25, negrita=True, color=MARINO, fuente="Georgia")
    par = p(doc, despues=4); tramo(par, f"{d['titulo']} | {d['bajada']}", tam=10.5, negrita=True, color=GRAFITO, mayus=True, espaciado=10)
    par = p(doc, despues=1); tramo(par, "  |  ".join([DATOS["tel"], DATOS["correo"], DATOS["linkedin"]]), tam=9.8, color=CUERPO)
    par = p(doc, despues=2); tramo(par, f"{d['cedula_r']}: ", tam=9.8, negrita=True, color=MARINO); tramo(par, DATOS["cedula"], tam=9.8)
    filete(par, grosor=18, color="14284A", espacio=6)

    encabezado(doc, d["h_perfil"])
    par = p(doc, despues=2, interlineado=1.12); tramo(par, d["perfil"], tam=10)

    encabezado(doc, d["h_comp"])
    for k, v in d["comp"]:
        par = p(doc, despues=1.5); tramo(par, k + ": ", tam=10, negrita=True, color=MARINO); tramo(par, v, tam=10)

    encabezado(doc, d["h_exp"])
    for i, puesto in enumerate(d["exp"]):
        par = p(doc, antes=5 if i else 0, despues=1, junto=True)
        par.paragraph_format.tab_stops.add_tab_stop(ANCHO, WD_TAB_ALIGNMENT.RIGHT)   # tope = ancho útil
        tramo(par, puesto["puesto"], tam=11, negrita=True, color=GRAFITO)
        tramo(par, " | " + puesto["empresa"], tam=11, color=MARINO)
        tramo(par, "\t" + puesto["fechas"], tam=9.6, color=GRIS)
        for punto in puesto["puntos"]:
            par = p(doc, despues=0.6, interlineado=1.06, estilo="List Bullet", sangria=0.2); tramo(par, punto, tam=10)

    encabezado(doc, d["h_edu"])
    for a, b, f in d["edu"]:
        par = p(doc, despues=1.5)
        par.paragraph_format.tab_stops.add_tab_stop(ANCHO, WD_TAB_ALIGNMENT.RIGHT)
        tramo(par, a, tam=10, negrita=True, color=GRAFITO); tramo(par, " | " + b, tam=10); tramo(par, "\t" + f, tam=9.6, color=GRIS)

    encabezado(doc, d["h_idi"])
    par = p(doc, despues=0)
    for n, (a, b) in enumerate(d["idi"]):
        if n: tramo(par, "   ·   ", tam=10, color=GRIS)
        tramo(par, a + ": ", tam=10, negrita=True, color=MARINO); tramo(par, b, tam=10)
    doc.save(str(destino)); return destino


if __name__ == "__main__":
    for d in (ES, EN):
        f = construir(d, SALE / f"cv-luis-ricardo-garrido-mendoza-{d['lang']}.docx")
        print(f"{f.name}  {f.stat().st_size:,} bytes")
