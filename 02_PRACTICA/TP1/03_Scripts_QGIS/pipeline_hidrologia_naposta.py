# -*- coding: utf-8 -*-
"""
==================================================================================
 PIPELINE HIDROLÓGICO — CUENCA ARROYO NAPOSTÁ GRANDE (FABDEM)
 Salida ORDENADA y NUMERADA (01 -> 14). Sin subdivisión en microcuencas.
 La cuenca ya está definida por el vector; el DEM es FABDEM recortado a ella.
==================================================================================
 QUÉ HACE (en este orden):
   1  Reproyecta FABDEM a EPSG:32720 (UTM 20S, metros) y recorta al polígono.
   2  Rellena depresiones (priority-flood, Barnes 2014) -> DEM hidro-acondicionado.
   3  Dirección de flujo D8 (códigos ESRI) y acumulación de flujo.
   4  Red de drenaje por umbral de acumulación + orden de Strahler.
   5  Vectoriza la red, traza el cauce principal (longest flow path) y el outlet.
   6  Pendiente, hillshade, curvas de nivel y zonificación alta/media/baja.
   7  Calcula los parámetros morfométricos.
   8  Escribe un estilo .qml junto a cada salida (QGIS lo aplica solo al cargar).

 REQUISITOS (instalar una sola vez):
     pip install rasterio scipy pyshp contourpy
 USO:
     1) Editar el bloque CONFIG (rutas de entrada y carpeta de salida).
     2) python pipeline_hidrologia_naposta.py
     3) En QGIS, arrastrar los archivos 00..13 (el estilo se aplica automáticamente).
==================================================================================
"""
import os, math, json
import numpy as np
import rasterio
from rasterio.transform import Affine
from rasterio.warp import calculate_default_transform, reproject, Resampling, transform_geom
from rasterio.mask import mask as rio_mask
import shapefile                      # pyshp
from contourpy import contour_generator
import heapq
from collections import deque

# =============================== CONFIG ==========================================
# EDITAR ANTES DE EJECUTAR (rutas de SU máquina):
#   DEM_IN : GeoTIFF FABDEM en EPSG:4326 que cubra TODA la cuenca
#            (mosaico descargado de https://data.bris.ac.uk — buscar "FABDEM").
#   SHP_IN : shapefile EN EPSG:4326 con el polígono de la cuenca; debe tener un
#            campo cuyo nombre/valor se indican en BASIN_FIELD / BASIN_VALUE.
#            (El resultado ya calculado está en 07_Hidrologia_Naposta_Grande/.)
#   OUT    : carpeta de salida (se crea sola).
DEM_IN   = r"EDITAR\ruta\a\FABDEM_zona_naposta.tif"          # FABDEM (EPSG:4326)
SHP_IN   = r"EDITAR\ruta\a\poligono_cuenca.shp"              # polígono cuenca (EPSG:4326)
BASIN_FIELD, BASIN_VALUE = "bid", 2                          # campo y valor que seleccionan la cuenca en SHP_IN
OUT      = r"salida_hidrologia_naposta"                      # carpeta de salida
DST_CRS  = "EPSG:32720"     # WGS84 / UTM 20S (Bahia Blanca). POSGAR 2007 Faja 4 = EPSG:5346
RES      = 30.0              # tamaño de píxel (m)
THRESH_KM2 = 0.5            # umbral de acumulacion para definir cauce (km2)
CONTOUR_INT = 50.0          # intervalo de curvas de nivel (m)
ND = -9999.0
# =================================================================================

if "EDITAR" in DEM_IN or "EDITAR" in SHP_IN:
    raise SystemExit("[CONFIG] Edite primero las rutas DEM_IN y SHP_IN en el bloque "
                     "CONFIG de este script (líneas 38-48) con los archivos de su máquina.")

os.makedirs(OUT, exist_ok=True)
CRS = rasterio.crs.CRS.from_string(DST_CRS); WKT = CRS.to_wkt()
def log(n, msg): print(f"[{n:02d}] {msg}")

