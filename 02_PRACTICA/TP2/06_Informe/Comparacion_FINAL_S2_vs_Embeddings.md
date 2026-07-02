# Comparación final TP2 — Sentinel-2 vs Embeddings · Fotointerpretación vs ESA
### Clasificación LULC con Random Forest · Cuenca del Arroyo Napostá Grande (Bahía Blanca)

## Diseño

Mismo clasificador (Random Forest, 200 árboles), misma partición 70/30 y semilla 42, mismas 8 clases. Se cruzan **dos factores**:

- **Insumo:** Sentinel-2 SR 2025 (mediana anual, 10 bandas) **vs** Google Satellite Embedding V1 Annual 2024 (64 bandas).
- **Entrenamiento:** tu **fotointerpretación** (301 puntos) **vs** etiquetas **ESA WorldCover** (400 puntos, 50/clase).

## Resultados

| Insumo | Entrenamiento | Overall Accuracy | Kappa |
|---|---|---|---|
| Sentinel-2 | Fotointerpretación (301) | 43,0 % | 0,322 |
| Sentinel-2 | ESA WorldCover (400) | 56,2 % | 0,499 |
| **Embeddings** | **Fotointerpretación (301)** | **49,4 %** | **0,411** |
| **Embeddings** | **ESA WorldCover (400)** | **77,2 %** | **0,740** |

## Lectura de los resultados

**1. Los Embeddings mejoran a Sentinel-2 en todos los casos.** Las 64 bandas del embedding (rasgos aprendidos que resumen un año completo) separan mejor las clases que la mediana espectral cruda. La fotointerpretación sube de 43,0 % a 49,4 % y ESA de 56,2 % a 77,2 %.

**2. El modelo ESA es el que más gana con embeddings (salto enorme: +21 puntos de OA).** Es esperable y refuerza lo visto: las etiquetas ESA derivan de productos satelitales, y los embeddings están especialmente alineados con ese tipo de información. Reproducir ESA desde embeddings es muy fácil para el RF → la métrica es **parcialmente circular** (entrena y valida sobre el mismo producto).

**3. El modelo de fotointerpretación mejora menos (de 43 % a 49 %)** porque su límite no es el insumo sino la **muestra**: 301 puntos, desbalanceados, con clases críticas muy escasas (**Humedal = 5**, Cultivos = 23). El criterio humano es referencia independiente y más exigente.

## Conclusión del TP2

- **El mejor insumo es claramente el de Embeddings** (mayor OA y Kappa con cualquier set de entrenamiento). Para un mapa LULC de la cuenca, conviene usar Embeddings antes que Sentinel-2 crudo.
- **El número más alto (ESA + Embeddings, 77 %) no es el más representativo de la realidad de campo**, porque la validación contra ESA es autorreferencial. El resultado **honesto, validado por fotointerpretación, es Embeddings + Fotointerpretación: OA 49,4 % / Kappa 0,41.**
- La **mayor densidad de puntos sí ayuda** (se ve en ESA 400 vs los ~60 del TP2 original), pero **la calidad y el balance de la referencia importan tanto como la cantidad**: completar los ~100 puntos faltantes y reforzar las clases raras (sobre todo Humedal) subiría el modelo de fotointerpretación.
- **Mejoras futuras:** reagrupar o quitar *Humedal herbáceo* (5 puntos, baja separabilidad), sumar índices/estacionalidad si se usa Sentinel-2, y equilibrar la muestra de campo.

## Relación con la validación ESA vs fotointerpretación
Coherente con la matriz de acuerdo (47 % de coincidencia, Kappa 0,39): ESA y la fotointerpretación divergen sobre todo en el continuo herbáceo-arbustivo y en el humedal, y esa divergencia es la que explica por qué entrenar con uno u otro produce mapas y precisiones distintas.

## Archivos
- `03_Scripts_GEE/00_comparacion_FOTO_vs_ESA.js` — comparación con Sentinel-2.
- `03_Scripts_GEE/00_comparacion_EMBEDDINGS_FOTO_vs_ESA.js` — comparación con Embeddings (2024) + mapas 2024/2025 y cambios.
- `06_Informe/Comparacion_GEE_FOTO_vs_ESA.md` — detalle Sentinel-2.
- `06_Informe/Informe_acuerdo_ESA_vs_fotointerpretacion.md` — validación ESA vs campo.
- `06_Informe/Guia_fotointerpretacion_8clases_ESA.md` — guía completa del proceso.
- Mapas LULC (GeoTIFF): exportables desde la pestaña **Tasks** de GEE (carpeta `TP2_LULC` en Drive).
