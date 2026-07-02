# -*- coding: utf-8 -*-
"""07 - Vista previa de inundacion por metodo HAND y figuras (FABDEM bare-earth).
Mapas en azul con CENTRO de Bahia Blanca (estrella roja) y etiquetas de cauces
(Arroyo Naposta, Canal Maldonado) y referencias (Ing. White, Estuario).

Ejecutar:  python 07_Python_analisis_HAND_y_figuras.py
Requisitos: pip install rasterio pysheds numpy scipy matplotlib pyproj
NOTA: es una PREVIA hidrologica-topografica (proxy), NO el resultado hidrodinamico de HEC-RAS.
"""
import os, csv, warnings
import numpy as np
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LightSource, ListedColormap
from matplotlib.patches import Patch
from scipy.ndimage import binary_erosion
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pysheds.grid import Grid
from pyproj import Transformer

# ------------------- RUTAS -------------------
BASE     = r"D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA"   # carpeta raiz sugerida del practico
if not os.path.exists(BASE):
    BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FAB_UTM  = os.path.join(BASE, r"02_DATOS_BASE\DEM\FABDEM_BB_UTM20S.tif")
MDE_ORIG = os.path.join(BASE, r"02_DATOS_BASE\DEM\MDE_Ar_BB_UTM20S.tif")
CSV_PTS  = os.path.join(BASE, r"06_ORANGE_DATA_MINING\Datos\dataset_puntos_BB.csv")
CAP      = os.path.join(BASE, r"05_RESULTADOS_REFERENCIA\Figuras_HAND"); os.makedirs(CAP, exist_ok=True)

THR_DREN = 1200   # << AJUSTABLE (umbral de drenaje en celdas: red mas/menos densa)
COTA     = 2.0    # << AJUSTABLE (cota de inundacion sobre el drenaje, en metros)
_tr = Transformer.from_crs("EPSG:4326", "EPSG:32720", always_xy=True)

# --- ANOTACIONES (lon, lat) - EDITAR LIBREMENTE para reposicionar etiquetas ---
LON0, LAT0 = -62.2724, -38.7196                       # centro de Bahia Blanca
EX, NY = _tr.transform(LON0, LAT0)
CAUCES = [("Arroyo Naposta", -62.252, -38.700),       # cauce N-S por el centro
          ("Canal Maldonado", -62.320, -38.752)]      # aliviador, al oeste
REFS   = [("Ing. White (puerto)", -62.268, -38.770),
          ("Estuario / Ria",      -62.300, -38.795)]
_HALO = [pe.withStroke(linewidth=2.4, foreground="white")]

def _xy(lon, lat):  # centro/etiquetas estan en grados -> a UTM 20S
    return _tr.transform(lon, lat)
def estrella(ax):
    ax.scatter([EX], [NY], marker="*", s=240, c="red", edgecolor="black", lw=0.8, zorder=10, label="Bahia Blanca (centro)")
def etiquetas(ax, refs=True):
    for n, lo, la in CAUCES:
        x, y = _xy(lo, la)
        ax.text(x, y, n, fontsize=8.5, style="italic", weight="bold", color="#003B73",
                ha="center", va="center", zorder=11, path_effects=_HALO)
    if refs:
        for n, lo, la in REFS:
            x, y = _xy(lo, la)
            ax.scatter([x], [y], marker="s", s=26, c="black", edgecolor="white", lw=0.6, zorder=10)
            ax.text(x, y - 420, n, fontsize=7.5, color="black", ha="center", va="top", zorder=11, path_effects=_HALO)

def reproyectar_a_utm(entrada, salida, dst="EPSG:32720"):
    if os.path.exists(salida): return salida
    with rasterio.open(entrada) as src:
        t, w, h = calculate_default_transform(src.crs, dst, src.width, src.height, *src.bounds)
        meta = src.meta.copy(); meta.update(crs=dst, transform=t, width=w, height=h)
        with rasterio.open(salida, "w", **meta) as d:
            reproject(source=rasterio.band(src,1), destination=rasterio.band(d,1),
                      src_transform=src.transform, src_crs=src.crs, dst_transform=t, dst_crs=dst, resampling=Resampling.bilinear)
    return salida

