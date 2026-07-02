# -*- coding: utf-8 -*-
"""05 - Reproyectar un DEM a UTM 20S (EPSG:32720).
Ejecutar: python 05_Python_reproyectar_dem.py
Requisitos: pip install rasterio
"""
from pathlib import Path
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

BASE = Path(r"D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA")
if not BASE.exists():
    BASE = Path(__file__).resolve().parents[1]
ENTRADA = BASE / r"02_DATOS_BASE\DEM\FABDEM_BB_UTM20S.tif"          # DEM incluido; ya está en EPSG:32720
SALIDA  = BASE / r"02_DATOS_BASE\DEM\FABDEM_BB_UTM20S_reproyectado.tif"
DST_CRS = "EPSG:32720"

with rasterio.open(ENTRADA) as src:
    t, w, h = calculate_default_transform(src.crs, DST_CRS, src.width, src.height, *src.bounds)
    meta = src.meta.copy()
    meta.update(crs=DST_CRS, transform=t, width=w, height=h)
    with rasterio.open(SALIDA, "w", **meta) as dst:
        reproject(
            source=rasterio.band(src, 1),
            destination=rasterio.band(dst, 1),
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=t,
            dst_crs=DST_CRS,
            resampling=Resampling.bilinear,
        )
with rasterio.open(SALIDA) as o:
    print("OK ->", SALIDA, "| CRS:", o.crs, "| res(m):", [round(r, 2) for r in o.res])
