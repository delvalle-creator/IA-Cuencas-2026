# Cómo ejecutar los scripts del TP2 en Google Earth Engine (GEE)

Los scripts están en **JavaScript** y se ejecutan en el **Editor de Código de GEE**
(en el navegador: `code.earthengine.google.com`). No hace falta saber programar:
se pegan, se ajusta `SU_USUARIO` (cuando corresponde) y se presiona **Run**.

## Requisito previo
Una cuenta de Google Earth Engine aprobada, con un proyecto de la nube asociado
(GEE lo solicita la primera vez). Para los pasos 1 y 2 hay que tener subido el AOI
de la cuenca como *asset* (ver más abajo).

## Orden de ejecución (4 scripts)

| Orden | Script (`03_Scripts_GEE/`) | Qué hace | ¿Sube assets? |
|---|---|---|---|
| **1** | `10_ESA_recorte_estadisticas.js` | Recorta ESA WorldCover 2021 a la cuenca, la pasa a 8 clases (ES) y calcula áreas. | AOI |
| **2** | `20_generar_400_puntos.js` | Genera 400 puntos estratificados (50×8) y los exporta a CSV para CEO. | AOI |
| — | *(se va a Collect Earth Online a fotointerpretar)* | | |
| **3** | `30_comparacion_S2_FOTO_vs_ESA.js` | Random Forest sobre **Sentinel-2**: foto vs ESA → matrices de confusión. | No (autocontenido) |
| **4** | `40_comparacion_EMB_FOTO_vs_ESA.js` | Random Forest sobre **Embeddings 2024/2025**: foto vs ESA + mapas y cambios. | No (autocontenido) |

## Subir el AOI como asset (para los pasos 1 y 2)
1. En el Editor de Código, pestaña **Assets** → **NEW** → **Shape files**.
2. Suba `00_Area_estudio/AOI_Naposta_Grande_shp.zip`. Asset Name: `AOI_Naposta_Grande`.
3. Espere a que la tarea termine (pestaña **Tasks**) y **refresque** el panel Assets.

## Pasos para cada script
1. Abra el `.js` con el **Bloc de notas** (clic derecho → Abrir con; **no** doble
   clic, que en Windows intenta ejecutarlo y da error). Copie todo (Ctrl+A, Ctrl+C).
2. En GEE, clic en el editor central → **Ctrl+A** → **Ctrl+V** (reemplaza lo que haya).
3. En los scripts 1 y 2: reemplace `SU_USUARIO` por su usuario de Earth Engine.
   (Los scripts 3 y 4 son autocontenidos: no hay que tocar nada.)
4. Presione **Run**. Vea los resultados en el mapa y, en la **Console** (derecha),
   las estadísticas y matrices de confusión.

## Descargar resultados (GeoTIFF / CSV)
Cada `Export...` crea una tarea en la pestaña **Tasks**. Presione **Run** en la tarea;
el archivo queda en su **Google Drive**, carpeta `TP2_LULC`. Descárguelo a
`05_Resultados_LULC` (mapas) o `04_Datos_referencia` (CSV de puntos), según el caso.

## Nota sobre la geometría de los puntos (importante)
Si en algún momento sube un CSV de puntos como *asset* y al subirlo **no** asigna las
columnas de coordenadas (X = `lon`, Y = `lat`), los puntos quedan **sin ubicación** y
el clasificador da el error «No valid training data were found». Los scripts
autocontenidos (3 y 4) evitan esto porque traen los puntos embebidos.