def modelo(dem_path, thr=THR_DREN, stage=COTA):
    grid = Grid.from_raster(dem_path); dem = grid.read_raster(dem_path)
    a = np.array(dem, dtype="float32"); v = np.isfinite(a) & (a > -1000)
    inf = grid.resolve_flats(grid.fill_depressions(grid.fill_pits(dem)))
    fdir = grid.flowdir(inf); acc_r = grid.accumulation(fdir)
    hand = np.array(grid.compute_hand(fdir, inf, acc_r > thr), dtype="float32")
    acc = np.array(acc_r, dtype="float32")
    pond = np.array(grid.fill_depressions(grid.fill_pits(dem)), dtype="float32") - a
    inu = ((hand < stage) | (pond > 0.3)) & v
    red = (acc > thr) & binary_erosion(v, iterations=2)
    cell = abs(grid.affine.a * grid.affine.e) / 1e6
    return dict(dem=a, val=v, hand=hand, pond=pond, red=red, inund=inu, ext=grid.extent,
                area=float(inu.sum()*cell), affine=grid.affine)

_ls = LightSource(azdeg=315, altdeg=45)
def fondo(ax, m):
    h = _ls.hillshade(np.where(m["val"], m["dem"], np.nanmin(m["dem"][m["val"]])), vert_exag=18)
    ax.set_facecolor("white")
    ax.imshow(np.ma.masked_where(~m["val"], h), extent=m["ext"], cmap="gray", origin="upper")
    ax.imshow(np.ma.masked_where(~m["val"], m["dem"]), extent=m["ext"], cmap="terrain", alpha=0.28, origin="upper")
    ax.ticklabel_format(style="plain"); ax.tick_params(labelsize=7)
def pinta(ax, m, al=0.55):
    ax.imshow(np.ma.masked_where(~m["inund"], np.ones_like(m["dem"])), extent=m["ext"], cmap=ListedColormap(["#1565C0"]), alpha=al, origin="upper")
    ax.imshow(np.ma.masked_where(~m["red"], np.ones_like(m["dem"])), extent=m["ext"], cmap=ListedColormap(["#002C57"]), origin="upper")

