# -*- coding: utf-8 -*-
# Q2 - Reproyectar/verificar el DEM a UTM 20S desde QGIS
import processing

BASE = r"D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA"
RUTA_ENTRADA = BASE + r"\02_DATOS_BASE\DEM\FABDEM_BB_UTM20S.tif"          # DEM incluido, ya en EPSG:32720
RUTA_SALIDA  = BASE + r"\02_DATOS_BASE\DEM\FABDEM_BB_UTM20S_QGIS.tif"     # salida de practica
EPSG_DESTINO = 'EPSG:32720'
RESAMPLE     = 1   # 0=vecino, 1=bilineal, 2=cubico

params = {
    'INPUT': RUTA_ENTRADA,
    'SOURCE_CRS': None,
    'TARGET_CRS': EPSG_DESTINO,
    'RESAMPLING': RESAMPLE,
    'NODATA': None,
    'DATA_TYPE': 0,
    'OUTPUT': RUTA_SALIDA,
}
res = processing.run("gdal:warpreproject", params)
iface.addRasterLayer(res['OUTPUT'], "FABDEM_BB_UTM20S_QGIS")
print("Reproyectado/verificado OK ->", res['OUTPUT'])
