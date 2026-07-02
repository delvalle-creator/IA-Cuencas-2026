# NOTICE — Datos de terceros: fuentes, licencias y citas requeridas

Este repositorio utiliza y/o deriva productos de los siguientes conjuntos de datos.
Cada uno conserva su licencia original.

| Dataset | Fuente | Licencia | Redistribución en este repo |
|---|---|---|---|
| **FABDEM v1.2** | Universidad de Bristol / Fathom | CC BY-NC-SA 4.0 | Recortes y derivados incluidos (TP1, TP5) bajo la misma licencia |
| **MDE-Ar v2.1** (30 m) | Instituto Geográfico Nacional (IGN), Argentina | Descarga libre y gratuita; se requiere atribución al IGN | Recortes incluidos (TP1, TP5) |
| **TanDEM-X 30m EDEM** | DLR (Agencia Espacial Alemana) | Licencia de uso científico DLR — **no redistribuible** | **NO incluido.** Cada usuario debe descargarlo del EOC Geoservice de DLR (registro gratuito). Ver `02_PRACTICA/TP1/01_Materiales/LEEME_TanDEMX_EDEM.md` |
| **ESA WorldCover 10 m 2021 v200** | ESA | CC BY 4.0 | Recorte incluido (TP2) |
| **Copernicus Sentinel-1 / Sentinel-2** | ESA / Comisión Europea | Libre y abierta (legislación Copernicus) | Subsets incluidos (TP4); escena completa TP3 distribuida por Releases |
| **Google Satellite Embeddings** | Google Earth Engine | Términos de servicio de GEE | Solo resultados derivados (TP2) |
| **S2DR4** (superresolución) | Gamma Earth (info@gamma.earth) | Términos del proveedor | Solo el notebook que lo invoca (TP3) |

## Citas requeridas

- Hawker, L., Uhe, P., Paulo, L., Sosa, J., Savage, J., Sampson, C., & Neal, J. (2022).
  A 30 m global map of elevation with forests and buildings removed.
  *Environmental Research Letters*, 17(2), 024016. https://doi.org/10.1088/1748-9326/ac4d4f
- Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., et al. (2022).
  *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221
- Instituto Geográfico Nacional (Argentina). *Modelo Digital de Elevaciones de la
  República Argentina (MDE-Ar) v2.1*. https://www.ign.gob.ar
- DLR (2023). *TanDEM-X 30 m Edited Digital Elevation Model (EDEM)*.
  https://geoservice.dlr.de/web/dataguide/tdm30/
- **Atribución Sentinel:** "Contains modified Copernicus Sentinel data (2025–2026)".

## Nota sobre derivados del FABDEM

Todos los productos derivados del FABDEM incluidos en este repositorio (DEM
hidro-acondicionado, direcciones y acumulación de flujo, red de drenaje, orden de
Strahler, cauce principal, curvas de nivel, zonas altimétricas, HAND, resultados
HEC-RAS sobre terreno FABDEM) se distribuyen bajo **CC BY-NC-SA 4.0**, heredada
de la licencia del FABDEM.

## Datos hidrometeorológicos del TP5

Las series de lluvia (`hietograma_evento_BB.csv`) y caudal (`caudal_Naposta_evento.csv`)
son **series pedagógicas consistentes con el evento documentado** del 6-7 de marzo de
2025 (informes SMN/INA); no constituyen registros observados oficiales y no deben
usarse fuera del contexto didáctico de este curso.
