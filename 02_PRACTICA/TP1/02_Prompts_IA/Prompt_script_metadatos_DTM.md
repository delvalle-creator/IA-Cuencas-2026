# Prompt para generar un script que lea los metadatos de varios DTM

> **Cómo usar este documento:** copie todo el texto que está dentro del bloque
> "PROMPT" y péguelo en su asistente de IA (o entréguelo como consigna). Está
> redactado para que el asistente genere un script de Python funcional, comentado
> y pensado para principiantes. 

---

## PROMPT (copiar desde aquí)

Actúe como un programador experto en SIG y teledetección. Necesito un **script en
Python** que lea y compare los **metadatos de todos los modelos digitales de
elevación / terreno (DTM)** que se encuentren en una carpeta de práctica (la
carpeta donde están mis recortes). El script es para alumnos de posgrado que **no
programan**, así que debe ser claro, estar muy comentado en español y ser fácil de
ejecutar.

### Objetivo
Recorrer una carpeta, detectar todos los archivos ráster (DTM) y mostrar sus
metadatos en una tabla ordenada, además de **avisar automáticamente si los
archivos NO son homogéneos** entre sí (distinta resolución, CRS, extensión,
NoData, etc.), que es justamente el problema que queremos que los alumnos
detecten.

### Entrada
- Una ruta de carpeta indicada por el usuario (con un valor por defecto editable
  al inicio del script, en una variable bien visible llamada `CARPETA`).
- Debe procesar estos formatos ráster como mínimo: `.tif`, `.tiff`, `.img`,
  `.vrt`, `.asc`, `.dem`. Que sea fácil agregar más extensiones.
- Opción para buscar también en subcarpetas (búsqueda recursiva activable con una
  variable booleana `RECURSIVO`).

### Librerías
- Usar **rasterio** como librería principal (y, si hace falta, `numpy` y `pandas`).
- Al inicio, incluir un comentario con el comando de instalación:
  `pip install rasterio numpy pandas openpyxl`.
- Manejar errores: si un archivo no se puede abrir, que el script lo informe y
  continúe con los demás (no que se caiga).

### Metadatos que debe extraer de cada archivo
Para cada ráster, obtener y mostrar:
1. Nombre del archivo y ruta relativa.
2. Formato / driver (GTiff, HFA, etc.).
3. Sistema de coordenadas (CRS): nombre y código EPSG.
4. Tamaño en píxeles: ancho × alto y total de píxeles.
5. Resolución / tamaño de celda: en grados, en **arcosegundos** y en **metros
   aproximados** (calcular los metros usando la latitud media del ráster; aclarar
   en un comentario que es una aproximación).
6. Extensión (bounding box): Oeste, Sur, Este, Norte.
7. Número de bandas y tipo de dato (float32, int16, etc.).
8. Valor de NoData.
9. Registro de píxel (`AREA_OR_POINT`: Area o Point).
10. Compresión y si está en mosaico interno (tiled).
11. Tamaño del archivo en disco (MB).
12. Estadísticas básicas de la banda 1 ignorando NoData: mínimo, máximo, media,
    desviación estándar y cantidad de píxeles válidos.

### Control de calidad (la parte importante)
Después de leer todos los archivos, el script debe **comparar entre sí** y emitir
advertencias claras (con un encabezado tipo "⚠ ADVERTENCIAS DE HOMOGENEIDAD") si
detecta que entre los DTM hay:
- más de un **CRS** distinto;
- más de una **resolución** distinta (comparar con una tolerancia pequeña, p. ej.
  1e-9 grados, para no marcar diferencias por redondeo);
- **extensiones** que no coinciden;
- más de un valor de **NoData**;
- más de un tipo de **registro de píxel** (Area vs Point);
- más de un **tipo de dato**.
Si todos coinciden, que muestre un mensaje de "✔ Todos los DTM son homogéneos
(misma grilla)".

### Salidas
1. Una **tabla legible en la consola** con una fila por archivo y las columnas más
   importantes (nombre, EPSG, tamaño px, resolución en m, NoData, registro,
   estadísticas).
2. Un archivo **`metadatos_DTM.csv`** y, si es posible, también
   **`metadatos_DTM.xlsx`**, guardados en la misma carpeta de práctica, con todos
   los campos.
3. Al final, el bloque de advertencias de homogeneidad descrito arriba.

### Estilo del código
- Todo comentado en español, explicando qué hace cada bloque, pensado para que un
  alumno que no programa pueda leerlo y entenderlo.
- Variables de configuración (`CARPETA`, `RECURSIVO`, extensiones, nombres de
  salida) agrupadas y bien señalizadas al principio.
- Que se ejecute simplemente con `python leer_metadatos_dtm.py`, sin argumentos
  obligatorios.
- Incluir al final un breve instructivo en comentarios: cómo instalar las
  librerías y cómo cambiar la carpeta.

Entregue el script completo en un solo archivo llamado `leer_metadatos_dtm.py`,
listo para ejecutar.

## (fin del PROMPT)

---


