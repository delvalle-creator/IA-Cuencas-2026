# Prompt para generar el script de los 400 puntos estratificados (Paso 2)

> **Cómo usar este documento:** copie el texto del bloque "PROMPT" y péguelo en su
> asistente de IA. El script resultante ya se entrega en
> `03_Scripts_GEE/20_generar_400_puntos.js`.

---

## PROMPT (copiar desde aquí)

Actúe como experto en teledetección y Google Earth Engine (GEE). Necesito un
**script en JavaScript para el Editor de Código de GEE**, para alumnos que **no
programan** (claro, comentado en español, que corra con solo presionar "Run").

### Tarea
1. Recortar **ESA WorldCover 2021** (`ESA/WorldCover/v200`, banda `Map`, 10 m) al
   AOI de la cuenca del Napostá Grande (asset `FeatureCollection`) y reasignarla a
   8 clases con `clase_id` 1..8 (igual mapeo que el script del Paso 1: 10→1, 20→2,
   30→3, 40→4, 50→5, 60→6, 80→7, 90→8).
2. Tomar una **muestra aleatoria estratificada**: **50 puntos por cada una de las 8
   clases = 400 puntos**, con **semilla fija (42)** para que sea reproducible. Use
   `stratifiedSample` con `classBand: 'clase_id'`, `scale: 10`, `geometries: true`.
3. Agregar a cada punto las columnas **LON** y **LAT** (de su geometría) y un
   identificador correlativo **PLOTID** (1, 2, 3, …).
4. Mostrar los puntos sobre el mapa.
5. **Exportar** a Drive **dos CSV**:
   - uno para **subir a Collect Earth Online**, con columnas `LON, LAT, PLOTID`;
   - otro con la **clase ESA** de cada punto (`PLOTID, LON, LAT, clase_id`), para la
     validación posterior en GEE.

### Configuración
Al inicio, editable: *Asset ID* del AOI (con `SU_USUARIO`), puntos por clase (50),
semilla (42), mapeo de códigos ESA→clase_id y paleta.

### Estilo
Comentado en español, configuración al inicio, listo para "Run". Un único `.js`.

## (fin del PROMPT)

---
