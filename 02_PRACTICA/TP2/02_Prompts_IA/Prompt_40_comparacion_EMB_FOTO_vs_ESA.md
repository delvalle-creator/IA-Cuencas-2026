# Prompt para el script de validación en GEE — Embeddings 2024/2025: Fotointerpretación vs ESA (Paso 4b)

> **Cómo usar este documento:** copie el bloque "PROMPT" y péguelo en su asistente de
> IA. El script resultante ya se entrega en
> `03_Scripts_GEE/40_comparacion_EMB_FOTO_vs_ESA.js` (autocontenido: trae los puntos
> embebidos, no hace falta subir ningún *asset*).

---

## PROMPT (copiar desde aquí)

Actúe como experto en teledetección y Google Earth Engine. Necesito un **script en
JavaScript para el Editor de Código de GEE**, para alumnos que **no programan**
(comentado en español, que corra con solo presionar "Run", **sin subir assets**:
AOI y puntos embebidos).

### Contexto
Cuenca del Arroyo Napostá Grande. Mismos dos sets de puntos de 8 clases que el script
de Sentinel-2: fotointerpretación (~301) y ESA WorldCover (400, 50/clase).

### Tarea
1. Cargar los **Embeddings satelitales anuales** de Google
   (`GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`, 64 bandas, 10 m) para **2024** y **2025**,
   recortados al AOI (usar `mosaic()` por las zonas UTM).
2. Entrenar **Random Forest** (200 árboles, partición 70/30, semilla 42) sobre los
   embeddings, con cada set de entrenamiento (fotointerpretación y ESA) y reportar
   **matriz de confusión, OA, Kappa, precisión por clase**.
3. Aplicar el modelo a **2024 y 2025**, mostrar ambos mapas LULC (paleta de 8 clases)
   y un **mapa de cambios** (píxeles cuya clase cambió de un año al otro).
4. Calcular el **área por clase** de cada año y exportar los GeoTIFF.
5. Comentar la lectura: los embeddings mejoran a Sentinel-2; el número más alto (ESA
   + embeddings) es **parcialmente circular**; el resultado **honesto** es
   **embeddings + fotointerpretación**.

### Estilo
Comentado en español, configuración al inicio, autocontenido, listo para "Run".
Un único `.js`.

## (fin del PROMPT)

---
