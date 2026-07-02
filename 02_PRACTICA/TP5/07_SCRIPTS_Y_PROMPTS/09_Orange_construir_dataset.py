# -*- coding: utf-8 -*-
"""
09 - Construye el dataset tabular para Orange Data Mining a partir de los
resultados de referencia HAND/ponding del práctico.

Salida:
  06_ORANGE_DATA_MINING/Datos/dataset_inundacion_BB.csv
  06_ORANGE_DATA_MINING/Datos/dataset_puntos_BB.csv

Uso: python 09_Orange_construir_dataset.py
Requisitos: numpy
"""
import json
from pathlib import Path
import numpy as np

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
RES = BASE / "05_RESULTADOS_REFERENCIA" / "HAND_Numpy"
DATOS = BASE / "06_ORANGE_DATA_MINING" / "Datos"
DATOS.mkdir(parents=True, exist_ok=True)
OUT_CSV = DATOS / "dataset_inundacion_BB.csv"
OUT_PTS = DATOS / "dataset_puntos_BB.csv"

N_MUESTRA = 30000
UMBRAL_INUNDADO = 0.05

dem = np.load(RES / "_dem.npy").astype(float)
hand = np.load(RES / "_hand.npy").astype(float)
pond = np.load(RES / "_pond.npy").astype(float)
meta = json.load(open(RES / "_meta.json", encoding="utf-8"))
xmin, xmax, ymin, ymax = meta["extent"]
nrow, ncol = dem.shape
pw = (xmax - xmin) / ncol
ph = (ymax - ymin) / nrow

dem[dem <= -9000] = np.nan
hand[hand > 1000] = np.nan
valido = ~np.isnan(dem) & ~np.isnan(hand) & ~np.isnan(pond)

rr, cc = np.where(valido)
x = xmin + (cc + 0.5) * pw
y = ymax - (rr + 0.5) * ph
elev = dem[rr, cc]
h = hand[rr, cc]
prof = pond[rr, cc]
inund = (prof > UMBRAL_INUNDADO).astype(int)

bins = [-0.001, UMBRAL_INUNDADO, 0.5, 1.0, 2.0, np.inf]
etiq = ["seco", "0-0.5 m", "0.5-1 m", "1-2 m", ">2 m"]
clase = np.array(etiq)[np.digitize(prof, bins) - 1]

idx = np.arange(len(rr))
if N_MUESTRA and len(idx) > N_MUESTRA:
    rng = np.random.default_rng(42)
    pos = idx[inund == 1]
    neg = idx[inund == 0]
    n_pos = min(len(pos), N_MUESTRA // 2)
    n_neg = N_MUESTRA - n_pos
    sel = np.concatenate([
        rng.choice(pos, n_pos, replace=False),
        rng.choice(neg, min(n_neg, len(neg)), replace=False),
    ])
    rng.shuffle(sel)
    idx = sel

with open(OUT_CSV, "w", encoding="utf-8") as f:
    f.write("x_utm,y_utm,elevacion_m,hand_m,profundidad_m,inundado,inundado_cat,clase_profundidad\n")
    for i in idx:
        cat = "si" if inund[i] == 1 else "no"
        f.write(f"{x[i]:.2f},{y[i]:.2f},{elev[i]:.3f},{h[i]:.3f},{prof[i]:.3f},{inund[i]},{cat},{clase[i]}\n")

pts = np.load(RES / "_pts.npy").astype(float)
with open(OUT_PTS, "w", encoding="utf-8") as f:
    f.write("punto,x_utm,y_utm,elevacion_m,hand_m,profundidad_m,inundado\n")
    for k in range(pts.shape[1]):
        px, py = pts[0, k], pts[1, k]
        c = int(min(max((px - xmin) / pw, 0), ncol - 1))
        r = int(min(max((ymax - py) / ph, 0), nrow - 1))
        e = dem[r, c]
        hh = hand[r, c]
        pp = pond[r, c]
        ii = int(pp > UMBRAL_INUNDADO) if not np.isnan(pp) else 0
        f.write(
            f"{k+1},{px:.2f},{py:.2f},"
            f"{'' if np.isnan(e) else round(e,3)},"
            f"{'' if np.isnan(hh) else round(hh,3)},"
            f"{'' if np.isnan(pp) else round(pp,3)},{ii}\n"
        )

n_tot = int(valido.sum())
print(f"Pixeles validos: {n_tot:,} | filas exportadas: {len(idx):,}")
print(f"Inundados en grilla completa (prof>{UMBRAL_INUNDADO} m): {int(inund.sum()):,} ({100*inund.mean():.2f}% del total valido)")
print(f"CSV principal: {OUT_CSV}")
print(f"CSV puntos:    {OUT_PTS}")