# ---- 1. POLÍGONO + REPROYECCIÓN + RECORTE --------------------------------------
sf = shapefile.Reader(SHP_IN)
idx = next(i for i, r in enumerate(sf.records()) if r[BASIN_FIELD] == BASIN_VALUE)
geom = transform_geom("EPSG:4326", DST_CRS, sf.shape(idx).__geo_interface__)
with rasterio.open(DEM_IN) as src:
    dt, w, h = calculate_default_transform(src.crs, DST_CRS, src.width, src.height,
                                           *src.bounds, resolution=RES)
    demr = np.full((h, w), np.nan, np.float32)
    reproject(rasterio.band(src, 1), demr, src_transform=src.transform, src_crs=src.crs,
              dst_transform=dt, dst_crs=DST_CRS, src_nodata=src.nodata, dst_nodata=np.nan,
              resampling=Resampling.bilinear)
    prof = src.profile.copy()
prof.update(driver="GTiff", crs=DST_CRS, transform=dt, width=w, height=h, count=1,
            dtype="float32", nodata=ND, compress="deflate", tiled=True)
_tmp = OUT + "/_dem32.tif"
with rasterio.open(_tmp, "w", **prof) as ds:
    ds.write(np.where(np.isnan(demr), ND, demr).astype(np.float32), 1)
with rasterio.open(_tmp) as src:
    clip, ct = rio_mask(src, [geom], crop=True, nodata=ND, filled=True)
    clip = clip[0].astype(np.float32); cp = src.profile.copy()
os.remove(_tmp)
H, W = clip.shape; N = H * W
valid = clip != ND
elev = np.where(valid, clip, np.nan).astype(np.float64)
a, b, c, d_, e_, f_ = ct.a, ct.b, ct.c, ct.d, ct.e, ct.f
AFF = Affine(a, b, c, d_, e_, f_)
def writeR(name, arr, dtype, nodata):
    p = dict(driver="GTiff", height=H, width=W, count=1, dtype=dtype, crs=CRS,
             transform=AFF, nodata=nodata, compress="deflate", tiled=True)
    with rasterio.open(OUT + "/" + name, "w", **p) as ds: ds.write(arr.astype(dtype), 1)
def prj(path): open(path + ".prj", "w").write(WKT)
def xy(i): r = i // W; cc = i % W; return (a * (cc + 0.5) + c, e_ * (r + 0.5) + f_)
writeR("01_DEM_clip.tif", clip, "float32", ND)
log(1, f"DEM recortado {W}x{H}  |  {int(valid.sum())} celdas válidas  |  {DST_CRS} @ {RES} m")

# ---- 2. RELLENO (priority-flood + epsilon) -------------------------------------
P = np.full((H + 2, W + 2), np.nan); P[1:-1, 1:-1] = elev
PV = ~np.isnan(P); Wp = W + 2; flatP = P.ravel(); flatV = PV.ravel()
filled = flatP.copy(); closed = np.zeros(flatP.size, bool); closed[~flatV] = True
offs = [-Wp - 1, -Wp, -Wp + 1, -1, 1, Wp - 1, Wp, Wp + 1]
vidx = np.flatnonzero(flatV); isb = np.zeros(flatP.size, bool)
for o in offs:
    nb = vidx + o; isb[vidx[~flatV[nb]]] = True
pq = [(float(flatP[i]), int(i)) for i in np.flatnonzero(isb)]; heapq.heapify(pq)
for i in np.flatnonzero(isb): closed[i] = True
pit = deque(); EPS = 1e-3
while pq or pit:
    if pit: ci = pit.popleft(); ce = filled[ci]
    else:   ce, ci = heapq.heappop(pq)
    for o in offs:
        nb = ci + o
        if closed[nb]: continue
        closed[nb] = True; en = flatP[nb]
        if en <= ce + EPS: filled[nb] = ce + EPS; pit.append(nb)
        else:              filled[nb] = en; heapq.heappush(pq, (en, nb))
fill = filled.reshape(H + 2, W + 2)[1:-1, 1:-1]
writeR("03_DEM_fill.tif", np.where(valid, fill, ND), "float32", ND)
log(2, "Depresiones rellenadas (DEM hidrológicamente acondicionado)")

