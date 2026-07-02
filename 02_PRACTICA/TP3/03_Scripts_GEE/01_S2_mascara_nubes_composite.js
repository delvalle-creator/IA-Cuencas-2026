/******************************************************************************
 * TP3 - Insumo Sentinel-2 y manejo de nubes con Google Earth Engine
 * Objetivo: a partir de la escena Sentinel-2 del area de estudio, enmascarar
 *           nubes y sombras (s2cloudless + SCL) y generar un COMPUESTO LIBRE
 *           DE NUBES, que luego sirve como insumo para la superresolucion
 *           (S2DR4) en Google Colab.
 * Area de estudio: sector de Bahia Blanca (Argentina), tile MGRS T20HNC.
 *
 * Este script esta pensado para alumnos que NO programan: solo debe ajustar las
 * variables de la seccion CONFIGURACION y presionar "Run". Todo lo demas ya esta
 * resuelto y comentado en espanol.
 *
 * Pegue este codigo en el Editor de Codigo de GEE: https://code.earthengine.google.com
 *
 * NOTA: este paso (limpieza de nubes en GEE) es COMPLEMENTARIO. El insumo del TP es
 * la escena Sentinel-2 (carpeta 01_Insumo_Sentinel2) y la superresolucion se hace
 * con S2DR4 en Colab. Use este script si necesita ademas un producto cuantitativo
 * libre de nubes a 10 m.
 ******************************************************************************/

/* ============================ 1) CONFIGURACION ============================ *
 * Cambie unicamente lo que esta dentro de este bloque.                       */

// Area de interes: recorte rectangular [min_lon, min_lat, max_lon, max_lat].
// Por defecto cubre el sector de Bahia Blanca donde se eligieron los puntos del TP.
var BBOX = [-62.50, -38.85, -62.00, -38.30];   // sector de Bahia Blanca (escena T20HNC)
var area = ee.Geometry.Rectangle(BBOX);

// Ventana temporal de busqueda (la escena del TP es de 2026-04-30).
var FECHA_INI = '2026-03-15';
var FECHA_FIN = '2026-05-15';

// Umbral de probabilidad de nube de s2cloudless (0 a 100). Tipico: 40 a 60.
var UMBRAL_NUBE = 50;

// Distancia maxima de proyeccion de la sombra de nube, en km.
var DIST_SOMBRA_KM = 1.5;

// Sistema de coordenadas de salida (Bahia Blanca = UTM 20S).
var EPSG_SALIDA = 'EPSG:32720';

// Carpeta de Google Drive donde quedara el GeoTIFF exportado.
var CARPETA_DRIVE = 'TP3_Insumo_S2';

Map.centerObject(area, 11);

/* ============== 2) UNION Sentinel-2 SR + probabilidad de nube ============= */

var s2sr = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(area).filterDate(FECHA_INI, FECHA_FIN);

var s2cp = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY')
  .filterBounds(area).filterDate(FECHA_INI, FECHA_FIN);

var coleccion = ee.ImageCollection(
  ee.Join.saveFirst('s2cloudless').apply({
    primary: s2sr,
    secondary: s2cp,
    condition: ee.Filter.equals({leftField: 'system:index', rightField: 'system:index'})
  })
);

// Inventario de escenas con su porcentaje de nubes (mire la Consola, a la derecha).
print('Escenas Sentinel-2 encontradas:', s2sr.size());
print('Inventario (fecha y % de nubes):',
  s2sr.map(function(img){
    return ee.Feature(null, {
      fecha: img.date().format('YYYY-MM-dd'),
      nubes_pct: img.get('CLOUDY_PIXEL_PERCENTAGE')
    });
  }));

/* ===================== 3) MASCARA DE NUBES Y SOMBRAS ===================== */

function agregarNubes(img){
  var prob = ee.Image(img.get('s2cloudless')).select('probability');
  var esNube = prob.gt(UMBRAL_NUBE).rename('nubes');
  return img.addBands([prob.rename('prob_nube'), esNube]);
}

function agregarSombras(img){
  var noAgua = img.select('SCL').neq(6);
  var oscuros = img.select('B8').lt(0.15 * 1e4).multiply(noAgua).rename('oscuros');
  var azimut = ee.Number(90).subtract(ee.Number(img.get('MEAN_SOLAR_AZIMUTH_ANGLE')));
  var proy = img.select('nubes')
    .directionalDistanceTransform(azimut, DIST_SOMBRA_KM * 10)
    .reproject({crs: img.select(0).projection(), scale: 100})
    .select('distance').mask().rename('proy_nube');
  var sombras = proy.multiply(oscuros).rename('sombras');
  return img.addBands([oscuros, proy, sombras]);
}

function agregarMascara(img){
  img = agregarNubes(img);
  img = agregarSombras(img);
  var mascara = img.select('nubes').add(img.select('sombras')).gt(0);
  mascara = mascara.focalMin(2).focalMax(10)
    .reproject({crs: img.select(0).projection(), scale: 20})
    .rename('mascara_nube');
  return img.addBands(mascara);
}

var conMascara = coleccion.map(agregarMascara);

/* ================== 4) VISUALIZAR UNA ESCENA CON NUBES ================== */

var visRGB = {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000};
var escena = ee.Image(conMascara.first());

Map.addLayer(escena.clip(area), visRGB, '1) S2 original (con nubes)');
Map.addLayer(escena.select('prob_nube').clip(area),
  {min: 0, max: 100, palette: ['blue', 'white', 'red']}, '2) Probabilidad de nube', false);
Map.addLayer(escena.select('mascara_nube').selfMask().clip(area),
  {palette: 'orange'}, '3) Mascara nube + sombra', false);

/* ============ 5) COMPUESTO LIBRE DE NUBES (composicion temporal) ========= */

function aplicarMascara(img){
  return img.select('B.*').updateMask(img.select('mascara_nube').not());
}

var compuesto = conMascara.map(aplicarMascara).median().clip(area);
Map.addLayer(compuesto, visRGB, '4) Compuesto LIBRE DE NUBES (mediana)');

/* ====================== 6) EXPORTAR EL INSUMO LIMPIO ===================== */

Export.image.toDrive({
  image: compuesto.select(['B2', 'B3', 'B4', 'B8']).toFloat(),
  description: 'S2_BahiaBlanca_libre_nubes_10m',
  folder: CARPETA_DRIVE,
  fileNamePrefix: 's2_bahiablanca_libre_nubes_10m',
  region: area,
  scale: 10,
  crs: EPSG_SALIDA,
  maxPixels: 1e13
});

print('Listo. Revise el mapa (capas 1 a 4) y ejecute la tarea de exportacion en "Tasks".');
