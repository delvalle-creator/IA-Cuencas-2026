# Inteligencia Artificial aplicada al Manejo de Cuencas Hidrográficas e Hidrológicas

**Curso de Posgrado** · Departamento de Geografía y Turismo, Universidad Nacional del Sur (UNS)
Bahía Blanca, Argentina · 18 al 26 de junio de 2026

**Docente:** Héctor Francisco del Valle
Centro Regional de Geomática (CeReGeo), FCyT, Universidad Autónoma de Entre Ríos (UADER) ·
Laboratorio de Ecología, Meteorología y Gestión de Fuegos de Vegetación (LEMIV), Facultad de Ingeniería, UNPSJB

---

## Descripción

Materiales teóricos y prácticos para integrar la Inteligencia Artificial al análisis espacial, la teledetección y el modelado hidrológico, con foco en la cuenca del Arroyo Napostá Grande y la inundación de Bahía Blanca del 7 de marzo de 2025. El desarrollo combinó aportes de IA (ChatGPT, Claude y Copilot) con dirección y revisión humana.

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `01_TEORIA/` | Clases teóricas (PDF) y ética científica en el uso de IA |
| `02_PRACTICA/01_GUIA_TP/` | Guía de trabajos prácticos y cuestionario |
| `02_PRACTICA/02_TUTORIALES/` | Tutoriales paso a paso de las prácticas |
| `02_PRACTICA/TP1/` | Metadatos y control de calidad de DTM (FABDEM, MDE-Ar, TanDEM-X EDEM) + pipeline hidrológico en QGIS/Python |
| `02_PRACTICA/TP2/` | Validación de ESA WorldCover por fotointerpretación (Collect Earth Online + Google Earth Engine) |
| `02_PRACTICA/TP3/` | Superresolución de Sentinel-2 con S2DR4 (Google Colab) |
| `02_PRACTICA/TP4/` | SAR Sentinel-1 y ópticos Sentinel-2 en SNAP (detección de inundación) |
| `02_PRACTICA/TP5/` | Simulación de inundación: HEC-RAS 2D *rain-on-grid*, HAND y Orange Data Mining |

Cada TP incluye sus LEEME/README, prompts de IA, scripts y datos de referencia. Los prompts están pensados para que el estudiante genere y ejecute los scripts con asistencia de IA.

## Software requerido

QGIS (3.34+), SNAP (ESA), HEC-RAS 6.x con RAS Mapper, Orange Data Mining, Python 3.10+ (ver `02_PRACTICA/TP5/07_SCRIPTS_Y_PROMPTS/requirements.txt`), cuenta de Google Earth Engine y Google Colab, cuenta en Collect Earth Online.

## Datos pesados (no incluidos en el repositorio)

Por los límites de GitHub (100 MB por archivo), estos insumos se distribuyen por separado — ver **Releases** de este repositorio (o el enlace Zenodo/Drive indicado por la cátedra):

| Archivo | Tamaño | Uso |
|---|---|---|
| `S2C_MSIL2A_20260430T140051_N0512_R067_T20HNC_20260430T191458.SAFE.zip` | 1,1 GB | TP3 — insumo Sentinel-2. Alternativa: descargarlo directamente del [Copernicus Data Space](https://dataspace.copernicus.eu/) con ese ID de producto |
| `TP3_S2DR4_Resultados.zip` | 423 MB | TP3 — resultados de referencia |
| `SNAP_RGB_READY_geotiffs_profiles.zip` | 148 MB | TP4 — resultados de referencia |

El recorte del **TanDEM-X 30m EDEM** usado en TP1 no se redistribuye por restricciones de licencia de DLR: ver `02_PRACTICA/TP1/01_Materiales/LEEME_TanDEMX_EDEM.md` para obtenerlo (registro gratuito en el EOC Geoservice de DLR).

## Licencias

- **Materiales docentes** (PDF, Markdown, figuras propias): [CC BY-NC-SA 4.0](LICENSE-docs.md).
- **Código y notebooks**: [Licencia MIT](LICENSE).
- **Datos de terceros**: conservan su licencia original — ver [NOTICE.md](NOTICE.md).
- **Datos propios derivados de FABDEM** (DEM acondicionado, red de drenaje, HAND, etc.): CC BY-NC-SA 4.0 (heredada del FABDEM).

## Atribución de datos

Este material utiliza los siguientes conjuntos de datos (detalle completo en [NOTICE.md](NOTICE.md)):

- Hawker, L., Uhe, P., Paulo, L., Sosa, J., Savage, J., Sampson, C., & Neal, J. (2022). A 30 m global map of elevation with forests and buildings removed. *Environmental Research Letters*, 17(2), 024016. — **FABDEM** (CC BY-NC-SA 4.0)
- Zanaga, D., et al. (2022). *ESA WorldCover 10 m 2021 v200*. DOI: 10.5281/zenodo.7254221 — (CC BY 4.0)
- Instituto Geográfico Nacional de la República Argentina. *MDE-Ar v2.1* (30 m).
- DLR. *TanDEM-X 30 m Edited DEM (EDEM)* — licencia de uso científico, no redistribuible.
- *Contains modified Copernicus Sentinel data (2025–2026)* — Sentinel-1 y Sentinel-2.

## Cómo citar

Ver [CITATION.cff](CITATION.cff). Formato sugerido:

> del Valle, H. F. (2026). *Inteligencia Artificial aplicada al Manejo de Cuencas Hidrográficas e Hidrológicas — Materiales del curso de posgrado* (v2026.1). Universidad Nacional del Sur / CeReGeo-UADER / LEMIV-UNPSJB.

## Contacto

Héctor Francisco del Valle — hfdelvalle@gmail.com
