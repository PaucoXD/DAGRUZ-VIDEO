# Diseños Draguz Shop

Una carpeta por personaje. Dentro de cada una:
- `imprimir/`: PNG sin fondo para DTF (300 dpi).
  - `*-playera-negra.png` / `*-sin-negro.png`: solo se quitó el negro puro, para playera negra (menos plasta).
  - `*-contorno.png` / `*-sin-fondo-letras.png`: diseño sólido con contorno, para playeras de color.
  - `*-sin-blanco.png` / `*-sin-fondo.png`: se quitó el blanco del fondo.
- `mockups/`: mockups. Los `*-tormenta.jpg` son el estilo de la marca (nubes y rayos del color del diseño).

`generador-tormenta.py` genera los mockups estilo tormenta.

Colecciones del catálogo (solo mockups, los originales con código ST/DB/TJ están en la PC en Documentos\Draguz Diseños):
- `Tom y Jerry/`, `Dragon Ball/`, `Semitonos/`, `Animales Semitonos/`: `mockups/` en alta y `mockups/web/` para la página.
- `importar-*.json`: archivos para importar al catálogo de la página (`importar-catalogo-draguz.json` = catálogo completo).
