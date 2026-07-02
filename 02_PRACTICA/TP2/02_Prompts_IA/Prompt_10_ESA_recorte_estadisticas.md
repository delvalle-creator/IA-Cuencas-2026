# Prompt para generar el script de recorte de ESA WorldCover + estadísticas (Paso 1)

> **Cómo usar este documento:** copie el texto del bloque "PROMPT" y péguelo en su
> asistente de IA. El script resultante ya se entrega en
> `03_Scripts_GEE/10_ESA_recorte_estadisticas.js`.

---

## PROMPT (copiar desde aquí)

Actúe como experto en teledetección y Google Earth Engine (GEE). Necesito un
**script en JavaScript para el Editor de Código de GEE**, pensado para alumnos de
posgrado que **no programan** (claro, comentado en español, que corra con solo
presionar "Run"). El objetivo es preparar la capa de referencia del trabajo.

### Tarea
1. Cargar **ESA WorldCover 2021** (colección `ESA/WorldCover/v200`, banda `Map`,
   10 m) y **recortarla** al área de estudio: la cuenca del Arroyo Napostá Grande,
   provista como *asset* `FeatureCollection` (AOI).
2. **Reasignar (remap)** los códigos de ESA a 8 clases en español con identificador
   entero `clase_id` 1..8, en este orden:
   - 10 → 1 Cobertura arbórea
   - 20 → 2 Matorral/arbustal
   - 30 → 3 Pastizal/herbáceas
   - 40 → 4 Cultivos
   - 50 → 5 Construido/urbano
   - 60 → 6 Suelo desnudo/veg. escasa
   - 80 → 7 Cuerpos de agua permanentes
   - 90 → 8 Humedal herbáceo
3. Mostrar el mapa de las 8 clases con una paleta de colores (una por clase).
4. Calcular las **estadísticas de área por clase** dentro de la cuenca: superficie
   en km² y porcentaje del total (use `ee.Image.pixelArea` agrupada por `clase_id`).
   Mostrar también un gráfico de barras del área por clase.
5. **Exportar** a Google Drive: (a) el recorte de 8 clases como GeoTIFF en UTM 20S
   (EPSG:32720), 10 m; y (b) la tabla de estadísticas como CSV.

### Configuración
Agrupe al inicio, fácil de editar: el *Asset ID* del AOI (con un `SU_USUARIO`
reemplazable), las listas de códigos ESA y nombres de clase, y la paleta.

### Estilo
Todo comentado en español, variables de configuración al inicio, listo para "Run".
Entregue un único archivo `.js`.

## (fin del PROMPT)

---
