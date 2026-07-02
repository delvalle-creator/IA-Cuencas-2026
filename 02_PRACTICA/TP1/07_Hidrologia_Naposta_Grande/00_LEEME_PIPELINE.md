# Hidrología — Cuenca del Arroyo Napostá Grande (FABDEM)

**Sistema de coordenadas: WGS 84 / UTM 20S — EPSG:32720** (metros), el utilizado en este curso para Bahía Blanca.
**Red de drenaje: umbral de acumulación de 0,5 km².**

**Qué es esto.** Una sola cuenca —la del Napostá Grande, definida por el vector de la cuenca (polígono `bid = 2`) y recortada sobre el **FABDEM**— con su hidrología completa, **numerada del 00 al 14**. Sin partición en 5 cuencas, sin microcuencas, sin máscara de agua.

**Cómo usarlo en QGIS.** Arrastre los archivos **en orden, del 00 al 13**. Cada capa trae al lado un `.qml` con el mismo nombre: **el estilo se aplica solo** al cargarla.

> **Datos de origen:** FABDEM v1.2 (Hawker et al. 2022, CC BY-NC-SA 4.0). Todas las capas derivadas de esta carpeta heredan la licencia CC BY-NC-SA 4.0. Ver `NOTICE.md` en la raíz del repositorio.

---

## Orden de las capas (de la primera a la última)

1. **00_Cuenca_Naposta.shp** — Límite de la cuenca (polígono / máscara). *Contorno negro.*
2. **01_DEM_clip.tif** — FABDEM reproyectado a UTM 20S (30 m) y recortado a la cuenca. *Rampa 0–1235 m.*
3. **02_Hillshade.tif** — Relieve sombreado (315°/45°). *Gris.*
4. **03_DEM_fill.tif** — DEM acondicionado (relleno de depresiones, *priority-flood* de Barnes con épsilon). *Rampa de elevación.*
5. **04_Flow_direction.tif** — Dirección D8 (códigos ESRI 1–128). *Paleta 8 clases.*
6. **05_Flow_accumulation.tif** — Acumulación de flujo. *Rampa azul logarítmica.*
7. **06_Slope.tif** — Pendiente en grados (Horn). *Verde→amarillo→rojo, 0–35°.*
8. **07_Streams_raster.tif** — Red de drenaje ráster (acum. ≥ 0,5 km²). *Azul.*
9. **08_Strahler_raster.tif** — Orden de Strahler ráster. *Paleta azul por orden.*
10. **09_Red_drenaje.shp** — Red de drenaje vectorial (atributos `strahler`, `long_m`). *Graduado por orden de Strahler.*
11. **10_Curvas_nivel.shp** — Curvas de nivel cada 50 m (`indice = 1` en las maestras cada 250 m). *Marrón fino.*
12. **11_Cauce_principal.shp** — Cauce principal / *longest flow path* (114,8 km). *Azul oscuro grueso.*
13. **12_Outlet.shp** — Punto de cierre. *Punto rojo.*
14. **13_Zonas_altimetricas.tif** — Cuenca alta / media / baja por tercios de altitud (1 = Baja ≤123 m, 2 = Media 123–229 m, 3 = Alta >229 m). *Verde / amarillo / marrón.*

> **14_Parametros_morfometricos.csv** — Tabla de parámetros (separador `;`).
> **pipeline_hidrologia_naposta.py** — Script reproducible (genera todo desde FABDEM + vector; ya trae EPSG:32720 y 0,5 km²). Se encuentra en `../03_Scripts_QGIS/`.
> **_control_red_drenaje.png** — Imagen de control de la red.

---

## Parámetros morfométricos

| Parámetro | Valor | Unidad |
|---|---|---|
| Área de la cuenca | 1404,0 | km² |
| Perímetro | 316,6 | km |
| Cota máxima / mínima / media | 1234,8 / 0,5 / 190,7 | m |
| Relieve | 1234,3 | m |
| Pendiente media de la cuenca | 1,88 (3,4 %) | ° |
| Longitud total de cauces | 1539,0 | km |
| **Densidad de drenaje (Dd)** | **1,096** | km/km² |
| **Orden de la cuenca (Strahler)** | **6** | — |
| Longitud del cauce principal (Lcp) | 114,76 | km |
| Pendiente media del cauce principal | 0,94 | % |
| Coef. de compacidad de Gravelius (Kc) | 2,38 | — |
| Factor de forma de Horton (Rf) | 0,107 | — |
| Razón de elongación (Re) | 0,368 | — |
| Tiempo de concentración (Kirpich) | 15,4 | h |
| Tiempo de concentración (Témez) | 26,8 | h |
| Outlet (X, Y) UTM 20S | 559500,9 ; 5712733,7 | m |

**Lectura geomorfológica.** Kc = 2,38, Rf = 0,107 y Re = 0,368 describen una **cuenca marcadamente alargada** (cabeceras en la Sierra de la Ventana a ~1235 m, descarga en el estuario de Bahía Blanca). Con el umbral de 0,5 km² la densidad de drenaje es **1,10 km/km²**, coherente con relieve de llanura y sector serrano en cabeceras.

---

## Notas técnicas

- **CRS = EPSG:32720 (WGS 84 / UTM 20S).** Si lo necesita en POSGAR 2007 Faja 4, cambie `DST_CRS` a `EPSG:5346` en el script y vuelva a ejecutar.
- **Umbral = 0,5 km² (556 celdas).** Variable en `THRESH_KM2`.
- **Outlet.** Drena 1244 de los 1404 km²; los ~160 km² restantes son margen costero del polígono que descarga directo al estuario. El outlet principal es el del cauce Napostá.
- **Perímetro y Kc** reflejan la geometría detallada del polígono entregado (multipartes, frente costero). Para un Kc más “de manual”, simplificar el límite.
- **Tc.** Kirpich es para cuencas chicas (en 1400 km² es referencial); Témez (~27 h) es más adecuado a esta escala. Ambos usan la pendiente del cauce principal (0,94 %).
- **Zonas alta/media/baja**: zonificación altitudinal por tercios (percentiles 33 y 66), ~468 km² cada franja. No es subdivisión en cuencas.

## Reproducir
```
pip install rasterio scipy pyshp contourpy
# editar rutas en el bloque CONFIG (ya trae EPSG:32720 y 0,5 km²)
python ../03_Scripts_QGIS/pipeline_hidrologia_naposta.py
```
