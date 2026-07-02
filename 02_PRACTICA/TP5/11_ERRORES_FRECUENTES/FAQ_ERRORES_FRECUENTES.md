# Errores frecuentes

## HEC-RAS no abre el proyecto

Revisar que se esté abriendo:

```text
03_HEC_RAS/Proyecto_HEC_RAS/BahiaBlanca_2025.prj
```

No abrir archivos `.g01`, `.p01` o `.hdf` directamente.

## RAS Mapper no encuentra el terreno

Verificar que exista:

```text
03_HEC_RAS/Proyecto_HEC_RAS/Terrain/Terrain.hdf
```

Si el terreno no aparece, regenerar RAS Terrain desde `02_DATOS_BASE/DEM/FABDEM_BB_UTM20S.tif` y verificar EPSG:32720.

## Error de proyección

Usar siempre:

```text
EPSG:32720 - WGS 84 / UTM zone 20S
```

El archivo `.prj` está en `02_DATOS_BASE/Proyeccion` y también dentro del proyecto HEC-RAS.

## QGIS no carga el CSV de puntos

El CSV de puntos usa coordenadas UTM:

```text
xField = x_utm
yField = y_utm
crs = EPSG:32720
```

No usar LON/LAT para `dataset_puntos_BB.csv`.

## Orange abre el flujo pero no encuentra el CSV

Abrir el widget File y seleccionar manualmente:

```text
06_ORANGE_DATA_MINING/Datos/dataset_inundacion_BB.csv
```

Definir `inundado_cat` como target.

## El porcentaje de inundados en Orange parece alto

Es normal: el dataset de Orange está submuestreado para trabajar rápido. Incluye todos los píxeles inundados disponibles y una muestra de los secos. Para el porcentaje sobre la grilla completa, mirar el reporte de validación.

## HEC-RAS 7.x falla durante Compute

Puede ocurrir por problemas internos del preprocesador 2D o del RAS Terrain. Probar:

1. Regenerar el terreno.
2. Revisar geometría y malla.
3. Correr con una versión 6.x estable.
4. Reducir complejidad de malla para diagnóstico.

