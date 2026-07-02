# Contraste ESA WorldCover 10 m (2021) vs Fotointerpretación — Cuenca Napostá Grande

**Proyecto CEO:** LULC Naposta ESA8 2021 - 400 ptos (institución CEREGEO).
**Referencia:** muestreo aleatorio estratificado, 400 puntos (50 por clase, 8 clases ESA).
**Fotointerpretados:** 301 puntos (75% de la muestra) en Collect Earth Online, sobre imagen de alta resolución.
**Método:** se cruzó por `PLOTID` la clase de ESA WorldCover de cada punto contra la clase asignada por fotointerpretación, y se construyó la matriz de acuerdo.

## Resultados globales

| Métrica | Valor |
|---|---|
| Puntos contrastados | 301 |
| Acuerdo global (Overall Accuracy) | **46,8 %** |
| Kappa de Cohen | **0,392** (acuerdo moderado-bajo) |

Un acuerdo del 47 % y un Kappa de 0,39 indican que, a nivel de las 8 clases finas, **ESA WorldCover coincide solo parcialmente** con la fotointerpretación local en esta cuenca. No es un mal producto: la divergencia se concentra en clases visual y espectralmente similares.

## Acuerdo por clase (precisión del productor = sobre los puntos que ESA etiquetó así)

| Clase ESA | Acuerdo |
|---|---|
| Cuerpos de agua permanentes | 68 % |
| Construido/urbano | 68 % |
| Cultivos | 57 % |
| Suelo desnudo/veg. escasa | 51 % |
| Cobertura arbórea | 51 % |
| Matorral/arbustal | 44 % |
| Pastizal/herbáceas | 32 % |
| **Humedal herbáceo** | **5 %** |

Las clases **espectralmente distintas** (agua, construido, cultivos) son las que mejor coinciden. El continuo **herbáceo–arbustivo–suelo** (pastizal, matorral, suelo desnudo) es donde ESA y el intérprete más difieren, por la similitud visual entre esas coberturas.

## Principales confusiones (ESA → Fotointerpretación)

| n | ESA dijo | El intérprete vio |
|---|---|---|
| 19 | Pastizal/herbáceas | Matorral/arbustal |
| 14 | Humedal herbáceo | Matorral/arbustal |
| 13 | Humedal herbáceo | Pastizal/herbáceas |
| 9 | Cobertura arbórea | Construido/urbano |
| 8 | Pastizal/herbáceas | Suelo desnudo/veg. escasa |
| 8 | Matorral/arbustal | Pastizal/herbáceas |

El caso más notable es el **Humedal herbáceo**: ESA mapea como humedal amplias zonas que en la imagen se interpretan como matorral o pastizal (típica sobre-estimación del humedal herbáceo en ambientes de transición del estuario de Bahía Blanca). También aparece confusión arbórea↔construido (arbolado urbano) y el clásico solapamiento pastizal↔matorral↔suelo.

## Conclusión

- Para clases bien definidas (agua, urbano, cultivos), ESA WorldCover es un insumo confiable en la cuenca.
- Para vegetación herbácea/arbustiva y, sobre todo, humedal, **conviene no usar ESA como verdad de campo sin verificación**.
- La muestra densa y balanceada (301 puntos vs ~60 del TP2 original) permite una estimación de acuerdo mucho más robusta y desagregada por clase.

> Nota metodológica: el acuerdo se calculó solo sobre los 301 puntos efectivamente fotointerpretados. No se rellenaron los puntos faltantes con la etiqueta de ESA, para no inflar artificialmente el acuerdo.

## Archivos
- `matriz_acuerdo_ESA_vs_foto.xlsx` — matriz de confusión coloreada + métricas.
- `matriz_acuerdo_ESA_vs_foto.csv` — la misma matriz en texto.
- `ceo_export_ESA8_300.csv` — exportación cruda de CEO (fotointerpretación).
- `puntos_naposta_ESA8_GEE.csv` — etiquetas ESA por punto.