print("Procesando FABDEM ...")
mF = modelo(FAB_UTM); xmin, xmax, ymin, ymax = mF["ext"]
def cargar_puntos_validacion(csv_pts):
    xs, ys = [], []
    if os.path.exists(csv_pts):
        with open(csv_pts, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if "LON" in row and "LAT" in row:
                    x, y = _tr.transform(float(row["LON"]), float(row["LAT"]))
                elif "x_utm" in row and "y_utm" in row:
                    x, y = float(row["x_utm"]), float(row["y_utm"])
                else:
                    continue
                xs.append(x); ys.append(y)
    else:
        pts_npy = os.path.join(BASE, r"05_RESULTADOS_REFERENCIA\HAND_Numpy\_pts.npy")
        if os.path.exists(pts_npy):
            pts = np.load(pts_npy).astype(float)
            xs, ys = list(pts[0, :]), list(pts[1, :])
    if not xs:
        raise FileNotFoundError("No se encontraron puntos de validacion en CSV_PTS ni en _pts.npy")
    return np.array(xs), np.array(ys)

xs, ys = cargar_puntos_validacion(CSV_PTS)
dentro = (xs>=xmin)&(xs<=xmax)&(ys>=ymin)&(ys<=ymax)

# mapa principal
fig, ax = plt.subplots(figsize=(9, 7.6)); fondo(ax, mF); pinta(ax, mF)
ax.scatter(xs[dentro], ys[dentro], c="red", s=24, edgecolor="white", lw=0.5, zorder=6); estrella(ax); etiquetas(ax)
ax.legend(handles=[Patch(fc="#1565C0", alpha=0.55, label=f"Area inundada (HAND<2 m) ~ {mF['area']:.0f} km2"),
    Patch(fc="#002C57", label="Red de drenaje"),
    plt.Line2D([0],[0], marker="o", color="w", markerfacecolor="red", markeredgecolor="white", markersize=8, label=f"Puntos validacion ({int(dentro.sum())})"),
    plt.Line2D([0],[0], marker="*", color="w", markerfacecolor="red", markeredgecolor="black", markersize=13, label="Bahia Blanca (centro)")],
    loc="lower right", fontsize=8.5, framealpha=0.92)
ax.set_title("Vista previa de inundacion sobre FABDEM (bare-earth) - metodo HAND (preliminar)")
ax.set_xlabel("Este (m) - UTM 20S / EPSG:32720"); ax.set_ylabel("Norte (m)")
plt.tight_layout(); plt.savefig(os.path.join(CAP, "fig_inundacion_FABDEM.png"), dpi=145); plt.close()

# comparacion DEM
print("Procesando MDE-Ar ...")
MDE_UTM = reproyectar_a_utm(MDE_ORIG, os.path.join(BASE, r"02_DATOS_BASE\DEM\MDE_Ar_BB_UTM20S.tif")); mM = modelo(MDE_UTM)
fig, axs = plt.subplots(1, 2, figsize=(13, 6.2))
for a, m, ttl in [(axs[0], mF, "FABDEM (bare-earth)"), (axs[1], mM, "MDE-Ar (fotogrametrico)")]:
    fondo(a, m); pinta(a, m); estrella(a); etiquetas(a, refs=False); a.set_title(f"{ttl}\nArea ~ {m['area']:.0f} km2"); a.set_xlabel("Este (m)")
axs[0].set_ylabel("Norte (m)"); plt.suptitle("Sensibilidad al DEM: misma metodologia (HAND<2 m)")
plt.tight_layout(); plt.savefig(os.path.join(CAP, "fig_comparacion_DEM.png"), dpi=140); plt.close()

# escenarios de cota
fig, axs = plt.subplots(1, 3, figsize=(15, 5.6))
for a, st in zip(axs, [1, 2, 3]):
    mS = modelo(FAB_UTM, stage=st); fondo(a, mS); pinta(a, mS); estrella(a); etiquetas(a, refs=False)
    a.set_title(f"Cota HAND < {st} m  ->  {mS['area']:.0f} km2"); a.set_xlabel("Este (m)")
axs[0].set_ylabel("Norte (m)"); plt.suptitle("FABDEM - Escenarios de severidad por cota")
plt.tight_layout(); plt.savefig(os.path.join(CAP, "fig_escenarios_cota.png"), dpi=140); plt.close()

# umbral de drenaje
fig, axs = plt.subplots(1, 3, figsize=(15, 5.6))
for a, thr in zip(axs, [400, 1200, 3000]):
    mT = modelo(FAB_UTM, thr=thr); fondo(a, mT); pinta(a, mT, 0.5); estrella(a); etiquetas(a, refs=False)
    a.set_title(f"acc > {thr} celdas\nArea ~ {mT['area']:.0f} km2"); a.set_xlabel("Este (m)")
axs[0].set_ylabel("Norte (m)"); plt.suptitle("FABDEM - Calibracion del umbral de drenaje")
plt.tight_layout(); plt.savefig(os.path.join(CAP, "fig_umbral_drenaje.png"), dpi=140); plt.close()

# profundidad
depth = np.where(mF["hand"] < 3, 3 - mF["hand"], 0).astype("float32")
depth = np.maximum(depth, np.where(mF["pond"] > 0.3, mF["pond"], 0)); depth[~mF["val"]] = np.nan; depth[depth<=0] = np.nan
fig, ax = plt.subplots(figsize=(9, 7.6)); fondo(ax, mF)
im = ax.imshow(np.ma.masked_invalid(depth), extent=mF["ext"], cmap="Blues", alpha=0.8, origin="upper", vmin=0, vmax=3)
ax.imshow(np.ma.masked_where(~mF["red"], np.ones_like(mF["dem"])), extent=mF["ext"], cmap=ListedColormap(["#002C57"]), origin="upper")
estrella(ax); etiquetas(ax); plt.colorbar(im, ax=ax, shrink=0.8, label="Profundidad relativa estimada (m) - proxy")
ax.set_title("FABDEM - Mapa de profundidad relativa estimada (proxy)"); ax.set_xlabel("Este (m) - UTM 20S"); ax.set_ylabel("Norte (m)")
ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
plt.tight_layout(); plt.savefig(os.path.join(CAP, "fig_profundidad.png"), dpi=145); plt.close()

# clasificacion de puntos
res = abs(mF["affine"].e); pxw = mF["affine"].a; clase = []
for x, y in zip(xs[dentro], ys[dentro]):
    c = int((x-xmin)/pxw); r = int((ymax-y)/res); ok = (0<=r<mF["inund"].shape[0]) and (0<=c<mF["inund"].shape[1])
    clase.append(bool(mF["inund"][r, c]) if ok else False)
clase = np.array(clase); n_in = int(clase.sum()); n_dry = int(len(clase)-n_in)
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 6.4), gridspec_kw={"width_ratios": [1.5, 1]})
fondo(ax, mF); ax.imshow(np.ma.masked_where(~mF["inund"], np.ones_like(mF["dem"])), extent=mF["ext"], cmap=ListedColormap(["#1565C0"]), alpha=0.4, origin="upper")
xi, yi = xs[dentro], ys[dentro]
ax.scatter(xi[clase],  yi[clase],  c="#0D47A1", s=42, edgecolor="white", lw=0.7, zorder=6, label=f"Sim. inundado ({n_in})")
ax.scatter(xi[~clase], yi[~clase], c="#E65100", s=42, edgecolor="white", lw=0.7, zorder=6, label=f"Sim. seco ({n_dry})")
estrella(ax); etiquetas(ax); ax.legend(loc="upper left", fontsize=9); ax.set_xlabel("Este (m)"); ax.set_ylabel("Norte (m)")
ax.set_title(f"Clasificacion SIMULADA de los {len(clase)} puntos dentro del DEM")
ax2.axis("off"); ax2.set_title("Matriz de confusion (plantilla)\nObservado = Collect Earth Online")
tbl = [["", "Obs. INUNDADO", "Obs. SECO"], ["Sim. INUNDADO", "VP = ?", "FP = ?"], ["Sim. SECO", "FN = ?", "VN = ?"]]
t = ax2.table(cellText=tbl, loc="center", cellLoc="center", bbox=[0.05, 0.3, 0.9, 0.45]); t.auto_set_font_size(False); t.set_fontsize(10)
for (r, c), cel in t.get_celld().items():
    if r == 0 or c == 0: cel.set_facecolor("#1F4E79"); cel.set_text_props(color="white", weight="bold")
ax2.text(0.5, 0.12, f"Simulado: {n_in} inundados / {n_dry} secos (de {len(clase)} puntos).", ha="center", fontsize=9, transform=ax2.transAxes)
plt.tight_layout(); plt.savefig(os.path.join(CAP, "fig_validacion_puntos.png"), dpi=140); plt.close()

print("\nLISTO. Figuras (centro + cauces + referencias) en:", CAP)
print(f"  Area FABDEM ~ {mF['area']:.0f} km2 | MDE-Ar ~ {mM['area']:.0f} km2 | Puntos en DEM: {int(dentro.sum())}/60")
