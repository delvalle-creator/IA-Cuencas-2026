# Anexo — Google Drive en Windows (para el TP2)

Este anexo resuelve los problemas más habituales con **Google Drive para escritorio**
en Windows, que aparecen al trabajar este TP2. Importa porque los resultados que se
exportan desde **Google Earth Engine (GEE)** —por ejemplo el recorte raster
`ESA8_Naposta_2021.tif` y los mapas LULC— **no se descargan a su computadora
automáticamente: quedan primero en su Google Drive**, en la carpeta `TP2_LULC`. Para
usarlos en QGIS o copiarlos al TP2, necesita ver su Drive en el Explorador de Windows.

> Está pensado para alumnos que **no programan** y que quizás nunca configuraron Drive
> en el escritorio. Puede copiarse tal cual dentro de la guía única de prácticas.

---

## 1. Drive en el escritorio es una "unidad" más

Al instalar **Google Drive para escritorio** (distinto de la web `drive.google.com`) e
iniciar sesión, Drive aparece en el Explorador como **una unidad con su propia letra**,
por ejemplo `Google Drive (H:)`, dentro de "Este equipo". Adentro verá:

- **Mi unidad** — sus archivos personales de Drive. Aquí está la carpeta `TP2_LULC`
  donde GEE deja las exportaciones.
- **Otros ordenadores** / unidades compartidas, si las tiene.

**Atención a una confusión muy común:** la letra de Drive **no** es fija y **no** es lo
mismo que un disco local. En muchas PC el disco local de datos usa una letra (por
ejemplo `G:` llamado "Datos 3") y **Drive usa otra distinta** (por ejemplo `H:`). Mirar
solo la letra engaña: fíjese en el **nombre** y el **ícono** (Drive tiene el triángulo
de colores). Una carpeta local llamada algo como "Respaldo_GoogleDrive" **no** es su
Drive en vivo: es solo una copia vieja.

---

## 2. Si no ve la unidad de Drive en el Explorador

Casi siempre es porque **la aplicación de Drive no está abierta**. La unidad solo
aparece mientras Google Drive para escritorio está en ejecución.

1. Abra el menú **Inicio** y escriba **Google Drive**; ábralo.
2. Espere unos segundos: aparecerá `Google Drive (H:)` (u otra letra) en "Este equipo".
3. Si pide iniciar sesión, hágalo **usted mismo** con su cuenta de Google (la misma de
   Earth Engine). *(Por seguridad, nadie debe escribir su contraseña por usted.)*

> Recién iniciada, la app tarda unos segundos en "montar" los archivos. Si al abrir una
> carpeta de Drive aparece el error **"El parámetro no es correcto"**, espere de 15 a 30
> segundos y vuelva a intentar: es que Drive todavía estaba inicializándose.

---

## 3. Que Drive esté SIEMPRE disponible (iniciar con Windows)

La unidad de Drive solo aparece en el Explorador mientras la aplicación está en
ejecución. Si al **reiniciar la computadora el ícono de Drive desaparece** y la unidad
ya no figura, es porque Drive **no está arrancando solo** con Windows. Para resolverlo:

> ⚠️ **Cuidado con una confusión muy frecuente.** Hacer clic derecho sobre el ícono de
> Drive y elegir **"Anclar a Inicio"** **NO** sirve para esto: esa opción solo **fija el
> ícono en el menú Inicio**, pero **no** hace que Drive arranque al encender la PC. Son
> cosas distintas. Use cualquiera de los dos métodos de abajo.

### Método A — Configuración de Windows (el más simple y confiable)

1. Abra **Configuración** de Windows (menú Inicio → engranaje ⚙, o tecla `Windows + I`).
2. Vaya a **Aplicaciones** → **Inicio**.
3. Busque **Google Drive** en la lista y ponga su interruptor en **Activado**.

Listo: en el próximo reinicio, Drive arrancará solo y la unidad aparecerá en el
Explorador. *(Verificado: tras reiniciar, el ícono de Drive y la unidad vuelven solos.)*

