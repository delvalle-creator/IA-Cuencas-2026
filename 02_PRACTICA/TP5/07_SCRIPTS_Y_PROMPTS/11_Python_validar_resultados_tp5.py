# -*- coding: utf-8 -*-
r"""Valida los resultados de referencia del TP5.

Este script NO reemplaza la corrida hidrodinamica de HEC-RAS. Sirve para verificar que
los archivos HAND/Orange incluidos en el práctico son consistentes entre sí.

Ejecutar desde cualquier carpeta:
    python D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA\07_SCRIPTS_Y_PROMPTS\11_Python_validar_resultados_tp5.py
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

BASE = Path(r"D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA")
if not BASE.exists():
    BASE = Path(__file__).resolve().parents[1]
RES = BASE / "05_RESULTADOS_REFERENCIA" / "HAND_Numpy"
DATOS = BASE / "06_ORANGE_DATA_MINING" / "Datos"
OUT = BASE / "05_RESULTADOS_REFERENCIA" / "VALIDACION_RESULTADOS_REFERENCIA.txt"

UMBRAL = 0.05

def ok(path):
    return "OK" if path.exists() else "FALTA"

requeridos = [
    RES / "_dem.npy", RES / "_hand.npy", RES / "_pond.npy", RES / "_pts.npy", RES / "_meta.json",
    DATOS / "dataset_inundacion_BB.csv", DATOS / "dataset_puntos_BB.csv", DATOS / "estadisticas_resumen.csv",
]

lineas = []
lineas.append("VALIDACION DE RESULTADOS DE REFERENCIA - TP5 Bahia Blanca")
lineas.append("=" * 72)
lineas.append(f"Carpeta base: {BASE}")
lineas.append("")
lineas.append("1) Archivos requeridos")
for p in requeridos:
    lineas.append(f"   [{ok(p)}] {p.relative_to(BASE)}")

faltantes = [p for p in requeridos if not p.exists()]
if faltantes:
    OUT.write_text("\n".join(lineas) + "\n\nFaltan archivos; no se puede completar la validacion.\n", encoding="utf-8")
    raise SystemExit(f"Faltan archivos. Ver reporte: {OUT}")

dem = np.load(RES / "_dem.npy").astype(float)
hand = np.load(RES / "_hand.npy").astype(float)
pond = np.load(RES / "_pond.npy").astype(float)
pts = np.load(RES / "_pts.npy").astype(float)
meta = json.load(open(RES / "_meta.json", encoding="utf-8"))

dem2 = dem.copy(); hand2 = hand.copy(); pond2 = pond.copy()
dem2[dem2 <= -9000] = np.nan
hand2[hand2 > 1000] = np.nan
valido = ~np.isnan(dem2) & ~np.isnan(hand2) & ~np.isnan(pond2)
inund_full = (pond2[valido] > UMBRAL)
cell_km2 = float(meta.get("cell_km2", 0))
area_valida = int(valido.sum()) * cell_km2
area_inundada = int(inund_full.sum()) * cell_km2

lineas.append("")
lineas.append("2) Matrices HAND / ponding")
lineas.append(f"   Shape DEM/HAND/Ponding: {dem.shape} / {hand.shape} / {pond.shape}")
lineas.append(f"   CRS: {meta.get('crs')}")
lineas.append(f"   Extension UTM: {meta.get('extent')}")
lineas.append(f"   Pixeles validos: {int(valido.sum()):,}")
lineas.append(f"   Pixeles inundados en grilla completa (prof > {UMBRAL} m): {int(inund_full.sum()):,} ({100*inund_full.mean():.2f}%)")
lineas.append(f"   Area valida aprox.: {area_valida:.2f} km2")
lineas.append(f"   Area inundada aprox.: {area_inundada:.2f} km2")
lineas.append(f"   Puntos de validacion: {pts.shape[1] if pts.ndim == 2 else 'shape inesperada'}")

for nombre, arr in [("Elevacion", dem2[valido]), ("HAND", hand2[valido]), ("Profundidad/ponding", pond2[valido])]:
    lineas.append(f"   {nombre} - min={np.nanmin(arr):.3f}, media={np.nanmean(arr):.3f}, mediana={np.nanmedian(arr):.3f}, max={np.nanmax(arr):.3f}")

df = pd.read_csv(DATOS / "dataset_inundacion_BB.csv")
pts_df = pd.read_csv(DATOS / "dataset_puntos_BB.csv")
stats = pd.read_csv(DATOS / "estadisticas_resumen.csv", index_col=0)
num = ["elevacion_m", "hand_m", "profundidad_m"]
calc = df[num].describe().T
calc["mediana"] = df[num].median()
max_diff = float((calc[stats.columns].round(6) - stats.round(6)).abs().max().max())

lineas.append("")
lineas.append("3) Dataset Orange")
lineas.append(f"   Filas / columnas: {df.shape[0]:,} / {df.shape[1]}")
lineas.append(f"   Inundados en dataset Orange: {int(df['inundado'].sum()):,} ({100*df['inundado'].mean():.2f}%)")
lineas.append("   Nota: el dataset de Orange esta submuestreado y enriquecido con todos los pixeles inundados; por eso el porcentaje no coincide con la grilla completa.")
lineas.append(f"   Puntos con valor inundado=1: {int(pts_df['inundado'].sum())} de {len(pts_df)}")
lineas.append(f"   Diferencia maxima entre estadisticas calculadas y estadisticas_resumen.csv: {max_diff:.8f}")

corr = df[num + ["inundado"]].corr().round(3)
lineas.append("")
lineas.append("4) Correlaciones principales")
for row_name in corr.index:
    vals = ", ".join([f"{col}={corr.loc[row_name, col]:.3f}" for col in corr.columns])
    lineas.append(f"   {row_name}: {vals}")

lineas.append("")
lineas.append("5) Conclusion automatica")
if max_diff < 1e-5 and df.shape[0] == 30000 and pts_df.shape[0] == 60:
    lineas.append("   OK: los resultados HAND/Orange incluidos son internamente consistentes.")
else:
    lineas.append("   REVISAR: se detectaron diferencias en dimensiones, estadisticas o puntos.")

OUT.write_text("\n".join(lineas) + "\n", encoding="utf-8")
print("\n".join(lineas))
print("\nReporte escrito en:", OUT)
