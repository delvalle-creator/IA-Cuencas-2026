# Prompt para generar el script de GEE (máscara de nubes y compuesto libre de nubes)

> **Cómo usar este documento:** copie todo el texto que está dentro del bloque
> "PROMPT" y péguelo en su asistente de IA. Está redactado para que el asistente
> genere un script de Google Earth Engine (JavaScript) funcional, comentado y
> pensado para alumnos que **no programan**. El script ya entregado en
> `03_Scripts_GEE/01_S2_mascara_nubes_composite.js` fue generado con este prompt;
> aquí lo conserva para entender cómo se pide y para poder adaptarlo.

---

## PROMPT (copiar desde aquí)

Actúe como un experto en teledetección y Google Earth Engine (GEE). Necesito un
**script en JavaScript para el Editor de Código de GEE** que prepare el insumo
Sentinel-2 para un trabajo de superresolución, separando correctamente dos
problemas: la **limpieza de nubes** (que resuelve este script) y la
**superresolución** (que se hace después, fuera de GEE). El script es para alumnos
de posgrado que **no programan**, así que debe ser claro, estar muy comentado en
español y ejecutarse presionando "Run", configurando solo unas variables al inicio.

### Área de estudio y datos de entrada
- Área de estudio: sector de Bahía Blanca (Argentina), escena Sentinel-2 tile T20HNC,
  delimitada por un *bounding box* (sin shapefile).
- Use `COPERNICUS/S2_SR_HARMONIZED` (reflectancia de superficie) y
  `COPERNICUS/S2_CLOUD_PROBABILITY` (s2cloudless) unidas por su índice común.

### Sección de configuración (al inicio, bien visible)
Agrupe en un solo bloque, fácil de editar: el *bounding box* del área, ventana temporal (fecha inicial y final), umbral de probabilidad de
nube de s2cloudless, distancia de proyección de la sombra, sistema de coordenadas de
salida y carpeta de Drive para la exportación.

### Procesamiento que debe realizar
1. Inventariar las escenas Sentinel-2 del período con su porcentaje de nubes.
2. Derivar la máscara de **nubes** (probabilidad mayor al umbral) y de **sombras**
   (píxeles oscuros en el NIR proyectados desde la nube según el azimut solar,
   excluyendo el agua con la banda SCL); combinarlas con un pequeño buffer.
3. Visualizar en el mapa: la escena con nubes, la probabilidad de nube, la máscara y
   el compuesto limpio.
4. Generar un **compuesto libre de nubes** tomando la **mediana** de los píxeles
   limpios de toda la serie temporal (eliminación de nubes con observaciones reales).
5. Exportar el compuesto limpio (10 m) a Google Drive como GeoTIFF, como insumo para
   la superresolución.

### Estilo del código
- Todo comentado en español, explicando cada bloque para alguien que no programa.
- Variables de configuración agrupadas y señalizadas al principio.
- Que se ejecute con solo presionar "Run" tras configurar el *asset* del AOI.

Entregue el script completo en un solo archivo `.js`, listo para pegar en el Editor
de Código de GEE.

## (fin del PROMPT)

---

> **Recordatorio:** este script **no** aumenta la resolución; solo prepara una escena
> limpia. La superresolución a ~1 m se hace después con S2DR3/S2DR4 (vea el prompt
> `Prompt_notebook_superresolucion_S2DR.md`).
