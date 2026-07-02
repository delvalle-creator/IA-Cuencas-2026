# -*- coding: utf-8 -*-
# ============================================================================
#  TP1 — IA aplicada a Hidrografía e Hidrología
#  Copyright (c) 2026 Héctor Francisco del Valle
#  Licencia: CC BY-NC-SA 4.0  (https://creativecommons.org/licenses/by-nc-sa/4.0/)
#  Datos de elevacion de terceros (FABDEM / TanDEM-X / IGN): ver NOTICE.md
#  Atribucion requerida. Uso no comercial. Compartir igual.
# ============================================================================
"""
============================================================================
 LEER Y COMPARAR METADATOS DE VARIOS DTM / DEM   (version para QGIS)
============================================================================
 Curso de posgrado - IA aplicada a Hidrografia e Hidrologia (TP1)

 Esta version usa GDAL (osgeo), que YA VIENE INSTALADO con QGIS, asi que
 corre en la Consola de Python de QGIS sin instalar nada extra.

 ---------------------------------------------------------------------------
 COMO EJECUTARLO EN QGIS:
   1. Abri QGIS.
   2. Menu Complementos -> Consola de Python (o Ctrl+Alt+P).
   3. En la consola, hace clic en el boton "Mostrar editor" (icono de hoja).
   4. En el editor, abri este archivo y apreta el boton verde "Ejecutar
      script" (Run). Asi QGIS reconoce la ubicacion del archivo.
   5. Mira el resultado en la consola.

 Si lo PEGAS directo en la consola (sin usar el editor), QGIS no sabe donde
 esta el archivo: en ese caso, completa a mano la variable RUTA_TP1 de abajo.
============================================================================
"""

import os, sys, csv, math
from osgeo import gdal, osr

gdal.UseExceptions()
# Evita que GDAL cree archivos .aux.xml sueltos junto a los datos:
gdal.SetConfigOption("GDAL_PAM_ENABLED", "NO")

# ===========================================================================
#  CONFIGURACION
# ===========================================================================
# Intenta ubicarse solo a partir de donde esta este archivo (.../TP1/03_Scripts_QGIS).
try:
    CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
    RUTA_TP1 = os.path.dirname(CARPETA_SCRIPT)
except NameError:
    # Si lo pegaste en la consola y falla, escribi a mano la ruta de tu TP1:
    RUTA_TP1 = r"G:\IA APLICADA A HIDROGRAFIA E HIDROLOGIA\PERSONAL\02_PRACTICA\TP1"

# Carpeta de ENTRADA (recortes corregidos / homogeneos):
CARPETA = os.path.join(RUTA_TP1, "05_DTMs_corregidos")

# Para ver PRIMERO el error, descomenta esta linea (materiales originales):
# CARPETA = os.path.join(RUTA_TP1, "01_Materiales")

# Carpeta de SALIDA:
CARPETA_SALIDA = os.path.join(RUTA_TP1, "04_Metadatos")

RECURSIVO = False
EXTENSIONES = (".tif", ".tiff", ".img", ".vrt", ".asc", ".dem")
# ===========================================================================


def metros_por_grado(lat_media):
    lat = math.radians(lat_media)
    m_lat = 111132.92 - 559.82 * math.cos(2*lat) + 1.175 * math.cos(4*lat)
    m_lon = 111412.84 * math.cos(lat) - 93.5 * math.cos(3*lat)
    return m_lon, m_lat


def buscar_rasters(carpeta, recursivo):
    out = []
    if recursivo:
        for raiz, _d, archivos in os.walk(carpeta):
            for a in archivos:
                if a.lower().endswith(EXTENSIONES):
                    out.append(os.path.join(raiz, a))
    else:
        for a in os.listdir(carpeta):
            r = os.path.join(carpeta, a)
            if os.path.isfile(r) and a.lower().endswith(EXTENSIONES):
                out.append(r)
    return sorted(out)


def leer_metadatos(ruta):
    ds = gdal.Open(ruta)
    if ds is None:
        raise RuntimeError("GDAL no pudo abrir el archivo")
    gt = ds.GetGeoTransform()
    ancho, alto = ds.RasterXSize, ds.RasterYSize
    res_x = gt[1]
    res_y = -gt[5]
    oeste = gt[0]
    norte = gt[3]
    este = oeste + ancho * res_x
    sur = norte - alto * res_y
    lat_media = (norte + sur) / 2.0
    m_lon, m_lat = metros_por_grado(lat_media)

    # EPSG
    epsg = None
    proj = ds.GetProjection()
    if proj:
        srs = osr.SpatialReference(); srs.ImportFromWkt(proj)
        epsg = srs.GetAuthorityCode(None)

    banda = ds.GetRasterBand(1)
    nodata = banda.GetNoDataValue()
    tipo = gdal.GetDataTypeName(banda.DataType)
    # Estadisticas (GDAL respeta el NoData). force=True las calcula.
    try:
        vmin, vmax, vmean, vstd = banda.GetStatistics(False, True)
    except Exception:
        vmin = vmax = vmean = vstd = float("nan")

    registro = ds.GetMetadataItem("AREA_OR_POINT") or "-"
    compresion = ds.GetMetadataItem("COMPRESSION", "IMAGE_STRUCTURE") or "ninguna"
    driver = ds.GetDriver().ShortName

    datos = {
        "archivo": os.path.basename(ruta),
        "formato": driver,
        "EPSG": epsg,
        "ancho_px": ancho,
        "alto_px": alto,
        "total_px": ancho * alto,
        "res_grados": round(res_x, 10),
        "res_arcseg": round(res_x * 3600, 4),
        "res_m_EO": round(res_x * m_lon, 2),
        "res_m_NS": round(res_y * m_lat, 2),
        "oeste": round(oeste, 6),
        "sur": round(sur, 6),
        "este": round(este, 6),
        "norte": round(norte, 6),
        "tipo_dato": tipo,
        "NoData": nodata,
        "registro_pixel": registro,
        "compresion": compresion,
        "tamano_MB": round(os.path.getsize(ruta) / 1e6, 2),
        "elev_min": round(vmin, 2),
        "elev_max": round(vmax, 2),
        "elev_media": round(vmean, 2),
        "elev_std": round(vstd, 2),
    }
    ds = None
    return datos


