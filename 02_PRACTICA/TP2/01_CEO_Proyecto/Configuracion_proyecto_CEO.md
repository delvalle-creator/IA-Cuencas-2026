# Proyecto CEO (REVISIÓN) — 8 clases ESA WorldCover, 400 puntos

Objetivo: **contrastar las clases de ESA WorldCover 10 m (2021) contra la
fotointerpretación de campo**. Se fotointerpretan los 400 puntos en CEO con la
misma leyenda de 8 clases ESA (en español); luego se compara la clase ESA de
cada punto con la clase fotointerpretada (matriz de acuerdo / precisión).

## Datos del proyecto
- **Nombre:** `LULC Naposta ESA8 2021 - 400 ptos`
- **Descripción:** Validación de ESA WorldCover 10 m por fotointerpretación.
  Cuenca del Arroyo Napostá Grande (Bahía Blanca).
- **Plataforma:** la misma de tu TP2 (app.collect.earth o la institucional).

## Área de Interés (AOI)
- Subir `00_Area_estudio/AOI_Naposta_Grande_shp.zip`.

## Diseño de parcelas (Plot Design)
- **Distribución espacial:** `CSV` (cargar puntos predefinidos).
- **Archivo:** `01_CEO_Proyecto/plots_naposta_ESA8_400.csv`  (columnas LON, LAT, PLOTID).
- **Forma de parcela:** cuadrada · **Tamaño:** 10 m (coincide con ESA WorldCover).
- **N° de parcelas:** 400 (ya definidas en el CSV).

## Diseño de muestra (Sample Design)
- **Tipo:** `Center` (un punto por parcela).

## Encuesta (Survey Question)
- **Componente:** `Button` / `Select (one)`.
- **Pregunta:** «¿Cuál es la cobertura del suelo en este punto (leyenda ESA)?»
- **Respuestas (8 clases ESA, español):**

| clase_id | Clase (ES) | ESA val | Color |
|---|---|---|---|
| 1 | Cobertura arbórea | 10 | #006400 |
| 2 | Matorral/arbustal | 20 | #ffbb22 |
| 3 | Pastizal/herbáceas | 30 | #ffff4c |
| 4 | Cultivos | 40 | #f096ff |
| 5 | Construido/urbano | 50 | #fa0000 |
| 6 | Suelo desnudo/veg. escasa | 60 | #b4b4b4 |
| 7 | Cuerpos de agua permanentes | 80 | #0064c8 |
| 8 | Humedal herbáceo | 90 | #0096a0 |

> Importante: que la columna de clase fotointerpretada quede como entero (1..8)
> al exportar, para poder cruzarla con la etiqueta ESA (`clase_id`/`esa_val`)
> del archivo `04_Datos_referencia/puntos_naposta_ESA8_GEE.csv` por `PLOTID`.

## Imágenes de apoyo
Activar Bing/Google Satellite y usar el zoom para decidir la clase de cada punto.
