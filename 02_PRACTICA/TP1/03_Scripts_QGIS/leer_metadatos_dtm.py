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
 LEER Y COMPARAR METADATOS DE VARIOS DTM / DEM   (version Python + rasterio)
============================================================================
 Curso de posgrado - IA aplicada a Hidrografia e Hidrologia (TP1)

 Que hace:
   1. Recorre una carpeta y detecta los archivos raster (DTM/DEM).
   2. Lee los metadatos de cada uno (CRS, tamano, resolucion, extension,
      NoData, registro de pixel, estadisticas, etc.).
   3. Muestra una tabla en la pantalla.
   4. Guarda los resultados en CSV y Excel.
   5. AVISA si los DTM NO son homogeneos entre si (distinta resolucion,
      CRS, extension, NoData...). Ese es el punto clave del ejercicio.

 ---------------------------------------------------------------------------
 INSTALAR LIBRERIAS (una sola vez), desde la consola:
       pip install rasterio numpy pandas openpyxl
 EJECUTAR:
       python leer_metadatos_dtm.py
 ---------------------------------------------------------------------------
 NOTA: esta version usa 'rasterio'. Para correr dentro de la CONSOLA PYTHON
 DE QGIS sin instalar nada, usa el archivo 'leer_metadatos_dtm_QGIS.py'.