### Método B — desde la propia aplicación de Drive

1. Clic en el **ícono de Google Drive** en la **bandeja del sistema** (abajo a la
   derecha, junto al reloj; puede estar dentro de la flechita "Mostrar íconos ocultos").
2. Clic en el **engranaje ⚙** → **Configuración** (o **Preferencias**).
3. Deje **tildado**: *"Iniciar Google Drive al iniciar sesión en el sistema"* (el texto
   puede variar según la versión).

> Si después de reiniciar el ícono de Drive **no aparece**, abra Drive a mano una vez
> (menú Inicio → escribir "Google Drive") y revise el Método A: casi siempre es que el
> inicio automático estaba desactivado.

---

## 4. El anclaje a "Acceso rápido" puede fallar (y no es su culpa)

Es tentador hacer clic derecho sobre la carpeta de Drive → **"Anclar a Acceso rápido"**
para tenerla siempre a mano en el panel izquierdo. En muchas PC, Windows responde con
el error **"El parámetro no es correcto"**. Es una **limitación conocida** entre la
unidad virtual de Google Drive y el Acceso rápido de Windows 11 — no se puede forzar y
no indica ningún problema en sus archivos.

Alternativas que sí funcionan:

- **No haga falta anclar:** la unidad `Google Drive (H:)` ya aparece sola en "Este
  equipo" siempre que Drive esté abierto (ver punto 3).
- **Anclar una subcarpeta real:** en algunas versiones, anclar una carpeta *interna* de
  Mi unidad funciona aunque la raíz falle. Pruebe con la subcarpeta concreta que use.
- **Acceso directo en el Escritorio:** clic derecho sobre la carpeta → **Mostrar más
  opciones** → **Enviar a** → **Escritorio (crear acceso directo)**. Queda un ícono que
  abre Drive directamente.

---

## 5. Archivos "en la nube" vs. "en este dispositivo" (ícono de nubecita)

En la unidad de Drive, muchos archivos muestran un **ícono de nube**: están en Google
Drive pero **todavía no descargados** a su disco. Eso es normal (ahorra espacio).

- **Para usarlos** (abrir en QGIS, copiar al TP2): al **abrirlos o copiarlos**, Drive
  los descarga automáticamente. Tras descargarse, el ícono cambia a un **tilde verde**.
- **Para forzar la descarga** y dejarlos siempre disponibles sin conexión: clic derecho
  sobre el archivo o carpeta → **"Disponible sin conexión"**.

> En este TP, antes de abrir `ESA8_Naposta_2021.tif` en QGIS conviene copiarlo desde
> `H:\Mi unidad\TP2_LULC` a la carpeta local `00_Area_estudio` del TP2; al copiarlo se
> descarga y queda guardado en su disco.

---

## 6. Si aparece un cuadro de "TeraCopy" al copiar/pegar

Si su PC tiene instalado **TeraCopy**, al pegar archivos puede abrirse un cuadro
**"Copy & Paste"** preguntando con qué copiar. Para una copia simple, elija **Explorer**
("Use Explorer to paste files"). Verifique que el **origen** y el **destino** mostrados
sean los correctos antes de aceptar.

---

## Apartado para el/la docente

- El error "El parámetro no es correcto" tiene **dos causas distintas** que conviene
  separar para los alumnos: (a) Drive recién iniciado y aún montando —se resuelve
  esperando— y (b) la incompatibilidad estructural del Acceso rápido con la unidad
  virtual de Drive —no se resuelve, se evita—.
- Recomiende a los alumnos **copiar** los productos de GEE desde Drive al disco local
  (a `00_Area_estudio` / `05_Resultados_LULC`) antes de procesarlos, para no depender de
  la conexión ni del estado "en la nube".
- La letra de unidad de Drive **varía por equipo**; pida que identifiquen la unidad por
  el **ícono/nombre**, no por la letra.