# ---- 3. DIRECCIÓN D8 + RECEPTOR + ACUMULACIÓN ----------------------------------
fillpad = np.full((H + 2, W + 2), np.nan); fillpad[1:-1, 1:-1] = fill
dist = np.array([np.sqrt(2), 1, np.sqrt(2), 1, 1, np.sqrt(2), 1, np.sqrt(2)])
esri = np.array([32, 64, 128, 16, 1, 8, 4, 2])
dy = np.array([-1, -1, -1, 0, 0, 1, 1, 1]); dx = np.array([-1, 0, 1, -1, 1, -1, 0, 1])
fdir = np.zeros((H, W), np.int32); recv = np.full(N, -1, np.int64); best = np.full((H, W), -1.0)
ys, xs = np.where(valid)
for k in range(8):
    nbv = fillpad[1 + ys + dy[k], 1 + xs + dx[k]]
    drop = (fill[ys, xs] - nbv) / dist[k]
    sel = np.where((drop > best[ys, xs]) & np.isfinite(nbv))[0]
    yy, xx = ys[sel], xs[sel]
    best[yy, xx] = drop[sel]; fdir[yy, xx] = esri[k]
    recv[yy * W + xx] = (yy + dy[k]) * W + (xx + dx[k])
recv[np.where(((best <= 0) & valid).ravel())[0]] = -1
writeR("04_Flow_direction.tif", np.where(valid, fdir, 0), "int32", 0)
acc = np.ones(N); acc[~valid.ravel()] = 0
order = np.argsort(-fill.ravel()); order = order[valid.ravel()[order]]
for cc in order:
    if recv[cc] >= 0: acc[recv[cc]] += acc[cc]
accg = np.where(valid, acc.reshape(H, W), np.nan)
writeR("05_Flow_accumulation.tif", np.where(valid, accg, ND), "float32", ND)
log(3, f"Dirección D8 + acumulación (máx = {int(np.nanmax(accg))} celdas)")

# ---- 4. RED DE DRENAJE + STRAHLER ----------------------------------------------
thc = int(round(THRESH_KM2 * 1e6 / (RES * RES)))
stream = (np.nan_to_num(accg) >= thc) & valid
writeR("07_Streams_raster.tif", np.where(stream, 1, 0).astype(np.int32), "int32", 0)
sflat = stream.ravel(); sidx = np.flatnonzero(sflat)
contrib = np.zeros(N, np.int32); rc = recv[sidx]
m = (rc >= 0) & sflat[np.where(rc >= 0, rc, 0)]; np.add.at(contrib, rc[m], 1)
topo = np.argsort(-fill.ravel()); topo = topo[sflat[topo]]
maxo = np.zeros(N, np.int32); cnt = np.zeros(N, np.int32); orderA = np.zeros(N, np.int32)
for cc in topo:
    o = 1 if contrib[cc] == 0 else (maxo[cc] if cnt[cc] == 1 else maxo[cc] + 1)
    orderA[cc] = o; r2 = recv[cc]
    if r2 >= 0 and sflat[r2]:
        if o > maxo[r2]: maxo[r2] = o; cnt[r2] = 1
        elif o == maxo[r2]: cnt[r2] += 1
strah = np.zeros((H, W), np.int32); strah.ravel()[sidx] = orderA[sidx]
writeR("08_Strahler_raster.tif", strah, "int32", 0)
maxorder = int(orderA.max())
log(4, f"Red de drenaje (umbral {THRESH_KM2} km² = {thc} celdas)  |  orden de Strahler máx = {maxorder}")

# ---- 5. VECTOR RED + CAUCE PRINCIPAL + OUTLET ----------------------------------
confl = contrib >= 2; starts = np.flatnonzero(((contrib == 0) | confl) & sflat)
def trace(s):
    p = [s]; cur = s
    while True:
        nx = recv[cur]
        if nx < 0 or not sflat[nx]: break
        p.append(nx)
        if confl[nx]: break
        cur = nx
    return p
wv = shapefile.Writer(OUT + "/09_Red_drenaje", shapeType=shapefile.POLYLINE)
wv.field("strahler", "N", 10, 0); wv.field("long_m", "N", 12, 1)
totlen = 0.0
for s in starts:
    p = trace(s)
    if len(p) < 2: continue
    pts = [xy(int(i)) for i in p]
    L = sum(math.dist(pts[k - 1], pts[k]) for k in range(1, len(pts)))
    wv.line([pts]); wv.record(int(orderA[s]) or 1, round(L, 1)); totlen += L
