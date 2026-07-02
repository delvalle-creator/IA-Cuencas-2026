# -*- coding: utf-8 -*-
# Q4 - Cargar profundidad exportada desde HEC-RAS + puntos de validacion
import os
from qgis.core import QgsVectorLayer, QgsProject

BASE = r"D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA"
RUTA_DEPTH = BASE + r"\05_RESULTADOS_REFERENCIA\HEC_RAS_EXPORTAR_AQUI\Depth_Max.tif"
RUTA_CSV   = BASE + r"\06_ORANGE_DATA_MINING\Datos\dataset_puntos_BB.csv"

if os.path.exists(RUTA_DEPTH):
    iface.addRasterLayer(RUTA_DEPTH, "Profundidad_HECRAS_Maxima")
    print("Profundidad HEC-RAS cargada:", RUTA_DEPTH)
else:
    print("AVISO: todavia no existe Depth_Max.tif. Exportarlo desde RAS Mapper a:", RUTA_DEPTH)

uri = "file:///" + RUTA_CSV.replace("\\", "/") + "?delimiter=,&xField=x_utm&yField=y_utm&crs=EPSG:32720"
pts = QgsVectorLayer(uri, "puntos_validacion_BB", "delimitedtext")
if pts.isValid():
    QgsProject.instance().addMapLayer(pts)
    print("Puntos cargados:", pts.featureCount())
else:
    print("ERROR cargando puntos. Revisar el CSV:", RUTA_CSV)
