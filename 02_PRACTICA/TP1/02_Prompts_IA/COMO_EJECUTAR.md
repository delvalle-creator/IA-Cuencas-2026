# Cómo ejecutar el script de metadatos de DTM

Hay **dos versiones** del script (hacen lo mismo):

| Archivo | Dónde se usa | Requiere instalar |
|---|---|---|
| `leer_metadatos_dtm.py` | Python normal (Anaconda, IDLE, VS Code, terminal) | `rasterio numpy pandas openpyxl` |
| `leer_metadatos_dtm_QGIS.py` | **Consola de Python de QGIS** | Nada (usa el GDAL que trae QGIS) |

## Estructura de carpetas
```
TP1\
 ├─ 03_Scripts_QGIS\     <- los .py van aquí
 ├─ 01_Materiales\       <- ENTRADA de demostración: recortes originales (con el error)
 ├─ 05_DTMs_corregidos\  <- ENTRADA: recortes corregidos (homogéneos)
 └─ 04_Metadatos\        <- SALIDA: aquí se guardan los CSV/Excel
```

## Opción A — Python normal
1. Instalar una sola vez (en la consola/Anaconda Prompt):
   `pip install rasterio numpy pandas openpyxl`
2. Ejecutar:
   `python leer_metadatos_dtm.py`

## Opción B — Consola de Python de QGIS (sin instalar nada)
1. Abrir QGIS.
2. Menú **Complementos → Consola de Python** (o `Ctrl+Alt+P`).
3. Clic en **"Mostrar editor"** (icono de hoja).
4. Abrir `leer_metadatos_dtm_QGIS.py` y apretar el botón verde **"Ejecutar script"**.
   (Usar el editor es importante: así QGIS sabe dónde está el archivo y arma solo las rutas.)
5. El resultado aparece en la consola; los CSV quedan en `04_Metadatos`.

> Si en vez del editor pega el código directo en la consola, complete a mano
> la variable `RUTA_TP1` al inicio del script.

## Actividad sugerida (ver el error primero)
1. Abra el script y, en la sección CONFIGURACIÓN, **descomente** la línea:
   `# CARPETA = ... "01_Materiales"`  (quítele el `#`).
2. Ejecute: va a ver el bloque **"ADVERTENCIAS DE HOMOGENEIDAD"**
   (resoluciones y tamaños distintos → los DTM NO son comparables).
3. Vuelva a **comentar** esa línea y ejecute de nuevo: ahora usa la carpeta
   corregida (`05_DTMs_corregidos`) y debe decir **"Todos los DTM son homogéneos"**.

## Alternativa sin programar (para validar)
- En QGIS: clic derecho en la capa → **Propiedades → Información**.
- O en consola: `gdalinfo archivo.tif`.
