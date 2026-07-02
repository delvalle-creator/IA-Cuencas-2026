# Área de estudio — vector del AOI y recorte raster ESA WorldCover

Esta carpeta contiene la definición del **área de estudio** del TP2: la cuenca del
**Arroyo Napostá Grande** (Bahía Blanca, Argentina). El área de estudio se compone de
**dos productos**:

1. **El vector del AOI** (límite de la cuenca), que ya está aquí.
2. **El recorte raster de ESA WorldCover 2021 (10 m)** sobre ese AOI, que usted genera
   una vez (ver más abajo) y guarda en esta misma carpeta como
   `ESA8_Naposta_2021.tif`.

Aunque después el raster se vuelve a recortar dentro de GEE (para las estadísticas y el
muestreo) y nunca se sube a CEO, **el recorte raster forma parte del área de estudio** y
por eso vive junto al vector.

---

## 1. El vector del AOI (ya incluido)

| Archivo | Para qué sirve |
|---|---|
| `AOI_Naposta_Grande_shp.zip` | Subir a **GEE** como *asset* (NEW → Shape files) y a **CEO**. |
| `AOI_Naposta_Grande.shp` (+ `.dbf .shx .prj .cpg`) | El shapefile descomprimido (QGIS/ArcGIS). |
| `AOI_Naposta_Grande.geojson` | El mismo límite en GeoJSON (EPSG:4326). |

Datos del AOI: 1 polígono, EPSG:4326, extensión lon/lat
−62,343 / −38,795 a −61,947 / −38,084; **área ≈ 1.404 km²** (UTM 20S). El AOI cae
entero dentro de un solo tile ESA WorldCover (**S39W063**).

---

## 2. El recorte raster ESA WorldCover (`ESA8_Naposta_2021.tif`) — cómo obtenerlo

El recorte **no se entrega como archivo** porque el insumo original de ESA pesa cientos
de MB; usted lo produce una sola vez por **una de estas dos vías** (cualquiera sirve) y
guarda el resultado en esta carpeta.

### Vía A — En Google Earth Engine (recomendada, sin instalar nada)

1. Ejecute `03_Scripts_GEE/10_ESA_recorte_estadisticas.js` (reemplazando `SU_USUARIO`
   por su usuario de Earth Engine). Recorta ESA WorldCover 2021 al AOI, la traduce a las
   **8 clases en español** y calcula las áreas.
2. En la pestaña **Tasks**, presione **Run** en la tarea de exportación
   `ESA8_Naposta_2021`. El GeoTIFF queda en su **Google Drive** (carpeta `TP2_LULC`).
3. Descárguelo y **guárdelo en esta carpeta** como `ESA8_Naposta_2021.tif`.

> Este script ya fue verificado: carga ESA, la remapea a 8 clases, recorta al AOI y
> calcula el área por clase (8 grupos) sin errores.

### Vía B — En su computadora, sin GEE (carpeta `Recorte_raster_ESA/`)

Si prefiere trabajar localmente (QGIS / Python), la subcarpeta **`Recorte_raster_ESA/`**
deja el recorte automatizado:

```bash
cd Recorte_raster_ESA
python -m venv .venv
.venv\Scripts\activate        # en Windows
pip install geopandas rasterio requests shapely pyproj numpy
python clip_esa_worldcover.py --aoi ../AOI_Naposta_Grande_shp.zip --out outputs
```

El script descarga el tile oficial `S39W063`, recorta por el AOI, reproyecta a UTM 20S a
10 m y calcula áreas por clase. Genera, en `Recorte_raster_ESA/outputs/`:

- `..._clip_EPSG4326.tif` (CRS original de ESA)
- `..._clip_EPSG32720_10m.tif` (UTM 20S, 10 m — el que conviene para medir áreas)
- `..._area_stats.csv` y `.json`

Renombre el GeoTIFF UTM a `ESA8_Naposta_2021.tif` y muévalo a esta carpeta. Para ver el
raster con los colores correctos en QGIS, aplique el estilo `worldcover_qgis.qml`.

Contenido de `Recorte_raster_ESA/`: `clip_esa_worldcover.py` (script), `run_clip.sh`,
`worldcover_legend.csv` (tabla de clases), `worldcover_qgis.qml` (estilo QGIS),
`ESA_WorldCover_tile_S39W063.geojson` (polígono del tile), `manifest.json` (metadatos).

---

## Las 8 clases del recorte (español)

| clase_id | Clase | Valor ESA | Color |
|---:|---|---:|---|
| 1 | Cobertura arbórea | 10 | `#006400` |
| 2 | Matorral / arbustal | 20 | `#ffbb22` |
| 3 | Pastizal / herbáceas | 30 | `#ffff4c` |
| 4 | Cultivos | 40 | `#f096ff` |
| 5 | Construido / urbano | 50 | `#fa0000` |
| 6 | Suelo desnudo / veg. escasa | 60 | `#b4b4b4` |
| 7 | Cuerpos de agua permanentes | 80 | `#0064c8` |
| 8 | Humedal herbáceo | 90 | `#0096a0` |

> ESA WorldCover © ESA / contribuyentes (CC BY 4.0).
> Cita: Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200.* DOI: 10.5281/zenodo.7254221.
