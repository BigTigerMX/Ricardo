# Luis Ricardo Garrido Mendoza · Abogado

Sitio personal y currículum. Paleta: gris oscuro (grafito) y azul oscuro (marino), con plata de acento.

## Qué hay

| Ruta | Qué es |
|---|---|
| `sitio/` | El sitio, listo para publicar tal cual (HTML, CSS y JS sin dependencias; fuentes dentro) |
| `sitio/cv/` | Currículum en PDF (español e inglés) y en Word editable |
| `plantilla.html`, `armar.py` | De aquí sale `sitio/index.html`. **Se edita la plantilla, no el index** |
| `contenido.py` | Los textos del currículum, una sola fuente para PDF y Word |
| `hacer_cv.py`, `hacer_docx.py` | Generan los PDF y los Word, y comprueban lo que leería un filtro automático |
| `hacer_fuentes.py`, `glifos.py` | Preparan las tipografías y los trazos del monograma |

## Reglas de este proyecto

- **No se inventa ningún dato.** Todo sale del currículum que entregó Ricardo. Lo que él no dijo, no está.
- El sitio lleva `<meta name="robots" content="noindex">`: tiene su teléfono y su correo, y no debe salir en buscadores hasta que él lo autorice. Quitarlo es borrar ese renglón de `plantilla.html`.
- Movimiento sólo con `transform` y `clip-path`; nunca se anima la opacidad de un texto. Con `prefers-reduced-motion` o sin JavaScript el contenido se ve completo y quieto.
- Los encabezados del PDF llevan poco espaciado entre letras a propósito: con más, el extractor de texto lee «E D U C A T I O N» y un filtro automático no reconoce la sección. Está medido en `hacer_cv.py`.

## Reconstruir

```bash
python3 hacer_fuentes.py && python3 glifos.py   # sólo si cambian las tipografías
python3 hacer_cv.py && python3 hacer_docx.py     # currículums
node og.cjs                                      # tarjeta para compartir
python3 armar.py --unico                         # sitio/index.html + versión de un solo archivo
```

Tipografías: Bodoni Moda e IBM Plex, ambas con licencia SIL Open Font (ver `sitio/fuentes/`).
