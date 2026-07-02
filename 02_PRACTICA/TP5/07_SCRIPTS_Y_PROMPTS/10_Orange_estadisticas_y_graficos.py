# -*- coding: utf-8 -*-
"""
10 - Analisis estadistico y graficos del dataset de inundacion.
Replica, fuera de Orange, las estadisticas y figuras principales.

Uso: python 10_Orange_estadisticas_y_graficos.py
Requisitos: numpy, pandas, matplotlib
Salida: 06_ORANGE_DATA_MINING/Figuras/*.png y 06_ORANGE_DATA_MINING/Datos/estadisticas_resumen.csv
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = Path(__file__).resolve().parent
BASE = AQUI.parent
DATOS = BASE / "06_ORANGE_DATA_MINING" / "Datos"
CSV = DATOS / "dataset_inundacion_BB.csv"
FIG = BASE / "06_ORANGE_DATA_MINING" / "Figuras"
FIG.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)
num = ["elevacion_m", "hand_m", "profundidad_m"]

desc = df[num].describe().T
desc["mediana"] = df[num].median()
desc.to_csv(DATOS / "estadisticas_resumen.csv")
print("=== Estadisticas descriptivas ===")
print(desc.round(3).to_string())
print("\n=== Correlaciones (Pearson) ===")
print(df[num].corr().round(3).to_string())
print(f"\nInundado en dataset Orange: {df['inundado'].mean()*100:.1f}% ({int(df['inundado'].sum())} de {len(df)})")

plt.figure(figsize=(7, 4))
d = df.loc[df.profundidad_m > 0.05, "profundidad_m"]
plt.hist(d, bins=40, edgecolor="white")
plt.xlabel("Profundidad de inundacion (m)")
plt.ylabel("N de pixeles")
plt.title("Distribucion de la profundidad (pixeles inundados)")
plt.tight_layout()
plt.savefig(FIG / "01_hist_profundidad.png", dpi=130)
plt.close()

plt.figure(figsize=(7, 4))
orden = ["seco", "0-0.5 m", "0.5-1 m", "1-2 m", ">2 m"]
cnt = df["clase_profundidad"].value_counts().reindex(orden).fillna(0)
plt.bar(orden, cnt.values)
plt.ylabel("N de pixeles")
plt.title("Pixeles por clase de profundidad")
plt.tight_layout()
plt.savefig(FIG / "02_barras_clases.png", dpi=130)
plt.close()

plt.figure(figsize=(6, 5))
s = df.sample(min(8000, len(df)), random_state=1)
sc = plt.scatter(s.hand_m, s.profundidad_m, c=s.inundado, s=8, alpha=0.5)
plt.xlabel("HAND (m)")
plt.ylabel("Profundidad (m)")
plt.title("HAND vs profundidad de inundacion")
plt.colorbar(sc, label="inundado")
plt.xlim(0, 30)
plt.tight_layout()
plt.savefig(FIG / "03_scatter_hand_prof.png", dpi=130)
plt.close()

plt.figure(figsize=(6, 5))
m = df[num + ["inundado"]].corr()
plt.imshow(m, vmin=-1, vmax=1)
plt.xticks(range(len(m)), m.columns, rotation=45, ha="right")
plt.yticks(range(len(m)), m.columns)
for i in range(len(m)):
    for j in range(len(m)):
        plt.text(j, i, f"{m.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
plt.title("Matriz de correlacion")
plt.colorbar(label="r")
plt.tight_layout()
plt.savefig(FIG / "04_correlacion.png", dpi=130)
plt.close()

plt.figure(figsize=(7, 4))
df.boxplot(column="elevacion_m", by="inundado", grid=False)
plt.suptitle("")
plt.title("Elevacion segun condicion de inundacion")
plt.xlabel("inundado (0=no, 1=si)")
plt.ylabel("Elevacion (m)")
plt.tight_layout()
plt.savefig(FIG / "05_box_elev_inundado.png", dpi=130)
plt.close()

print(f"\nFiguras guardadas en: {FIG}")
