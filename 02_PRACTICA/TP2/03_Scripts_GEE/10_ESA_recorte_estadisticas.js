/******************************************************************************
 * TP2 — PASO 1 (GEE): Recortar ESA WorldCover 10 m (2021) con la cuenca,
 *                     traducir a 8 clases en español y calcular estadísticas.
 * Área de estudio: cuenca del Arroyo Napostá Grande (Bahía Blanca, Argentina).
 *
 * Qué hace este script:
 *   1. Carga ESA WorldCover 2021 (v200, 10 m) y la recorta al AOI de la cuenca.
 *   2. Reasigna (remap) los códigos ESA (10,20,...,90) a las 8 clases del TP2
 *      en español (clase_id 1..8).
 *   3. Muestra el mapa con la paleta de las 8 clases.
 *   4. Calcula el ÁREA (km² y %) por clase dentro de la cuenca.
 *   5. Exporta el recorte como GeoTIFF y la tabla de estadísticas como CSV.
 *
 * Pensado para alumnos que NO programan: solo reemplace SU_USUARIO y presione Run.
 * Pegar en https://code.earthengine.google.com
 ******************************************************************************/

/* ============================ 1) CONFIGURACIÓN ============================ */

// AOI: cuenca del Napostá Grande (asset que usted subió desde 00_Area_estudio).
var aoi = ee.FeatureCollection('projects/SU_USUARIO/assets/AOI_Naposta_Grande');

// Las 8 clases ESA presentes en la cuenca: código ESA -> clase_id (1..8).
var ESA_VAL  = [10, 20, 30, 40, 50, 60, 80, 90];
var CLASE_ID = [ 1,  2,  3,  4,  5,  6,  7,  8];
var NOMBRES  = [
  'Cobertura arbórea',           // 1  (ESA 10)
  'Matorral/arbustal',           // 2  (ESA 20)
  'Pastizal/herbáceas',          // 3  (ESA 30)
  'Cultivos',                    // 4  (ESA 40)
  'Construido/urbano',           // 5  (ESA 50)
  'Suelo desnudo/veg. escasa',   // 6  (ESA 60)
  'Cuerpos de agua permanentes', // 7  (ESA 80)
  'Humedal herbáceo'             // 8  (ESA 90)
];
var PALETA = ['006400','ffbb22','ffff4c','f096ff','fa0000','b4b4b4','0064c8','0096a0'];

/* ===================== 2) RECORTAR ESA WORLDCOVER ======================== */

// Producto global ESA WorldCover 2021 (10 m). La banda se llama 'Map'.
var esaGlobal = ee.ImageCollection('ESA/WorldCover/v200').first();

// Recorte al AOI y traducción a las 8 clases del TP2 (1..8).
var esa8 = esaGlobal.select('Map')
  .remap(ESA_VAL, CLASE_ID)
  .rename('clase_id')
  .clip(aoi);

Map.centerObject(aoi, 11);
Map.addLayer(esa8, {min: 1, max: 8, palette: PALETA}, 'ESA WorldCover - 8 clases');
Map.addLayer(aoi.style({color: 'black', fillColor: '00000000', width: 2}), {}, 'Cuenca Napostá');

/* ===================== 3) ESTADÍSTICAS DE ÁREA POR CLASE ================= */

// Área de cada píxel (km²) agrupada por clase_id.
var areaPorClase = ee.Image.pixelArea().divide(1e6).addBands(esa8)
  .reduceRegion({
    reducer: ee.Reducer.sum().group(1, 'clase_id'),
    geometry: aoi.geometry(),
    scale: 10,
    maxPixels: 1e13
  });

// Armar una tabla legible (clase_id, nombre, área km², % del total).
var grupos = ee.List(areaPorClase.get('groups'));
var areaTotal = ee.Number(grupos.iterate(function(g, acc){
  return ee.Number(acc).add(ee.Dictionary(g).getNumber('sum'));
}, 0));

var tabla = ee.FeatureCollection(grupos.map(function(g){
  g = ee.Dictionary(g);
  var id = g.getNumber('clase_id');
  var km2 = g.getNumber('sum');
  var nombre = ee.List(NOMBRES).get(id.subtract(1));
  return ee.Feature(null, {
    clase_id: id,
    clase: nombre,
    area_km2: km2,
    porcentaje: km2.divide(areaTotal).multiply(100)
  });
}));

print('Área total de la cuenca (km²):', areaTotal);
print('Estadísticas ESA WorldCover por clase (km² y %):', tabla);

// Gráfico de barras del área por clase.
print(ui.Chart.feature.byFeature(tabla, 'clase', ['area_km2'])
  .setChartType('ColumnChart')
  .setOptions({title: 'Área por clase ESA WorldCover - Cuenca Napostá', legend: {position: 'none'},
               hAxis: {title: 'Clase'}, vAxis: {title: 'km²'}}));

/* ===================== 4) EXPORTAR (Tasks -> Run) ======================== */

// Recorte de 8 clases como GeoTIFF (UTM 20S, 10 m), para 05_Resultados_LULC.
Export.image.toDrive({
  image: esa8.toInt8(),
  description: 'ESA8_Naposta_2021',
  folder: 'TP2_LULC',
  fileNamePrefix: 'ESA8_Naposta_2021',
  region: aoi.geometry(),
  scale: 10,
  crs: 'EPSG:32720',
  maxPixels: 1e13
});

// Tabla de estadísticas como CSV.
Export.table.toDrive({
  collection: tabla,
  description: 'ESA8_Naposta_estadisticas',
  folder: 'TP2_LULC',
  fileFormat: 'CSV',
  selectors: ['clase_id', 'clase', 'area_km2', 'porcentaje']
});