wv.close(); prj(OUT + "/09_Red_drenaje")
# distancia aguas abajo -> longest flow path
order_lh = np.argsort(fill.ravel()); order_lh = order_lh[valid.ravel()[order_lh]]
dout = np.zeros(N)
for cc in order_lh:
    r2 = recv[cc]
    if r2 >= 0:
        diag = abs(cc // W - r2 // W) == 1 and abs(cc % W - r2 % W) == 1
        dout[cc] = dout[r2] + RES * (np.sqrt(2) if diag else 1)
src = int(np.flatnonzero(valid.ravel())[np.argmax(dout[valid.ravel()])])
path = [src]; cur = src
while recv[cur] >= 0: cur = recv[cur]; path.append(cur)
pts = [xy(int(i)) for i in path]
Lmain = sum(math.dist(pts[k - 1], pts[k]) for k in range(1, len(pts)))
wm = shapefile.Writer(OUT + "/11_Cauce_principal", shapeType=shapefile.POLYLINE)
wm.field("tipo", "C", 30); wm.field("long_km", "N", 10, 2)
wm.line([pts]); wm.record("Longest flow path", round(Lmain / 1000, 2)); wm.close()
prj(OUT + "/11_Cauce_principal")
outlet = int(np.nanargmax(np.where(valid.ravel(), acc, np.nan)))
ox, oy = xy(outlet)
wo = shapefile.Writer(OUT + "/12_Outlet", shapeType=shapefile.POINT)
wo.field("acc_cells", "N", 12, 0); wo.field("area_km2", "N", 10, 2)
wo.point(ox, oy); wo.record(int(acc[outlet]), round(acc[outlet] * RES * RES / 1e6, 2))
wo.close(); prj(OUT + "/12_Outlet")
log(5, f"Cauce principal = {Lmain/1000:.2f} km  |  outlet drena {acc[outlet]*900/1e6:.0f} km²")

# ---- 6. PENDIENTE + HILLSHADE + CURVAS + ZONAS + LÍMITE -------------------------
zp = np.pad(np.where(valid, elev, np.nan), 1, mode="edge")
def sh(ddy, ddx): return zp[1 + ddy:1 + ddy + H, 1 + ddx:1 + ddx + W]
cen = np.where(valid, elev, np.nan)
nb = {k: np.where(np.isnan(v), cen, v) for k, v in
      dict(nw=sh(-1, -1), n=sh(-1, 0), ne=sh(-1, 1), w=sh(0, -1), e=sh(0, 1),
           sw=sh(1, -1), s=sh(1, 0), se=sh(1, 1)).items()}
dzdx = ((nb["ne"] + 2 * nb["e"] + nb["se"]) - (nb["nw"] + 2 * nb["w"] + nb["sw"])) / (8 * RES)
dzdy = ((nb["sw"] + 2 * nb["s"] + nb["se"]) - (nb["nw"] + 2 * nb["n"] + nb["ne"])) / (8 * RES)
srad = np.arctan(np.hypot(dzdx, dzdy))
writeR("06_Slope.tif", np.where(valid, np.degrees(srad), ND).astype("float32"), "float32", ND)
zen = np.radians(45); azr = np.radians(360 - 315 + 90); asp = np.arctan2(dzdy, -dzdx)
hsh = np.clip(255 * (np.cos(zen) * np.cos(srad) + np.sin(zen) * np.sin(srad) * np.cos(azr - asp)), 0, 255)
writeR("02_Hillshade.tif", np.where(valid, hsh, 0).astype("uint8"), "uint8", 0)
ev = elev[valid]; p33, p66 = np.nanpercentile(ev, [33.3333, 66.6667])
zones = np.zeros((H, W), np.int32)
zones[valid & (elev <= p33)] = 1
zones[valid & (elev > p33) & (elev <= p66)] = 2
zones[valid & (elev > p66)] = 3
writeR("13_Zonas_altimetricas.tif", zones, "int32", 0)
xs1 = a * (np.arange(W) + 0.5) + c; ys1 = e_ * (np.arange(H) + 0.5) + f_
cg = contour_generator(x=xs1, y=ys1, z=np.ma.masked_invalid(np.where(valid, elev, np.nan)))
wc = shapefile.Writer(OUT + "/10_Curvas_nivel", shapeType=shapefile.POLYLINE)
wc.field("elev_m", "N", 10, 1); wc.field("indice", "N", 1, 0)
for lv in np.arange(math.ceil(np.nanmin(ev) / CONTOUR_INT) * CONTOUR_INT, np.nanmax(ev), CONTOUR_INT):
    for ln in cg.lines(float(lv)):
        if len(ln) < 2: continue
        wc.line([[(float(x), float(y)) for x, y in ln]])
        wc.record(round(float(lv), 1), 1 if round(lv) % 250 == 0 else 0)
wc.close(); prj(OUT + "/10_Curvas_nivel")
def rings(g): return g["coordinates"] if g["type"] == "Polygon" else [r for poly in g["coordinates"] for r in poly]
wb = shapefile.Writer(OUT + "/00_Cuenca_Naposta", shapeType=shapefile.POLYGON)
wb.field("nombre", "C", 40); wb.field("area_km2", "N", 10, 1)
wb.poly([[(float(x), float(y)) for x, y in r] for r in rings(geom)])
wb.record("Napostá Grande", round(valid.sum() * RES * RES / 1e6, 1)); wb.close()
prj(OUT + "/00_Cuenca_Naposta")
log(6, "Pendiente, hillshade, curvas de nivel, zonas alta/media/baja y límite de cuenca")

# ---- 7. MORFOMETRÍA ------------------------------------------------------------
A = valid.sum() * RES * RES / 1e6
Pm = sum(math.dist(r[k - 1], r[k]) for r in rings(geom) for k in range(1, len(r))) / 1000
Dd = totlen / 1000 / A; Lkm = Lmain / 1000
Hsrc, Hout = float(fill.ravel()[src]), float(fill.ravel()[outlet])
S = max((Hsrc - Hout) / Lmain, 1e-4)
sl = np.degrees(srad)[valid]
rows = [("Área de la cuenca", f"{A:.1f}", "km²"), ("Perímetro", f"{Pm:.1f}", "km"),
 ("Cota máxima", f"{np.nanmax(ev):.1f}", "m"), ("Cota mínima", f"{np.nanmin(ev):.1f}", "m"),
 ("Cota media", f"{np.nanmean(ev):.1f}", "m"), ("Relieve", f"{np.nanmax(ev)-np.nanmin(ev):.1f}", "m"),
 ("Pendiente media cuenca", f"{np.mean(sl):.2f}", "°"),
 ("Pendiente media cuenca", f"{np.mean(np.tan(np.radians(sl)))*100:.1f}", "%"),
 ("Longitud total de cauces", f"{totlen/1000:.1f}", "km"), ("Densidad de drenaje", f"{Dd:.3f}", "km/km²"),
 ("Orden de la cuenca (Strahler)", f"{maxorder}", "-"), ("Longitud cauce principal", f"{Lkm:.2f}", "km"),
 ("Pendiente media cauce principal", f"{S*100:.2f}", "%"),
 ("Coef. compacidad Gravelius (Kc)", f"{0.2821*Pm/math.sqrt(A):.2f}", "-"),
 ("Factor de forma (Rf)", f"{A/Lkm**2:.3f}", "-"), ("Razón de elongación (Re)", f"{1.1284*math.sqrt(A)/Lkm:.3f}", "-"),
 ("Tc Kirpich", f"{0.01947*(Lmain**0.77)*(S**-0.385):.0f}", "min"),
 ("Tc Témez", f"{0.3*((Lkm/S**0.25)**0.76):.2f}", "h")]
with open(OUT + "/14_Parametros_morfometricos.csv", "w", encoding="utf-8") as fo:
    fo.write("Parametro;Valor;Unidad\n")
    for r_ in rows: fo.write(";".join(r_) + "\n")
log(7, f"Morfometría: A={A:.0f} km²  Dd={Dd:.2f}  Lcp={Lkm:.1f} km  Kc={0.2821*Pm/math.sqrt(A):.2f}  orden {maxorder}")

HDR = "<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>\n"
def _w(name, body): open(OUT + "/" + name, "w", encoding="utf-8").write(HDR + body)
def _pseudo(mn, mx, stops, g=2):
    it = "".join(f'<item value="{v}" color="{col}" label="{lab}" alpha="255"/>\n' for v, col, lab in stops)
    return (f'<qgis version="3.34.0" styleCategories="AllStyleCategories"><pipe>'
      f'<rasterrenderer type="singlebandpseudocolor" band="1" classificationMin="{mn}" classificationMax="{mx}" opacity="1" alphaBand="-1" nodataColor="">'
      f'<rastershader><colorrampshader maximumValue="{mx}" minimumValue="{mn}" colorRampType="INTERPOLATED" classificationMode="1" clip="0">'
      f'{it}</colorrampshader></rastershader></rasterrenderer><blendMode>0</blendMode></pipe>'
      f'<layerGeometryType>{g}</layerGeometryType></qgis>\n')
def _pal(entries):
    e = "".join(f'<paletteEntry value="{v}" color="{col}" label="{lab}" alpha="255"/>\n' for v, col, lab in entries)
    return (f'<qgis version="3.34.0" styleCategories="AllStyleCategories"><pipe>'
      f'<rasterrenderer type="paletted" band="1" opacity="1" alphaBand="-1" nodataColor="">'
      f'<colorPalette>{e}</colorPalette></rasterrenderer><blendMode>0</blendMode></pipe>'
      f'<layerGeometryType>2</layerGeometryType></qgis>\n')
def _gray(mn, mx):
    return (f'<qgis version="3.34.0" styleCategories="AllStyleCategories"><pipe>'
      f'<rasterrenderer type="singlebandgray" band="1" grayBand="1" gradient="BlackToWhite" opacity="1" alphaBand="-1" nodataColor="">'
      f'<contrastEnhancement><minValue>{mn}</minValue><maxValue>{mx}</maxValue>'
      f'<algorithm>StretchToMinimumMaximum</algorithm></contrastEnhancement></rasterrenderer>'
      f'<blendMode>0</blendMode></pipe><layerGeometryType>2</layerGeometryType></qgis>\n')
def _line(rgba, wd):
    return (f'<qgis version="3.34.0" styleCategories="Symbology"><renderer-v2 type="singleSymbol">'
      f'<symbols><symbol type="line" name="0"><layer class="SimpleLine"><Option type="Map">'
      f'<Option type="QString" name="line_color" value="{rgba}"/>'
      f'<Option type="QString" name="line_width" value="{wd}"/>'
      f'<Option type="QString" name="line_width_unit" value="MM"/>'
      f'<Option type="QString" name="capstyle" value="round"/><Option type="QString" name="joinstyle" value="round"/>'
      f'</Option></layer></symbol></symbols></renderer-v2><layerGeometryType>1</layerGeometryType></qgis>\n')
def _point(rgba, sz):
    return (f'<qgis version="3.34.0" styleCategories="Symbology"><renderer-v2 type="singleSymbol">'
      f'<symbols><symbol type="marker" name="0"><layer class="SimpleMarker"><Option type="Map">'
      f'<Option type="QString" name="name" value="circle"/><Option type="QString" name="color" value="{rgba}"/>'
      f'<Option type="QString" name="outline_color" value="0,0,0,255"/>'
      f'<Option type="QString" name="size" value="{sz}"/><Option type="QString" name="size_unit" value="MM"/>'
      f'</Option></layer></symbol></symbols></renderer-v2><layerGeometryType>0</layerGeometryType></qgis>\n')
def _fillout(rgba, wd):
    return (f'<qgis version="3.34.0" styleCategories="Symbology"><renderer-v2 type="singleSymbol">'
      f'<symbols><symbol type="fill" name="0"><layer class="SimpleFill"><Option type="Map">'
      f'<Option type="QString" name="style" value="no"/><Option type="QString" name="color" value="0,0,0,0"/>'
      f'<Option type="QString" name="outline_color" value="{rgba}"/>'
      f'<Option type="QString" name="outline_width" value="{wd}"/>'
      f'<Option type="QString" name="outline_width_unit" value="MM"/>'
      f'</Option></layer></symbol></symbols></renderer-v2><layerGeometryType>2</layerGeometryType></qgis>\n')
def _grad(mo):
    blues = ["#bdd7e7","#6baed6","#3182bd","#08519c","#08306b","#062247","#04132b"]; wds = [0.26,0.45,0.65,0.9,1.2,1.5,1.8]
    def sy(i, hx, wd):
        r, g, bb = int(hx[1:3],16), int(hx[3:5],16), int(hx[5:7],16)
        return (f'<symbol type="line" name="{i}"><layer class="SimpleLine"><Option type="Map">'
          f'<Option type="QString" name="line_color" value="{r},{g},{bb},255"/>'
          f'<Option type="QString" name="line_width" value="{wd}"/>'
          f'<Option type="QString" name="line_width_unit" value="MM"/>'
          f'<Option type="QString" name="capstyle" value="round"/><Option type="QString" name="joinstyle" value="round"/>'
          f'</Option></layer></symbol>')
    rg = "".join(f'<range lower="{k-0.5:.6f}" upper="{k+0.5:.6f}" label="Orden {k}" symbol="{k-1}" render="true"/>' for k in range(1, mo+1))
    sy_ = "".join(sy(k-1, blues[k-1], wds[k-1]) for k in range(1, mo+1))
    return (f'<qgis version="3.34.0" styleCategories="Symbology">'
      f'<renderer-v2 type="graduatedSymbol" attr="strahler" graduatedMethod="GraduatedColor">'
      f'<ranges>{rg}</ranges><symbols>{sy_}</symbols><source-symbol>{sy(0, blues[0], wds[0])}</source-symbol>'
      f'<rotation/><sizescale/></renderer-v2><layerGeometryType>1</layerGeometryType></qgis>\n')
_dem = [("0","#27531a","0 m"),("50","#4a9b3c","50"),("150","#8fc866","150"),("300","#d9e89a","300"),
        ("500","#e3c47a","500"),("750","#b5825a","750"),("1000","#8a5a3c","1000"),("1235","#f2f2f2","1235")]
_w("01_DEM_clip.qml", _pseudo(0,1235,_dem)); _w("03_DEM_fill.qml", _pseudo(0,1235,_dem))
_w("02_Hillshade.qml", _gray(0,255))
_accm = int(np.nanmax(accg))
_w("05_Flow_accumulation.qml", _pseudo(1,_accm,[("1","#f7fbff","1"),("10","#d2e3f3","10"),("100","#9ecae1","100"),
   ("1000","#4292c6","1.000"),("10000","#2171b5","10.000"),("100000","#08519c","100.000"),(str(_accm),"#08306b","outlet")]))
_w("06_Slope.qml", _pseudo(0,35,[("0","#1a9850","0°"),("2","#91cf60","2°"),("5","#d9ef8b","5°"),
   ("10","#fee08b","10°"),("20","#fc8d59","20°"),("35","#d73027","≥35°")]))
_w("04_Flow_direction.qml", _pal([("1","#e41a1c","1 E"),("2","#ff7f00","2 SE"),("4","#ffff33","4 S"),("8","#4daf4a","8 SO"),
   ("16","#377eb8","16 O"),("32","#984ea3","32 NO"),("64","#a65628","64 N"),("128","#f781bf","128 NE")]))
_w("07_Streams_raster.qml", _pal([("1","#08519c","Cauce")]))
_blues7 = ["#bdd7e7","#6baed6","#3182bd","#08519c","#08306b","#062247","#04132b"]
_w("08_Strahler_raster.qml", _pal([(str(k), _blues7[min(k-1,6)], f"Orden {k}") for k in range(1, max(maxorder,1)+1)]))
_w("09_Red_drenaje.qml", _grad(max(maxorder,1)))
_w("10_Curvas_nivel.qml", _line("140,90,40,180","0.2"))
_w("11_Cauce_principal.qml", _line("8,48,107,255","1.1"))
_w("12_Outlet.qml", _point("227,26,28,255","4"))
_w("13_Zonas_altimetricas.qml", _pal([("1","#41ab5d","Baja"),("2","#fed976","Media"),("3","#a63603","Alta")]))
_w("00_Cuenca_Naposta.qml", _fillout("0,0,0,255","0.6"))
log(8, "Estilos .qml escritos junto a cada capa")
print("\nLISTO. En QGIS, cargá los archivos 00..13 en orden; el estilo se aplica automáticamente.")
