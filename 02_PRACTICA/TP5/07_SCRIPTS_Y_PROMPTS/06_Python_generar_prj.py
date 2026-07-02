# -*- coding: utf-8 -*-
"""06 - Generar el .prj (WKT) de un EPSG para RAS Mapper.
Ejecutar: python 06_Python_generar_prj.py
Requisitos: pip install pyproj
"""
from pathlib import Path
from pyproj import CRS

BASE = Path(r"D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA")
if not BASE.exists():
    BASE = Path(__file__).resolve().parents[1]
EPSG = 32720
SALIDAS = [
    BASE / r"03_HEC_RAS\Proyecto_HEC_RAS\EPSG_32720.prj",
    BASE / r"02_DATOS_BASE\Proyeccion\EPSG_32720.prj",
]

wkt = CRS.from_epsg(EPSG).to_wkt(version="WKT1_ESRI")
for salida in SALIDAS:
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(wkt, encoding="utf-8")
    print("OK ->", salida)
