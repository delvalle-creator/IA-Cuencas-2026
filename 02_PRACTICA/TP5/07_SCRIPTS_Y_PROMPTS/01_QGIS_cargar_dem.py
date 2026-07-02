# -*- coding: utf-8 -*-
# Q1 - Cargar el DEM de trabajo en QGIS
from qgis.core import QgsRasterLayer, QgsProject

BASE = r"D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA"  # carpeta raiz sugerida del practico
RUTA_DEM = BASE + r"\02_DATOS_BASE\DEM\FABDEM_BB_UTM20S.tif"

capa = QgsRasterLayer(RUTA_DEM, "FABDEM_BB_UTM20S")
if not capa.isValid():
    print("ERROR: no se pudo cargar el DEM. Revisar RUTA_DEM:", RUTA_DEM)
else:
    QgsProject.instance().addMapLayer(capa)
    ext = capa.extent()
    print("DEM cargado OK | CRS:", capa.crs().authid(), "| pixeles:", capa.width(), "x", capa.height())
    print("Extension:", ext.toString())
