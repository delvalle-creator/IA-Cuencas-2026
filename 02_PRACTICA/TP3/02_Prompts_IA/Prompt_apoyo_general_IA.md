# Prompts de apoyo general con IA (depurar, interpretar, adaptar)

Estos prompts son de uso general para el TP3. Sirven para que el alumno
resuelva dudas con un asistente de IA sin escribir código desde cero. Pegue siempre el
mensaje de error completo y el fragmento de código correspondiente.

---

## A. Depurar un error

Tengo este error al ejecutar mi script de Earth Engine (o mi notebook de Colab):

```
<pegue aquí el mensaje de error completo>
```

Este es el código:

```
<pegue aquí la celda o el bloque>
```

Explique en español por qué ocurre y entregue el bloque corregido.

---

## B. Interpretar resultados y redactar el informe

Comparé una imagen Sentinel-2 de 10 m con su versión superresuelta a 1 m (S2DR4) sobre
el sector de Bahía Blanca. Redacte, en tono académico y en español, un párrafo que analice las
ventajas y limitaciones de la superresolución para delinear canales finos, mencionando la
naturaleza sintética del detalle generado y la necesidad de validación con ortofotos.

---

## C. Adaptar el flujo a otra área de estudio

Quiero reutilizar este flujo para otra área. Mi *bounding box* es
`<min_lon, min_lat, max_lon, max_lat>` y la zona UTM es `<EPSG>`. Indique exactamente qué
líneas de este código se deben cambiar y por qué:

```
<pegue aquí el código>
```

---

## Buenas prácticas con IA

- Verifique siempre el código generado ejecutándolo en una celda o en el Editor de GEE.
- Pida que las explicaciones sean en español.
- Confirme los nombres de paquetes y funciones. El paquete real de superresolución es
  `s2dr4` (no `s2dr4-processor`, que era un nombre inventado del enunciado original).
- Valide los resultados visualmente en el mapa antes de exportar.