============================================================================
"""

# ===========================================================================
#  CONFIGURACION  (lo unico que se podria necesitar tocar)
# ===========================================================================
import os

# Rutas calculadas automaticamente a partir de la ubicacion de este archivo
# (.../TP1/03_Scripts_QGIS). Funciona aunque cambie la letra de unidad (G:, D:, ...).
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_TP1    = os.path.dirname(CARPETA_SCRIPT)          # sube un nivel: .../TP1

# Carpeta de ENTRADA: recortes corregidos / homogeneos (caso correcto).
CARPETA = os.path.join(CARPETA_TP1, "05_DTMs_corregidos")

# Carpeta de SALIDA: donde se guardan los resultados (CSV y Excel).
CARPETA_SALIDA = os.path.join(CARPETA_TP1, "04_Metadatos")

# -------------------------------------------------------------------------
# PARA LA CLASE: para ver PRIMERO el error de los tiles equivocados,
# descomenta la linea de abajo (quitale el '#'). Apunta a la carpeta con
# los recortes originales sin corregir. Para volver al caso correcto,
# volve a comentarla.
# CARPETA = os.path.join(CARPETA_TP1, "01_Materiales")
# -------------------------------------------------------------------------

# Buscar tambien dentro de subcarpetas? True = si, False = no.
RECURSIVO = False

# Extensiones de archivo que se consideran raster (DTM/DEM).
EXTENSIONES = (".tif", ".tiff", ".img", ".vrt", ".asc", ".dem")

# Los nombres de salida se mantienen segun el caso (corregido / con error),
# asi el caso "con error" y el "corregido" no se pisan entre si.
_ETIQUETAS = {"05_DTMs_corregidos": "DTM_DEM_aoi",
              "01_Materiales": "DTM_DEM_aoi_CON_ERROR"}
_CLAVE = os.path.basename(CARPETA.rstrip("/\\"))
_BASE_NOMBRE = "metadatos_" + _ETIQUETAS.get(_CLAVE, _CLAVE)
NOMBRE_CSV   = _BASE_NOMBRE + ".csv"
NOMBRE_EXCEL = _BASE_NOMBRE + ".xlsx"
# ===========================================================================


# --- Librerias necesarias --------------------------------------------------
import math
import sys

try:
    import numpy as np
    import pandas as pd
    import rasterio
except ImportError as e:
    print("ERROR: falta una libreria. Instalala con:")
    print("    pip install rasterio numpy pandas openpyxl")
    print("Detalle:", e)
    sys.exit(1)


# --- Funciones auxiliares --------------------------------------------------

def metros_por_grado(lat_media):
    """Cuantos metros mide 1 grado de longitud y de latitud a una latitud
    dada. Sirve para pasar la resolucion (grados) a metros. Es aproximado."""
    lat = math.radians(lat_media)
    m_lat = 111132.92 - 559.82 * math.cos(2 * lat) + 1.175 * math.cos(4 * lat)
    m_lon = 111412.84 * math.cos(lat) - 93.5 * math.cos(3 * lat)
    return m_lon, m_lat


def buscar_rasters(carpeta, recursivo):
    """Devuelve la lista de archivos raster encontrados en la carpeta."""
    encontrados = []
    if recursivo:
        for raiz, _dirs, archivos in os.walk(carpeta):
            for a in archivos:
                if a.lower().endswith(EXTENSIONES):
                    encontrados.append(os.path.join(raiz, a))
    else:
        for a in os.listdir(carpeta):
            ruta = os.path.join(carpeta, a)
            if os.path.isfile(ruta) and a.lower().endswith(EXTENSIONES):
                encontrados.append(ruta)
    return sorted(encontrados)


def leer_metadatos(ruta):
    """Abre un raster y devuelve un diccionario con sus metadatos."""
    with rasterio.open(ruta) as ds:
        b = ds.bounds
        res_x = ds.res[0]                      # tamano de celda en grados (lon)
        lat_media = (b.top + b.bottom) / 2.0
        m_lon, m_lat = metros_por_grado(lat_media)

        # Estadisticas de la banda 1 ignorando el NoData
        banda1 = ds.read(1).astype("float64")
        if ds.nodata is not None:
            validos = banda1[banda1 != ds.nodata]
        else:
            validos = banda1.ravel()

        if validos.size > 0:
            vmin, vmax = float(np.min(validos)), float(np.max(validos))
            vmean, vstd = float(np.mean(validos)), float(np.std(validos))
        else:
            vmin = vmax = vmean = vstd = float("nan")

        epsg = ds.crs.to_epsg() if ds.crs else None

        datos = {
            "archivo": os.path.basename(ruta),
            "formato": ds.driver,
            "CRS": ds.crs.to_string() if ds.crs else "SIN CRS",
            "EPSG": epsg,
            "ancho_px": ds.width,
            "alto_px": ds.height,
            "total_px": ds.width * ds.height,
            "res_grados": round(res_x, 10),
            "res_arcseg": round(res_x * 3600, 4),
            "res_m_EO": round(res_x * m_lon, 2),
            "res_m_NS": round(ds.res[1] * m_lat, 2),
            "oeste": round(b.left, 6),
            "sur": round(b.bottom, 6),
            "este": round(b.right, 6),
            "norte": round(b.top, 6),
            "bandas": ds.count,
            "tipo_dato": ds.dtypes[0],
            "NoData": ds.nodata,
            "registro_pixel": ds.tags().get("AREA_OR_POINT", "-"),
            "compresion": ds.compression.value if ds.compression else "ninguna",
            "tiled": ds.is_tiled,
            "tamano_MB": round(os.path.getsize(ruta) / 1e6, 2),
            "px_validos": int(validos.size),
            "elev_min": round(vmin, 2),
            "elev_max": round(vmax, 2),
            "elev_media": round(vmean, 2),
            "elev_std": round(vstd, 2),
        }
    return datos


def control_homogeneidad(df):
    """Compara los DTM entre si y devuelve una lista de advertencias."""
    advertencias = []

    if df["EPSG"].nunique(dropna=False) > 1:
        advertencias.append("Hay mas de un CRS/EPSG distinto: " +
                            ", ".join(str(x) for x in df["EPSG"].unique()))

    resoluciones = df["res_grados"].round(10).unique()
    if len(resoluciones) > 1:
        advertencias.append("Hay mas de una RESOLUCION distinta (grados): " +
                            ", ".join(str(r) for r in sorted(resoluciones)))

    ext = df[["oeste", "sur", "este", "norte"]].round(6).drop_duplicates()
    if len(ext) > 1:
        advertencias.append("Las EXTENSIONES no coinciden entre todos los archivos.")

    tam = df[["ancho_px", "alto_px"]].drop_duplicates()
    if len(tam) > 1:
        advertencias.append("Los TAMANOS en pixeles no coinciden.")

    if df["NoData"].nunique(dropna=False) > 1:
        advertencias.append("Hay mas de un valor de NoData: " +
                            ", ".join(str(x) for x in df["NoData"].unique()))

    if df["registro_pixel"].nunique(dropna=False) > 1:
        advertencias.append("Hay mas de un REGISTRO de pixel (Area vs Point): " +
                            ", ".join(str(x) for x in df["registro_pixel"].unique()))

    if df["tipo_dato"].nunique(dropna=False) > 1:
        advertencias.append("Hay mas de un TIPO de dato: " +
                            ", ".join(str(x) for x in df["tipo_dato"].unique()))

    return advertencias


# --- Programa principal ----------------------------------------------------

def main():
    print("=" * 70)
    print(" LECTURA DE METADATOS DE DTM / DEM")
    print("=" * 70)
    print("Carpeta de entrada :", CARPETA)
    print("Carpeta de salida  :", CARPETA_SALIDA)
    print("Busqueda recursiva :", RECURSIVO)
    print("-" * 70)

    if not os.path.isdir(CARPETA):
        print("ERROR: no existe la carpeta de entrada:", CARPETA)
        print("Edita la variable CARPETA al inicio del script.")
        sys.exit(1)

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    rasters = buscar_rasters(CARPETA, RECURSIVO)
    if not rasters:
        print("No se encontraron raster con las extensiones:", ", ".join(EXTENSIONES))
        sys.exit(0)
    print("Archivos raster encontrados:", len(rasters))
    print()

    filas = []
    for ruta in rasters:
        try:
            filas.append(leer_metadatos(ruta))
            print("  [OK] ", os.path.basename(ruta))
        except Exception as e:
            print("  [ERROR] no se pudo leer", os.path.basename(ruta), "->", e)

    if not filas:
        print("No se pudo leer ningun archivo.")
        sys.exit(1)

    df = pd.DataFrame(filas)

    cols_resumen = ["archivo", "EPSG", "ancho_px", "alto_px", "res_arcseg",
                    "res_m_NS", "NoData", "registro_pixel", "tipo_dato",
                    "elev_min", "elev_max", "elev_media", "tamano_MB"]
    print("\n" + "=" * 70)
    print(" RESUMEN DE METADATOS")
    print("=" * 70)
    with pd.option_context("display.max_columns", None,
                           "display.width", 200,
                           "display.max_colwidth", 30):
        print(df[cols_resumen].to_string(index=False))

    ruta_csv = os.path.join(CARPETA_SALIDA, NOMBRE_CSV)
    df.to_csv(ruta_csv, index=False, encoding="utf-8-sig")
    print("\nGuardado:", ruta_csv)
    try:
        ruta_xlsx = os.path.join(CARPETA_SALIDA, NOMBRE_EXCEL)
        df.to_excel(ruta_xlsx, index=False)
        print("Guardado:", ruta_xlsx)
    except Exception as e:
        print("(No se pudo crear el Excel; instala openpyxl. Detalle:", e, ")")

    print("\n" + "=" * 70)
    advertencias = control_homogeneidad(df)
    if advertencias:
        print(" /!\\  ADVERTENCIAS DE HOMOGENEIDAD")
        print("=" * 70)
        for a in advertencias:
            print("  - " + a)
        print("\n  >> Los DTM NO son directamente comparables celda a celda.")
        print("     Revisa resolucion, CRS, extension y NoData antes de operar.")
    else:
        print(" OK  Todos los DTM son homogeneos (misma grilla).")
        print("=" * 70)

    print("\nListo.")


if __name__ == "__main__":
    main()
