# TanDEM-X 30m EDEM — cómo obtener el recorte (no incluido en el repositorio)

El recorte `aoi_TanDEMX_EDEM.tif` **no se distribuye en este repositorio** porque la
licencia de uso científico de DLR no permite la redistribución a terceros. Cada
usuario debe descargar el producto y generar el recorte (10 minutos aprox.).

## Paso 1 — Descargar el tile

1. Ingresar al EOC Geoservice de DLR: https://download.geoservice.dlr.de/TDM30_EDEM/
2. Registrarse (gratuito) y aceptar la licencia de uso científico.
3. Descargar el tile que cubre el área de Bahía Blanca / cuenca del Napostá Grande
   (aprox. **S39 W063**, igual que el tile ESA WorldCover usado en TP2).

## Paso 2 — Generar el recorte

Recortar el tile con la misma extensión que los otros dos DTM del TP
(`aoi_FABDEM_v12.tif` y `aoi_MDE_Ar_v21.tif`). En QGIS:
**Ráster → Extracción → Cortar ráster por extensión**, usando como extensión la capa
`aoi_FABDEM_v12.tif`. Guardar como `aoi_TanDEMX_EDEM.tif` en esta carpeta
(el archivo `aoi_TanDEMX_EDEM.prj` ya está incluido como referencia del CRS).

También puede pedir a su asistente de IA un script de recorte, como se practica
en este TP (ver `02_Prompts_IA/`).

## Paso 3 — Continuar el TP normalmente

Los scripts `leer_metadatos_dtm.py` / `leer_metadatos_dtm_QGIS.py` detectan
automáticamente los GeoTIFF presentes en la carpeta: una vez colocado el recorte,
el TP se ejecuta igual que con los otros dos DTM.

> **Licencia:** el TanDEM-X 30m EDEM es © DLR, para uso científico, no
> redistribuible. Cita: DLR (2023), *TanDEM-X 30 m Edited DEM (EDEM)*,
> https://geoservice.dlr.de/web/dataguide/tdm30/. Ver `NOTICE.md` en la raíz.
