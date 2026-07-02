# Prompt para el script de validación en GEE — Sentinel-2: Fotointerpretación vs ESA (Paso 4a)

> **Cómo usar este documento:** copie el bloque "PROMPT" y péguelo en su asistente de
> IA. El script resultante ya se entrega en
> `03_Scripts_GEE/30_comparacion_S2_FOTO_vs_ESA.js` (autocontenido: trae los puntos
> embebidos, no hace falta subir ningún *asset*).

---

## PROMPT (copiar desde aquí)

Actúe como experto en teledetección y Google Earth Engine. Necesito un **script en
JavaScript para el Editor de Código de GEE**, para alumnos que **no programan**
(comentado en español, que corra con solo presionar "Run", **sin subir assets**:
incluya el AOI y los puntos embebidos en el propio código).

### Contexto
Cuenca del Arroyo Napostá Grande. Hay dos conjuntos de puntos de referencia con la
misma leyenda de 8 clases (`clase_id` 1..8):
- **Fotointerpretación:** ~301 puntos clasificados visualmente en Collect Earth Online.
- **ESA WorldCover:** 400 puntos (50 por clase) etiquetados con el producto ESA.

### Tarea
1. Armar un **compuesto Sentinel-2 SR 2025** (`COPERNICUS/S2_SR_HARMONIZED`, mediana
   anual sin nubes con máscara QA60, 10 bandas) recortado al AOI.
2. Entrenar **dos** clasificadores **Random Forest** idénticos (200 árboles, misma
   partición 70/30 y semilla 42), cambiando solo el set de entrenamiento: (A)
   fotointerpretación; (B) ESA. Muestrear el compuesto en los puntos con
   `sampleRegions` (`scale: 10`).
3. Para cada modelo, reportar **matriz de confusión, precisión general (OA), Kappa,
   precisión del productor y del usuario**.
4. Mostrar en el mapa los dos mapas LULC resultantes (paleta de 8 clases) y exportar
   los GeoTIFF.
5. Dejar un comentario aclarando que entrenar/validar contra **ESA** mide el
   **acuerdo con ESA** (es parcialmente circular), mientras que la
   **fotointerpretación** es la referencia independiente y más exigente.

### Estilo
Comentado en español, configuración al inicio, autocontenido (datos embebidos),
listo para "Run". Un único `.js`.

## (fin del PROMPT)

---
