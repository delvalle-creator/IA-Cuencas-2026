# Guía completa — Validación de ESA WorldCover 10 m por fotointerpretación
### TP2 · Cuenca del Arroyo Napostá Grande (Bahía Blanca) · Proyecto CEO "LULC Naposta ESA8 2021 - 400 ptos"

Esta guía cubre **todo el proceso, paso a paso**, desde el recorte de la cobertura ESA WorldCover hasta la matriz de acuerdo contra la fotointerpretación, e incluye las **pistas visuales por clase** y **todas las confusiones de clases** detectadas, con reglas para decidir en cada caso.

---

## 1. Objetivo

Evaluar qué tan bien coincide el producto global **ESA WorldCover 10 m 2021 v200** con la **fotointerpretación** sobre imagen de alta resolución en la cuenca del Napostá Grande, usando una muestra densa y balanceada de puntos. Reemplaza los ~60 puntos del TP2 original por **400 puntos (50 por clase)** para obtener una estimación más robusta y desagregada por clase.

---

## 2. Flujo de trabajo (paso a paso)

### Paso A — Recorte de ESA WorldCover 10 m con la cuenca
1. AOI: vector de la cuenca Napostá Grande (`AOI_Naposta_Grande_shp.zip`, EPSG:4326, ≈ 1404 km²).
2. Tile ESA necesario: **S39W063** (el AOI cae entero en ese tile de 3°×3°).
3. Recorte con GDAL (gdalwarp) leyendo el tile por rango desde el bucket oficial de AWS:
   - Salida 1: recorte EPSG:4326 (CRS original).
   - Salida 2: recorte UTM 20S (EPSG:32720), píxel 10 m, con la paleta de colores.
4. Estadísticas de área por clase sobre el raster UTM (NoData = 0).

### Paso B — Muestreo aleatorio estratificado (400 puntos)
1. Sobre el raster UTM 10 m (píxeles equiárea, sin sesgo espacial).
2. **50 puntos por cada una de las 8 clases presentes** = 400 puntos (semilla fija 42, reproducible).
3. Centros de píxel convertidos a lon/lat (EPSG:4326).
4. Salidas: `puntos_naposta_CEO.csv` (PLOTID, LON, LAT), `puntos_naposta_ESA8_GEE.csv` (con clase ESA), shapefile y GeoJSON, y un mapa de verificación.

### Paso C — Proyecto en Collect Earth Online (CEO)
1. Institución CEREGEO → **Create New Project** (se usó el TP2 como plantilla para heredar AOI e imágenes).
2. Plot Design: distribución **CSV**, se sube `plots_naposta_ESA8_400.csv` (LON, LAT, PLOTID). Muestra = **Center**.
3. Encuesta: 1 pregunta "¿Cuál es la cobertura del suelo en este punto?" con las **8 clases ESA en español** (ver §3).
4. **Create Project** → **Publish Project** (queda abierto para recolectar).

### Paso D — Fotointerpretación en CEO (operativa)
1. En la pantalla del proyecto, **Collect**.
2. Cada punto aparece **sin clasificar** (CEO no muestra la clase de ESA: vos decidís).
3. **Asignar:** clic en el botón de la clase que ves → el punto toma ese color.
4. **Cambiar:** si te equivocaste, clic en **otro botón** y reemplaza la selección.
5. **Guardar:** botón **Save** (guarda y salta al siguiente punto, que aparece sin color = es uno nuevo, no perdiste nada).
6. **Navegar:** flechas ← → o casilla **"Go to plot"**. Para seguir solo con los pendientes, poné **Navigate → "Unanalyzed"**.
7. **Re-Zoom:** si girás la rueda y el mapa se aleja, el botón **Re-Zoom** vuelve a centrar la parcela. Para zoom usá los botones **+ / –** del mapa.
8. **Avance:** se ve en **Project Dashboard** (`Analyzed / Unanalyzed` sobre 400). CEO guarda automáticamente: podés cortar y retomar cuando quieras.

> Recomendación: hacerlo en tandas de 40–50 puntos y descansar la vista. No hace falta ver la clase de ESA para interpretar; lo ideal es hacerlo "a ciegas" para no sesgar.

### Paso E — Exportar y armar la matriz de acuerdo
1. En **review-project → Export Data → Download Sample Data** se baja el CSV con la columna de la clase fotointerpretada.
2. Se cruza por **`PLOTID`** la clase ESA de cada punto contra la clase fotointerpretada.
3. Se calcula la **matriz de confusión**, el **acuerdo global**, el **Kappa** y la precisión por clase.
4. **Solo se usan los puntos efectivamente fotointerpretados** (no se rellenan los faltantes con ESA, para no inflar el acuerdo).

---

## 3. Las 8 clases ESA (leyenda) y pistas visuales

| clase_id | Clase ESA (ES) | Cód. | Pistas visuales (contexto Napostá / Bahía Blanca) |
|---|---|---|---|
| 1 | Cobertura arbórea | 10 | Verde oscuro, textura rugosa, sombras de copas. Cortinas forestales, montes, arbolado urbano denso. |
| 2 | Matorral/arbustal | 20 | Vegetación baja verde-grisácea, moteada, sin hileras ni geometría. Bordes de campo, médanos. |
| 3 | Pastizal/herbáceas | 30 | Superficie homogénea, verde claro a ocre, sin parcelado geométrico. Campos naturales, pasturas. |
| 4 | Cultivos | 40 | Parcelas geométricas, bordes rectos; color según estado (verde, marrón, suelo arado); hileras o círculos de riego. |
| 5 | Construido/urbano | 50 | Techos, calles en grilla, gris/rojizo, geometría regular. Ciudad, periurbano, puerto, petroquímica, caminos, silos. |
| 6 | Suelo desnudo/veg. escasa | 60 | Tonos claros (beige, gris, blanco), sin vegetación. Suelos erosionados, salitrales/salinas, playas, peladares. |
| 7 | Cuerpos de agua permanentes | 80 | Superficies oscuras o azuladas, homogéneas. Arroyo, lagunas, embalses, canales del estuario. |
| 8 | Humedal herbáceo | 90 | Vegetación herbácea sobre suelo saturado, cerca del estuario/cauces; verdes a pardos mezclados con láminas de agua. Marismas. |

