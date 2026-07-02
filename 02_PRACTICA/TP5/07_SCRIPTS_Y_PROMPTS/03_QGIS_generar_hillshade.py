# -*- coding: utf-8 -*-
# Q3 - Hillshade del DEM en UTM 20S
import processing

BASE = r"D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA"
RUTA_DEM_UTM = BASE + r"\02_DATOS_BASE\DEM\FABDEM_BB_UTM20S.tif"
RUTA_SALIDA  = BASE + r"\02_DATOS_BASE\DEM\FABDEM_hillshade_QGIS.tif"

res = processing.run("gdal:hillshade", {
    'INPUT': RUTA_DEM_UTM,
    'BAND': 1,
    'Z_FACTOR': 1.0,
    'AZIMUTH': 315.0,
    'ALTITUDE': 45.0,
    'OUTPUT': RUTA_SALIDA,
})
iface.addRasterLayer(res['OUTPUT'], "FABDEM_hillshade_QGIS")
print("Hillshade OK ->", res['OUTPUT'])
