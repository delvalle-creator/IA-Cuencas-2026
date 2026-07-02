# Prompt: Teledetección de inundaciones con Sentinel‑1, Sentinel‑2, SNAP y QGIS

Actúa como experto en teledetección de inundaciones con Sentinel‑1, Sentinel‑2, SNAP y QGIS.

## Imágenes disponibles

### Sentinel‑1 (dual‑pol VV/VH)
- **03/03/2025** — pre‑evento, track 141  
- **10/03/2025** — post‑evento 1, track 68  
- **15/03/2025** — post‑evento 2, track 141  

### Sentinel‑2
- **01/03/2025** — pre‑evento  
- **11/03/2025** — post‑evento  

## Área de estudio
Bahía Blanca, Argentina.  
CRS objetivo: **EPSG:32720**  
Resolución: **10 m**

## Requerimientos

1. Verificar nombres reales de bandas, CRS, resolución, extent y nodata.  
2. No asumir nombres B2, B3, etc.; revisar nombres reales.  
3. Para Sentinel‑1 usar intensidad lineal, no dB.  
4. Ortorrectificar S1 con Copernicus GLO‑30.  
5. Colocar S1 y S2 en una grilla común.  
6. Calcular solapamiento común.  
7. Hacer subset al área común.  
8. Generar productos derivados:  
   - dVV y dVH (03/03 → 15/03, mismo track)  
   - ratios VV/VH  
   - MNDWI pre/post y dMNDWI  
   - NDVI pre/post y dNDVI  
   - scores de sinergia radar + óptico  
9. S1 10/03 solo como diagnóstico visual (track distinto).  
10. Generar RGB:  
    - S1 multitemporal VV  
    - S1 multitemporal VH  
    - S1 strict same‑track  
    - S1+S2 synergy RGB  
11. Generar shapefiles para SNAP:  
    - polígono de solapamiento  
    - polígonos de inundación/anegamiento  
12. Explicar interpretación, colores, limitaciones y producto final recomendado.

