# Comparación en GEE: entrenamiento con Fotointerpretación vs ESA WorldCover
### TP2 · Cuenca del Arroyo Napostá Grande · Clasificación LULC con Random Forest sobre Sentinel-2

## Diseño del experimento

Se entrenó el **mismo** clasificador (Random Forest, 200 árboles), sobre el **mismo** compuesto **Sentinel-2 SR 2025** (mediana anual sin nubes, 10 bandas), con la **misma** partición 70/30 y semilla 42. Lo único que cambia es el **conjunto de puntos de entrenamiento**:

- **Modelo A — Fotointerpretación:** 301 puntos clasificados visualmente en CEO (referencia de campo). Distribución real: Matorral 63, Pastizal 60, Construido 48, Suelo 44, Arbórea 32, Agua 26, Cultivos 23, **Humedal 5**.
- **Modelo B — ESA WorldCover:** 400 puntos con la etiqueta del producto ESA WorldCover 10 m (50 por clase, balanceado).

## Resultados

| Modelo entrenado con | n puntos | Overall Accuracy | Kappa |
|---|---|---|---|
| Fotointerpretación | 301 | **43,0 %** | **0,322** |
| ESA WorldCover | 400 | **56,2 %** | **0,499** |

El modelo entrenado con etiquetas ESA obtiene mejor precisión global y Kappa.

## Interpretación (importante)

Una **mayor OA en el modelo ESA no significa un mejor mapa**. Hay tres motivos que lo explican:

1. **Validación parcialmente circular.** Las etiquetas ESA provienen de un producto que ya deriva de imágenes satelitales coherentes con Sentinel-2. Entrenar RF con S2 para predecir ESA y validar contra un *split* de las **mismas** etiquetas ESA mide, en gran parte, la capacidad de **reproducir ESA**, no la exactitud frente al terreno.
2. **Tamaño y balance.** 400 puntos balanceados (50/clase) vs 301 desbalanceados. Clases con pocos ejemplos en la fotointerpretación (Humedal = 5, Cultivos = 23) debilitan el modelo A.
3. **La fotointerpretación es referencia independiente y más exigente.** El 43 % mide qué tan bien Sentinel-2 reproduce el **criterio humano**; es un número más honesto y, por eso, más bajo.

**Conclusión metodológica:** para un producto LULC **validado a campo**, el modelo entrenado con **fotointerpretación (Modelo A)** es el correcto, aunque su métrica luzca más baja. El modelo ESA luce mejor por construcción.

## Limitaciones y mejoras sugeridas

- Ambos OA son moderados: **8 clases finas a partir de un solo compuesto S2** es difícil. Mejoras posibles:
  - **Agregar variables temporales/índices** (NDVI, NDWI, percentiles estacionales) además de la mediana anual.
  - **Reagrupar o quitar clases problemáticas** (p. ej. fusionar o descartar *Humedal herbáceo*, que tuvo solo 5 puntos y baja separabilidad).
  - **Equilibrar y ampliar** los puntos de fotointerpretación (completar los ~100 restantes y reforzar las clases raras).
- Reportar siempre **OA + Kappa + matriz de confusión + precisión por clase**, no solo la OA global.

## Relación con la validación ESA vs fotointerpretación

Este experimento es coherente con la **matriz de acuerdo** (ver `Informe_acuerdo_ESA_vs_fotointerpretacion.md`): ESA y la fotointerpretación coinciden solo parcialmente (47 % de acuerdo, Kappa 0,39), sobre todo en el continuo herbáceo-arbustivo y en el humedal. Esa divergencia es la misma que explica por qué entrenar con uno u otro conjunto produce mapas distintos.

## Archivos
- `03_Scripts_GEE/00_comparacion_FOTO_vs_ESA.js` — script autocontenido que corre ambos modelos y reporta las métricas.
- `04_Datos_referencia/puntos_GEE_fotointerp_ESA8.csv` — 301 puntos de fotointerpretación (entrenamiento Modelo A).
- `04_Datos_referencia/puntos_naposta_ESA8_GEE.csv` — 400 puntos ESA (entrenamiento Modelo B).
