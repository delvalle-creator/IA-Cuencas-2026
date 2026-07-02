# Orange Data Mining

Esta carpeta contiene el proyecto Orange, los datos tabulares, las figuras y el informe complementario.

Proyecto principal:

```text
06_ORANGE_DATA_MINING\Proyecto_Orange\Analisis_Inundacion_BB.ows
```

Datos principales:

```text
06_ORANGE_DATA_MINING\Datos\dataset_inundacion_BB.csv
06_ORANGE_DATA_MINING\Datos\dataset_puntos_BB.csv
```

Variable objetivo sugerida en Orange:

```text
inundado_cat
```

Scripts numerados asociados:

```text
07_SCRIPTS_Y_PROMPTS\09_Orange_construir_dataset.py
07_SCRIPTS_Y_PROMPTS\10_Orange_estadisticas_y_graficos.py
```

Regeneración desde consola de Windows:

```bat
cd /d D:\Temp\TP5_SIMULACION_INUNDACION_BAHIA_BLANCA\07_SCRIPTS_Y_PROMPTS
python 09_Orange_construir_dataset.py
python 10_Orange_estadisticas_y_graficos.py
```

El dataset de Orange está submuestreado para que el flujo sea ágil. Conserva todos los píxeles inundados disponibles y muestrea parte de los secos; por eso el porcentaje de inundación del CSV no representa directamente el porcentaje sobre toda la grilla.