---

## 4. Confusiones de clases (detectadas en la matriz) y cómo decidir

Estas son las confusiones reales que aparecieron al contrastar ESA vs fotointerpretación en esta cuenca. Tenelas presentes al interpretar y al leer los resultados.

**4.1. Pastizal ↔ Matorral ↔ Suelo desnudo (el continuo herbáceo–arbustivo–suelo).**
Es la zona más confusa. ESA marcó como *Pastizal* muchos puntos que en imagen se ven como *Matorral* (19 casos) o *Suelo desnudo* (8 casos), y al revés *Matorral* → *Pastizal* (8 casos).
- *Regla:* si hay **porte arbustivo** (textura moteada, manchones, sombras bajas) → **Matorral**. Si es **manto herbáceo continuo y bajo** → **Pastizal**. Si predomina **suelo expuesto** con vegetación rala → **Suelo desnudo**. Ante la duda, mirá la **textura** (rugosa = arbustos; lisa = pasto) y la **proporción de suelo visible**.

**4.2. Humedal herbáceo → Matorral / Pastizal (la peor coincidencia: solo 5 % de acuerdo).**
ESA mapea como *Humedal herbáceo* amplias zonas que el intérprete vio como *Matorral* (14 casos) o *Pastizal* (13 casos). Es una **sobre-estimación típica del humedal** en ambientes de transición del estuario de Bahía Blanca.
- *Regla:* clasificá **Humedal** solo si hay evidencia de **suelo saturado / láminas de agua entremezcladas / patrón de marisma**, generalmente **pegado al estuario o a cauces**. Si es vegetación seca tierra adentro, casi seguro es **Pastizal** o **Matorral**, no humedal.

**4.3. Cobertura arbórea → Construido/urbano (9 casos).**
ESA marcó árboles donde el intérprete vio zona construida; suele ser **arbolado urbano** mezclado con techos y calles.
- *Regla:* si dominan **estructuras** (manzanas, techos, calles) → **Construido**, aunque haya árboles. Reservá **Arbórea** para masas de copas sin edificación.

**4.4. Otras a vigilar.**
- **Cultivo vs Pastizal:** geometría. Bordes rectos / hileras / color uniforme de lote → **Cultivo**; superficie irregular sin parcelado → **Pastizal**.
- **Suelo desnudo vs Construido:** ambos son claros. Con **estructura regular** (techos/calles) → **Construido**; superficie clara **sin estructura** → **Suelo desnudo**.
- **Agua vs Humedal:** lámina de agua continua → **Agua**; vegetación herbácea con agua entremezclada y suelo saturado → **Humedal**.

---

## 5. Resultados obtenidos (301 puntos fotointerpretados)

| Métrica | Valor |
|---|---|
| Puntos contrastados | 301 |
| Acuerdo global (Overall Accuracy) | **46,8 %** |
| Kappa de Cohen | **0,392** (moderado-bajo) |

**Acuerdo por clase (precisión del productor):**

| Clase ESA | Acuerdo |
|---|---|
| Cuerpos de agua permanentes | 68 % |
| Construido/urbano | 68 % |
| Cultivos | 57 % |
| Suelo desnudo/veg. escasa | 51 % |
| Cobertura arbórea | 51 % |
| Matorral/arbustal | 44 % |
| Pastizal/herbáceas | 32 % |
| Humedal herbáceo | **5 %** |

**Lectura:** ESA WorldCover coincide bien en clases espectralmente distintas (agua, urbano, cultivos) y mal en el continuo herbáceo-arbustivo y, sobre todo, en humedal. Para vegetación natural y humedal **no conviene usar ESA como verdad de campo sin verificación**.

---

## 6. Recomendaciones metodológicas

- Interpretar **a ciegas** (sin mirar la clase ESA) da una validación más estricta; ver la clase ESA antes inclina a coincidir.
- Usar **solo los puntos interpretados** para la matriz (no rellenar con ESA).
- Una muestra **densa y balanceada** (50/clase) da mejor representación de clases raras (agua, humedal) que el muestreo proporcional.
- Reportar siempre **acuerdo global + Kappa + acuerdo por clase + confusiones**, no solo el porcentaje global.

---

## 7. Archivos del proyecto

- `00_Area_estudio/` — AOI de la cuenca.
- `04_Datos_referencia/puntos_naposta_ESA8_GEE.csv` — 400 puntos con clase ESA (`PLOTID`, `clase`, `clase_id`, `esa_val`).
- `04_Datos_referencia/referencia_PLOTID_claseESA.xlsx` — planilla ordenada por PLOTID con la clase ESA (consulta rápida).
- `04_Datos_referencia/ceo_export_ESA8_300.csv` — exportación cruda de CEO (fotointerpretación).
- `04_Datos_referencia/matriz_acuerdo_ESA_vs_foto.xlsx` / `.csv` — matriz de confusión + métricas.
- `06_Informe/Informe_acuerdo_ESA_vs_fotointerpretacion.md` — informe de resultados.
- `03_Scripts_GEE/01_clasificacion_S2_RF_ESA8.js` y `02_clasificacion_Embeddings_RF_ESA8.js` — scripts GEE adaptados a las 8 clases ESA.