def control_homogeneidad(filas):
    adv = []
    def distintos(clave, redondeo=None):
        vals = []
        for f in filas:
            v = f[clave]
            if redondeo is not None and isinstance(v, float):
                v = round(v, redondeo)
            vals.append(v)
        return sorted(set(vals), key=lambda x: str(x))

    if len(distintos("EPSG")) > 1:
        adv.append("Hay mas de un CRS/EPSG distinto: " +
                   ", ".join(str(x) for x in distintos("EPSG")))
    if len(distintos("res_grados", 10)) > 1:
        adv.append("Hay mas de una RESOLUCION distinta (grados): " +
                   ", ".join(str(x) for x in distintos("res_grados", 10)))
    exts = set((f["oeste"], f["sur"], f["este"], f["norte"]) for f in filas)
    if len(exts) > 1:
        adv.append("Las EXTENSIONES no coinciden entre todos los archivos.")
    tams = set((f["ancho_px"], f["alto_px"]) for f in filas)
    if len(tams) > 1:
        adv.append("Los TAMANOS en pixeles no coinciden.")
    if len(distintos("NoData")) > 1:
        adv.append("Hay mas de un valor de NoData: " +
                   ", ".join(str(x) for x in distintos("NoData")))
    if len(distintos("registro_pixel")) > 1:
        adv.append("Hay mas de un REGISTRO de pixel (Area vs Point): " +
                   ", ".join(str(x) for x in distintos("registro_pixel")))
    if len(distintos("tipo_dato")) > 1:
        adv.append("Hay mas de un TIPO de dato: " +
                   ", ".join(str(x) for x in distintos("tipo_dato")))
    return adv


def main():
    print("=" * 70)
    print(" LECTURA DE METADATOS DE DTM / DEM  (QGIS / GDAL)")
    print("=" * 70)
    print("Carpeta de entrada :", CARPETA)
    print("Carpeta de salida  :", CARPETA_SALIDA)
    print("-" * 70)

    if not os.path.isdir(CARPETA):
        print("ERROR: no existe la carpeta de entrada:", CARPETA)
        print("Edita la variable CARPETA (o RUTA_TP1) al inicio del script.")
        return

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    rasters = buscar_rasters(CARPETA, RECURSIVO)
    if not rasters:
        print("No se encontraron raster con extensiones:", ", ".join(EXTENSIONES))
        return
    print("Archivos raster encontrados:", len(rasters), "\n")

    filas = []
    for ruta in rasters:
        try:
            filas.append(leer_metadatos(ruta))
            print("  [OK] ", os.path.basename(ruta))
        except Exception as e:
            print("  [ERROR]", os.path.basename(ruta), "->", e)

    if not filas:
        print("No se pudo leer ningun archivo.")
        return

    # Tabla en pantalla
    cols = ["archivo", "EPSG", "ancho_px", "alto_px", "res_arcseg", "res_m_NS",
            "NoData", "registro_pixel", "tipo_dato", "elev_min", "elev_max",
            "elev_media", "tamano_MB"]
    anchos = {c: max(len(c), max(len(str(f[c])) for f in filas)) for c in cols}
    print("\n" + "=" * 70)
    print(" RESUMEN DE METADATOS")
    print("=" * 70)
    print("  ".join(c.ljust(anchos[c]) for c in cols))
    for f in filas:
        print("  ".join(str(f[c]).ljust(anchos[c]) for c in cols))

    # Guardar CSV (se abre con Excel sin problema)
    # El nombre del archivo se mantiene segun el caso (corregido / con error)
    # y asi coincide con los CSV ya entregados en 04_Metadatos.
    _ETIQUETAS = {"05_DTMs_corregidos": "DTM_DEM_aoi",
                  "01_Materiales": "DTM_DEM_aoi_CON_ERROR"}
    _clave = os.path.basename(CARPETA.rstrip("/\\"))
    base = "metadatos_" + _ETIQUETAS.get(_clave, _clave)
    ruta_csv = os.path.join(CARPETA_SALIDA, base + ".csv")
    campos = list(filas[0].keys())
    with open(ruta_csv, "w", newline="", encoding="utf-8-sig") as fcsv:
        w = csv.DictWriter(fcsv, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)
    print("\nGuardado:", ruta_csv)

    # Control de homogeneidad
    print("\n" + "=" * 70)
    adv = control_homogeneidad(filas)
    if adv:
        print(" /!\\  ADVERTENCIAS DE HOMOGENEIDAD")
        print("=" * 70)
        for a in adv:
            print("  - " + a)
        print("\n  >> Los DTM NO son directamente comparables celda a celda.")
        print("     Revisa resolucion, CRS, extension y NoData antes de operar.")
    else:
        print(" OK  Todos los DTM son homogeneos (misma grilla).")
        print("=" * 70)
    print("\nListo.")


main()
