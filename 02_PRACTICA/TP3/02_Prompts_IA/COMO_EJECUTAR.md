# Cómo ejecutar los scripts del TP3

El insumo es la **escena Sentinel-2** (carpeta `01_Insumo_Sentinel2`), del sector de Bahía
Blanca (tile T20HNC, 30-04-2026). Sobre esa imagen se eligen los puntos de interés. **S2DR4
no procesa toda la escena, sino cuadrantes acotados alrededor de cada coordenada.** Usted no
necesita programar: los archivos ya están escritos y comentados en español.

| Paso | Archivo | Entorno | Qué hace |
|---|---|---|---|
| Principal | `04_Scripts_Colab/02_superresolucion_S2DR4.ipynb` | Google Colab | Superresuelve un cuadrante (10 m → ~1 m) con el paquete S2DR4 |
| Complementario | `03_Scripts_GEE/01_S2_mascara_nubes_composite.js` | Editor de Código de GEE | Limpia nubes/sombras y genera un compuesto a 10 m del sector |

## Parte B (principal) — Superresolución en Colab

1. Abra `02_superresolucion_S2DR4.ipynb` en https://colab.research.google.com (Archivo → Subir cuaderno).
2. Active la **GPU (T4)**: `Entorno de ejecución → Cambiar tipo de entorno de ejecución`.
3. **Paso 1** del cuaderno: instale el paquete oficial **s2dr4** (una sola línea `pip install`).
4. **Paso 1b**: **reinicie la sesión** (evita el error de NumPy y mantiene Drive montado).
5. **Paso 2**: conecte Google Drive (opcional, para guardar en la nube).
6. **Paso 3**: indique el punto como **(longitud, latitud)** y la **fecha**.
7. **Paso 4**: ejecute `s2dr4.inferutils.test(lonlat, date)`. Genera 4 productos a 1 m en `/content/output/`.
8. **Paso 5**: guarde a Drive (copia recursiva) y/o descargue el ZIP al disco.

> Recuerde: S2DR4 procesa **un cuadrante alrededor del punto**, no la escena completa.

## Parte A (complementaria) — Limpieza de nubes en GEE

1. Abra `01_S2_mascara_nubes_composite.js` con el Bloc de notas, copie su contenido y péguelo
   en el Editor de Código de GEE (https://code.earthengine.google.com).
2. En la sección **CONFIGURACIÓN**, ajuste si lo desea el *bounding box* (por defecto cubre el
   sector de Bahía Blanca) y la ventana de fechas. **No requiere subir ningún shapefile.**
3. Presione **Run**. Revise en el mapa la escena con nubes, la probabilidad de nube, la máscara
   y el compuesto libre de nubes (capas 1 a 4).
4. Vaya a la pestaña **Tasks** y ejecute la exportación. El GeoTIFF limpio (10 m) quedará en su
   Google Drive, carpeta `TP3_Insumo_S2`.

> **Aclaración:** S2DR4 es un modelo de **superresolución de imagen única**: aumenta el detalle
> (10 m → ~1 m), pero **no elimina nubes**. La limpieza de nubes la resuelve este paso de GEE
> (compuesto temporal: mediana de píxeles limpios de varias fechas). El paquete real se llama
> **`s2dr4`** (no `s2dr4-processor`, que no existe).
