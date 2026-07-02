# Prompt para preparar el notebook de superresolución (S2DR3 / S2DR4)

> **Cómo usar este documento:** copie el texto del bloque "PROMPT" y péguelo en su
> asistente de IA. Sirve para generar el cuaderno de Colab de apoyo que está en
> `04_Scripts_Colab/02_superresolucion_S2DR.ipynb`. Tenga presente que el modelo
> S2DR3/S2DR4 es propietario de gamma.earth y se ejecuta en su notebook oficial; el
> cuaderno de apoyo organiza el flujo y la comparación, no contiene los pesos del modelo.

---

## PROMPT (copiar desde aquí)

Actúe como un experto en teledetección y Python para Google Colab. Necesito un
**cuaderno de Colab** de apoyo, muy comentado en español y pensado para alumnos que
**no programan**, para el paso de **superresolución** de una escena Sentinel-2 ya
libre de nubes. El cuaderno debe dejar claro que la superresolución (S2DR3/S2DR4) NO
elimina nubes y que la limpieza se hizo antes en Google Earth Engine.

El cuaderno debe incluir, en celdas separadas y explicadas:
1. Configuración del entorno e indicación de activar la GPU (T4).
2. Instalación de librerías de apoyo (`rasterio`, `matplotlib`).
3. Montaje de Google Drive y lectura del insumo limpio exportado desde GEE
   (`s2_libre_nubes_10m.tif`).
4. Instrucciones claras para ejecutar el **notebook oficial de gamma.earth**
   (parametrizado por punto central y fecha de baja nubosidad), aclarando que el paquete real se llama `s2dr4` (no `s2dr4-processor`).
5. Una celda de **comparación visual** que muestre, lado a lado, la escena de 10 m y
   la salida superresuelta de 1 m con `rasterio` y `matplotlib`.
6. Indicaciones para la comparación en QGIS (complemento de cortina) y para el informe.

Entregue el cuaderno como un archivo `.ipynb` válido, con texto en español formal.

## (fin del PROMPT)

---

## Método real de S2DR4 (lo que muestra el video de Alfonso Arteaga)

S2DR4 SÍ tiene un paquete instalable. El cuaderno entregado lo usa así, en Google Colab
con GPU T4 y Python 3.12:

```python
# 1) Instalar el paquete oficial s2dr4 (wheel de gamma.earth)
!pip -q install https://storage.googleapis.com/0x7ff601307fa5/s2dr4-20260126.1-cp312-cp312-linux_x86_64.whl

# 2) Importar y procesar por coordenadas + fecha
import s2dr4.inferutils
s2dr4.inferutils.test(lonlat, date)
# Salidas a 1 m en /content/output/  (RGB, falso color, NDVI, 12 bandas)
```

El modelo descarga la escena Sentinel-2 y el modelo (~841 MB) automáticamente. Para áreas
grandes se repite con varios centros y se arma un mosaico.

---

## Enlaces útiles
- Notebook oficial S2DR3 (gamma.earth):
  https://colab.research.google.com/drive/18phbwA1iYG5VDGN2WjK7WrWYi-FdCHJ5
- Demostración de S2DR4: https://storage.googleapis.com/sentinel-s2dr3/s2dr4menu1.html
- Acceso / consultas: info@gamma.earth
