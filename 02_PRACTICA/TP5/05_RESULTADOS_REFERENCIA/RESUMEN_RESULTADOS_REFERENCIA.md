# Resultados de referencia

## HAND / grilla completa

- Shape de la grilla: `592 x 661`.
- CRS: `EPSG:32720`.
- Píxeles válidos: `286,897`.
- Píxeles inundados con profundidad > 0,05 m: `7,649`.
- Porcentaje inundado sobre la grilla válida: `2.67%`.
- Área válida aproximada: `201.94 km²`.
- Área inundada aproximada: `5.38 km²`.

## Dataset Orange

- Filas: `30,000`.
- Columnas: `8`.
- Píxeles inundados dentro del dataset Orange: `7,649` (`25.50%`).

El porcentaje en Orange no debe confundirse con el porcentaje de la grilla completa porque el CSV fue submuestreado para acelerar la práctica.

## Validación automática

Ejecutar:

```bat
python D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA\07_SCRIPTS_Y_PROMPTS\11_Python_validar_resultados_tp5.py
```
