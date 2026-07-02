# HEC-RAS - notas de uso

Proyecto principal:

```text
03_HEC_RAS/Proyecto_HEC_RAS/BahiaBlanca_2025.prj
```

Abrir ese archivo desde HEC-RAS. No mover archivos internos del proyecto por separado: `.prj`, `.rasmap`, geometrías, planes, archivos HDF y carpeta `Terrain` deben permanecer juntos.

## Terreno

El terreno del proyecto está en:

```text
03_HEC_RAS/Proyecto_HEC_RAS/Terrain
```

Los DEM fuente están en:

```text
02_DATOS_BASE/DEM
```

## Exportación esperada

Cuando se genere la profundidad máxima desde RAS Mapper, exportar el raster como:

```text
05_RESULTADOS_REFERENCIA/HEC_RAS_EXPORTAR_AQUI/Depth_Max.tif
```

Ese nombre coincide con el script `07_SCRIPTS_Y_PROMPTS/04_QGIS_cargar_resultado_y_puntos.py`.

## Nota técnica

El material conserva el modelo HEC-RAS desarrollado. La ejecución completa depende de HEC-RAS instalado en Windows. Si una versión 7.x genera errores internos del preprocesador 2D, probar con una versión 6.x estable o regenerar el RAS Terrain desde el DEM.


## Malla 2D real

La malla 2D real del plan actual se documenta en el práctico principal y puede revisarse en QGIS desde `04_QGIS/Capas_Vectoriales/malla_2D_HEC_RAS_real.gpkg`.
