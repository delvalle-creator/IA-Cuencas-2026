/******************************************************************************
 * TP2 — PASO 2 (GEE): Generar 400 puntos de muestreo aleatorio ESTRATIFICADO
 *                     (50 puntos por cada una de las 8 clases ESA) sobre la cuenca.
 * Área de estudio: cuenca del Arroyo Napostá Grande (Bahía Blanca, Argentina).
 *
 * Qué hace este script:
 *   1. Recorta ESA WorldCover 2021 al AOI y la traduce a 8 clases (igual que el
 *      Paso 1).
 *   2. Toma una muestra ALEATORIA ESTRATIFICADA: 50 puntos por clase = 400 puntos
 *      (semilla fija 42, así es reproducible).
 *   3. Agrega a cada punto su longitud, latitud y un identificador PLOTID.
 *   4. Exporta DOS archivos:
 *        - el CSV para subir a Collect Earth Online (columnas LON, LAT, PLOTID);
 *        - un CSV con la clase ESA de cada punto, para la validación en GEE.
 *
 * Pensado para alumnos que NO programan: reemplace SU_USUARIO y presione Run.
 * Pegar en https://code.earthengine.google.com
 ******************************************************************************/

/* ============================ 1) CONFIGURACIÓN ============================ */

var aoi = ee.FeatureCollection('projects/SU_USUARIO/assets/AOI_Naposta_Grande');

var PUNTOS_POR_CLASE = 50;   // 50 x 8 clases = 400 puntos
var SEMILLA = 42;            // fija -> resultado reproducible

var ESA_VAL  = [10, 20, 30, 40, 50, 60, 80, 90];
var CLASE_ID = [ 1,  2,  3,  4,  5,  6,  7,  8];
var PALETA = ['006400','ffbb22','ffff4c','f096ff','fa0000','b4b4b4','0064c8','0096a0'];

/* ===================== 2) ESA WORLDCOVER -> 8 CLASES ===================== */

var esa8 = ee.ImageCollection('ESA/WorldCover/v200').first()
  .select('Map')
  .remap(ESA_VAL, CLASE_ID)
  .rename('clase_id')
  .clip(aoi);

/* ===================== 3) MUESTREO ESTRATIFICADO ========================= */

// 50 puntos por clase, en posiciones aleatorias dentro de la cuenca.
var muestra = esa8.stratifiedSample({
  numPoints: PUNTOS_POR_CLASE,
  classBand: 'clase_id',
  region: aoi.geometry(),
  scale: 10,
  seed: SEMILLA,
  geometries: true
});

// Agregar columnas LON / LAT a partir de la geometría del punto.
muestra = muestra.map(function(f){
  var c = ee.List(f.geometry().coordinates());
  return f.set({LON: c.get(0), LAT: c.get(1)});
});

// Numerar los puntos con un PLOTID correlativo (1, 2, 3, ...).
var listaPts = muestra.toList(muestra.size());
var indices  = ee.List.sequence(1, muestra.size());
var conPlotId = ee.FeatureCollection(indices.map(function(i){
  i = ee.Number(i);
  var f = ee.Feature(listaPts.get(i.subtract(1)));
  return f.set('PLOTID', i);
}));

print('Total de puntos generados (debe ser 400):', conPlotId.size());

Map.centerObject(aoi, 11);
Map.addLayer(esa8, {min: 1, max: 8, palette: PALETA}, 'ESA WorldCover - 8 clases', false);
Map.addLayer(conPlotId, {color: 'red'}, 'Puntos estratificados (400)');
Map.addLayer(aoi.style({color: 'black', fillColor: '00000000', width: 2}), {}, 'Cuenca Napostá');

/* ===================== 4) EXPORTAR (Tasks -> Run) ======================== */

// (a) CSV para CARGAR en Collect Earth Online: columnas LON, LAT, PLOTID.
Export.table.toDrive({
  collection: conPlotId,
  description: 'plots_naposta_ESA8_400_CEO',
  folder: 'TP2_LULC',
  fileFormat: 'CSV',
  selectors: ['LON', 'LAT', 'PLOTID']
});

// (b) CSV con la clase ESA de cada punto (para la validación posterior en GEE).
Export.table.toDrive({
  collection: conPlotId,
  description: 'puntos_naposta_ESA8_GEE',
  folder: 'TP2_LULC',
  fileFormat: 'CSV',
  selectors: ['PLOTID', 'LON', 'LAT', 'clase_id']
});
