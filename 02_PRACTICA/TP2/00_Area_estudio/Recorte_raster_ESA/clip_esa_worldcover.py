#!/usr/bin/env python3
"""
Descarga y recorta ESA WorldCover 10 m 2021 v200 con un AOI vectorial.

Uso recomendado para este paquete:
  python clip_esa_worldcover.py --aoi AOI_Naposta_Grande_shp.zip --out outputs

También se puede correr sin descargar, usando un tile ya existente:
  python clip_esa_worldcover.py --aoi AOI_Naposta_Grande_shp.zip --tile-dir data --skip-download --out outputs
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.mask import mask
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject
import requests
from shapely.geometry import box, mapping

S3_URL_PREFIX = "https://esa-worldcover.s3.eu-central-1.amazonaws.com"
VERSION = "v200"
YEAR = "2021"
LAYER = "Map"
NODATA = 0

CLASSES = {
    10: {"class_en": "Tree cover", "class_es": "Cobertura arbórea", "color": "#006400"},
    20: {"class_en": "Shrubland", "class_es": "Matorral / arbustal", "color": "#ffbb22"},
    30: {"class_en": "Grassland", "class_es": "Pastizal / herbáceas", "color": "#ffff4c"},
    40: {"class_en": "Cropland", "class_es": "Cultivos", "color": "#f096ff"},
    50: {"class_en": "Built-up", "class_es": "Construido / urbano", "color": "#fa0000"},
    60: {"class_en": "Bare / sparse vegetation", "class_es": "Suelo desnudo o vegetación escasa", "color": "#b4b4b4"},
    70: {"class_en": "Snow and ice", "class_es": "Nieve y hielo", "color": "#f0f0f0"},
    80: {"class_en": "Permanent water bodies", "class_es": "Cuerpos de agua permanentes", "color": "#0064c8"},
    90: {"class_en": "Herbaceous wetland", "class_es": "Humedal herbáceo", "color": "#0096a0"},
    95: {"class_en": "Mangroves", "class_es": "Manglares", "color": "#00cf75"},
    100: {"class_en": "Moss and lichen", "class_es": "Musgos y líquenes", "color": "#fae6a0"},
}


def _hex_to_rgba(hex_color: str) -> tuple[int, int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255


def tile_name(lat_ll: int, lon_ll: int) -> str:
    ns = "N" if lat_ll >= 0 else "S"
    ew = "E" if lon_ll >= 0 else "W"
    return f"{ns}{abs(int(lat_ll)):02d}{ew}{abs(int(lon_ll)):03d}"


def tile_lower_lefts(bounds: Tuple[float, float, float, float]) -> List[Tuple[int, int]]:
    """Return lower-left lat/lon tile origins for 3x3-degree WorldCover tiles."""
    minx, miny, maxx, maxy = bounds
    eps = 1e-12
    lon_start = math.floor(minx / 3.0) * 3
    lon_end = math.floor((maxx - eps) / 3.0) * 3
    lat_start = math.floor(miny / 3.0) * 3
    lat_end = math.floor((maxy - eps) / 3.0) * 3
    out = []
    lon = lon_start
    while lon <= lon_end:
        lat = lat_start
        while lat <= lat_end:
            out.append((int(lat), int(lon)))
            lat += 3
        lon += 3
    return out


def worldcover_url(tile: str) -> str:
    return f"{S3_URL_PREFIX}/{VERSION}/{YEAR}/map/ESA_WorldCover_10m_{YEAR}_{VERSION}_{tile}_{LAYER}.tif"


def read_aoi(aoi_path: Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(str(aoi_path))
    if gdf.empty:
        raise ValueError("El AOI no contiene geometrías.")
    if gdf.crs is None:
        raise ValueError("El AOI no tiene CRS definido. Asigne un CRS antes de ejecutar el recorte.")
    gdf = gdf[gdf.geometry.notna()].copy()
    gdf["geometry"] = gdf.geometry.make_valid()
    return gdf.to_crs("EPSG:4326")


def download_file(url: str, out_path: Path, overwrite: bool = False) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and out_path.stat().st_size > 0 and not overwrite:
        print(f"Usando archivo existente: {out_path}")
        return out_path
    tmp = out_path.with_suffix(out_path.suffix + ".part")
    print(f"Descargando: {url}")
    with requests.get(url, stream=True, timeout=(20, 120)) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        done = 0
        chunk_mb = 0
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                f.write(chunk)
                done += len(chunk)
                new_chunk_mb = done // (25 * 1024 * 1024)
                if new_chunk_mb != chunk_mb:
                    chunk_mb = new_chunk_mb
                    if total:
                        print(f"  {done/1024/1024:.1f} MB / {total/1024/1024:.1f} MB")
                    else:
                        print(f"  {done/1024/1024:.1f} MB")
    tmp.replace(out_path)
    return out_path


def write_clip_epsg4326(tile_paths: List[Path], aoi: gpd.GeoDataFrame, out_tif: Path) -> Path:
    out_tif.parent.mkdir(parents=True, exist_ok=True)
    geoms = [mapping(geom) for geom in aoi.geometry]
    clipped_paths: List[Path] = []
    for tile_path in tile_paths:
        tmp_path = out_tif.parent / f"_tmp_clip_{tile_path.stem}.tif"
        with rasterio.open(tile_path) as src:
            aoi_src = aoi.to_crs(src.crs)
            out_arr, out_transform = mask(src, [mapping(g) for g in aoi_src.geometry], crop=True, nodata=NODATA, filled=True)
            meta = src.meta.copy()
            meta.update({
                "driver": "GTiff",
                "height": out_arr.shape[1],
                "width": out_arr.shape[2],
                "transform": out_transform,
                "count": 1,
                "dtype": "uint8",
                "nodata": NODATA,
                "compress": "deflate",
                "predictor": 2,
                "tiled": True,
                "blockxsize": 512,
                "blockysize": 512,
                "BIGTIFF": "IF_SAFER",
            })
            with rasterio.open(tmp_path, "w", **meta) as dst:
                dst.write(out_arr.astype("uint8"))
                dst.write_colormap(1, {k: _hex_to_rgba(v["color"]) for k, v in CLASSES.items()})
                dst.update_tags(
                    dataset="ESA WorldCover 10 m 2021 v200",
                    layer="Map",
                    clipped_by="clip_esa_worldcover.py",
                    nodata=str(NODATA),
                )
        clipped_paths.append(tmp_path)

    if len(clipped_paths) == 1:
        clipped_paths[0].replace(out_tif)
    else:
        datasets = [rasterio.open(p) for p in clipped_paths]
        try:
            mosaic, transform = merge(datasets, nodata=NODATA)
            meta = datasets[0].meta.copy()
            meta.update({
                "height": mosaic.shape[1],
                "width": mosaic.shape[2],
                "transform": transform,
                "compress": "deflate",
                "predictor": 2,
                "tiled": True,
                "blockxsize": 512,
                "blockysize": 512,
                "BIGTIFF": "IF_SAFER",
            })
            with rasterio.open(out_tif, "w", **meta) as dst:
                dst.write(mosaic.astype("uint8"))
                dst.write_colormap(1, {k: _hex_to_rgba(v["color"]) for k, v in CLASSES.items()})
                dst.update_tags(dataset="ESA WorldCover 10 m 2021 v200", layer="Map", nodata=str(NODATA))
        finally:
            for ds in datasets:
                ds.close()
            for p in clipped_paths:
                p.unlink(missing_ok=True)
    return out_tif


def reproject_to_utm(src_tif: Path, aoi: gpd.GeoDataFrame, out_tif: Path, resolution: float = 10.0) -> Tuple[Path, float]:
    utm_crs = aoi.estimate_utm_crs()
    if utm_crs is None:
        raise ValueError("No se pudo estimar un CRS UTM para el AOI.")
    with rasterio.open(src_tif) as src:
        transform, width, height = calculate_default_transform(
            src.crs, utm_crs, src.width, src.height, *src.bounds, resolution=resolution
        )
        meta = src.meta.copy()
        meta.update({
            "crs": utm_crs,
            "transform": transform,
            "width": width,
            "height": height,
            "nodata": NODATA,
            "compress": "deflate",
            "predictor": 2,
            "tiled": True,
            "blockxsize": 512,
            "blockysize": 512,
            "BIGTIFF": "IF_SAFER",
        })
        data = np.full((height, width), NODATA, dtype="uint8")
        reproject(
            source=rasterio.band(src, 1),
            destination=data,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=utm_crs,
            src_nodata=NODATA,
            dst_nodata=NODATA,
            resampling=Resampling.nearest,
        )
        with rasterio.open(out_tif, "w", **meta) as dst:
            dst.write(data, 1)
            dst.write_colormap(1, {k: _hex_to_rgba(v["color"]) for k, v in CLASSES.items()})
            dst.update_tags(
                dataset="ESA WorldCover 10 m 2021 v200",
                layer="Map",
                crs_note="Reproyectado a UTM a 10 m con remuestreo vecino más cercano",
                nodata=str(NODATA),
            )
    pixel_area_m2 = abs(transform.a * transform.e)
    return out_tif, float(pixel_area_m2)


def write_area_stats(projected_tif: Path, pixel_area_m2: float, out_csv: Path, out_json: Path) -> None:
    with rasterio.open(projected_tif) as src:
        arr = src.read(1)
    values, counts = np.unique(arr[arr != NODATA], return_counts=True)
    total_area_m2 = float(counts.sum() * pixel_area_m2)
    rows = []
    for value, count in zip(values.tolist(), counts.tolist()):
        info = CLASSES.get(int(value), {"class_en": "Unknown", "class_es": "Desconocida", "color": "#000000"})
        area_m2 = float(count * pixel_area_m2)
        rows.append({
            "value": int(value),
            "class_en": info["class_en"],
            "class_es": info["class_es"],
            "color": info["color"],
            "pixels": int(count),
            "area_m2": area_m2,
            "area_ha": area_m2 / 10000.0,
            "area_km2": area_m2 / 1_000_000.0,
            "percent_of_classified_area": (area_m2 / total_area_m2 * 100.0) if total_area_m2 else 0.0,
        })
    rows.sort(key=lambda r: r["value"])
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [
            "value", "class_en", "class_es", "color", "pixels", "area_m2", "area_ha", "area_km2", "percent_of_classified_area"
        ])
        writer.writeheader()
        writer.writerows(rows)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"pixel_area_m2": pixel_area_m2, "total_classified_area_m2": total_area_m2, "classes": rows}, f, indent=2, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Recorta ESA WorldCover 10 m 2021 v200 con un AOI vectorial.")
    parser.add_argument("--aoi", default="AOI_Naposta_Grande_shp.zip", help="AOI vectorial: zip de shapefile, .shp, GeoJSON, GPKG, etc.")
    parser.add_argument("--out", default="outputs", help="Carpeta de salida")
    parser.add_argument("--tile-dir", default="data", help="Carpeta local para guardar/buscar tiles WorldCover")
    parser.add_argument("--skip-download", action="store_true", help="No descarga; exige que los tiles existan en --tile-dir")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribe tiles descargados y salidas")
    parser.add_argument("--dry-run", action="store_true", help="Solo informa tiles/URLs; no descarga ni recorta")
    args = parser.parse_args(argv)

    aoi_path = Path(args.aoi)
    out_dir = Path(args.out)
    tile_dir = Path(args.tile_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tile_dir.mkdir(parents=True, exist_ok=True)

    aoi = read_aoi(aoi_path)
    bounds = tuple(float(v) for v in aoi.total_bounds)
    tiles_ll = tile_lower_lefts(bounds)
    tiles = [tile_name(lat, lon) for lat, lon in tiles_ll]

    print("AOI CRS: EPSG:4326")
    print(f"Bounds lon/lat: {bounds}")
    print(f"Tiles WorldCover necesarios: {', '.join(tiles)}")
    for tile in tiles:
        print(f"  {tile}: {worldcover_url(tile)}")
    if args.dry_run:
        return 0

    tile_paths = []
    for tile in tiles:
        fn = f"ESA_WorldCover_10m_{YEAR}_{VERSION}_{tile}_{LAYER}.tif"
        out_path = tile_dir / fn
        if args.skip_download:
            if not out_path.exists():
                raise FileNotFoundError(f"No encontré {out_path}. Quite --skip-download o copie el tile allí.")
        else:
            download_file(worldcover_url(tile), out_path, overwrite=args.overwrite)
        tile_paths.append(out_path)

    clip4326 = out_dir / "ESA_WorldCover_2021_v200_AOI_Naposta_Grande_clip_EPSG4326.tif"
    cliputm = out_dir / "ESA_WorldCover_2021_v200_AOI_Naposta_Grande_clip_EPSG32720_10m.tif"
    stats_csv = out_dir / "ESA_WorldCover_2021_v200_AOI_Naposta_Grande_area_stats.csv"
    stats_json = out_dir / "ESA_WorldCover_2021_v200_AOI_Naposta_Grande_area_stats.json"

    if clip4326.exists() and not args.overwrite:
        print(f"Salida existente: {clip4326}")
    else:
        write_clip_epsg4326(tile_paths, aoi, clip4326)
        print(f"Recorte EPSG:4326: {clip4326}")

    if cliputm.exists() and not args.overwrite:
        print(f"Salida existente: {cliputm}")
        with rasterio.open(cliputm) as src:
            pixel_area_m2 = abs(src.transform.a * src.transform.e)
    else:
        _, pixel_area_m2 = reproject_to_utm(clip4326, aoi, cliputm, resolution=10.0)
        print(f"Recorte UTM 10 m: {cliputm}")

    write_area_stats(cliputm, pixel_area_m2, stats_csv, stats_json)
    print(f"Estadísticas: {stats_csv}")
    print(f"Estadísticas JSON: {stats_json}")
    print("Listo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
