---
title: "Tesseract y OCRmyPDF en OSINT: convertir escaneos en texto sin convertir errores en hechos"
slug: /tesseract-ocrmypdf-osint-documentos-publicos
authors: [osint-writter]
tags: [osint, investigation, verification, methodology, tooling, privacy]
date: 2026-09-03
image: /img/blog/2026-09-03-ocr-reproducible-documentos-publicos.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista comparando un documento escaneado intacto con su capa de texto OCR y un cuaderno de procedencia](/img/blog/2026-09-03-ocr-reproducible-documentos-publicos.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/tesseract-ocrmypdf-osint-documentos-publicos.m4a)


*Imagen generada mediante inteligencia artificial.*

Un contrato público escaneado contiene justo la cifra que resolvería una discrepancia, pero el buscador del repositorio no la encuentra. Tras aplicar OCR aparece «18.000 euros»; al ampliar la página, el papel dice «13.000». El programa no ha descubierto un dato oculto: **ha formulado una conjetura sobre píxeles**. Si esa conjetura entra en una hoja de cálculo sin conservar página, recorte y original, el error adquiere apariencia de hecho.

Tesseract y OCRmyPDF permiten hacer consultables grandes colecciones de documentos, pero su valor OSINT no está en producir texto perfecto. Está en construir un índice de trabajo reproducible, localizar pasajes candidatos y volver siempre a la imagen fuente antes de afirmar nada.

<!-- truncate -->

Este artículo propone un flujo local para documentos públicos obtenidos legítimamente. Las fuentes técnicas se consultaron el **3 de septiembre de 2026**. La entidad, los expedientes, los nombres y las cifras del ejemplo son ficticios. No se usa OCR para reconstruir datos ocultos, eludir controles de acceso ni tratar documentación privada sin base legal.

## Qué son Tesseract y OCRmyPDF

[Tesseract](https://tesseract-ocr.github.io/tessdoc/) es un motor de reconocimiento óptico de caracteres que puede procesar imágenes desde la línea de comandos o mediante una API. Su salida puede ser texto plano, PDF, hOCR o [TSV con coordenadas y confianza por elemento](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html). Esta última representación resulta útil para auditar dónde creyó ver cada palabra, aunque una confianza alta tampoco convierte el resultado en verdadero.

[OCRmyPDF](https://ocrmypdf.readthedocs.io/en/latest/introduction.html) orquesta Tesseract y otras herramientas para añadir una capa de texto buscable a un PDF escaneado. Puede conservar la imagen visible, producir un PDF de salida y generar un fichero de texto auxiliar o *sidecar*. También ofrece rotación y corrección de inclinación. Son transformaciones útiles para trabajar; no certifican la autenticidad del documento ni corrigen su contenido.

Conviene separar desde el principio cuatro objetos:

| Objeto | Para qué sirve | Lo que no demuestra |
| --- | --- | --- |
| PDF original | fija los bytes adquiridos y su representación recibida | que el emisor sea auténtico o que el contenido sea veraz |
| PDF procesado | facilita búsqueda, selección y revisión visual | identidad binaria con el original |
| texto OCR | permite filtrar y localizar términos candidatos | ortografía, cifras o lectura exactas |
| TSV/hOCR | aporta posición, segmentación y señales de confianza | certeza semántica ni procedencia documental |

El OCR es, por tanto, una **capa derivada**. Debe poder borrarse y reconstruirse sin perder el original ni la historia de cómo se obtuvo.

## Caso de uso legítimo: revisar actas públicas escaneadas

El ayuntamiento ficticio de **Villa Serena** publica 86 actas históricas como PDF de imagen. Una asociación vecinal quiere comprobar cuándo apareció por primera vez la partida «Mejora del mercado central» y cómo cambiaron sus importes. El encargo se limita a documentos del portal oficial; no incluye datos personales ajenos al asunto.

El equipo define una hipótesis estrecha: «localizar páginas que puedan contener el nombre de la partida y verificar visualmente fecha, importe y contexto en cada original». No delega al OCR la decisión sobre qué se aprobó. Tampoco suma automáticamente cifras extraídas, porque `3`, `8`, `0`, puntos y comas se confunden con facilidad en copias degradadas.

El resultado esperado es una tabla con URL, fecha de adquisición, hash, página, transcripción comprobada, recorte de referencia y observaciones. El texto automático solo sirve para proponer qué páginas revisar.

## Flujo recomendado, paso a paso

### 1. Adquiere, identifica y no sobrescribas

Guarda cada fichero tal como se recibió, registra la URL pública y calcula su hash antes de procesarlo:

```bash
mkdir -p originales derivados notas
sha256sum originales/acta-042.pdf > notas/acta-042.sha256
pdfinfo originales/acta-042.pdf > notas/acta-042.pdfinfo.txt
```

Anota además la fecha y hora de consulta en UTC, las cabeceras HTTP que ayuden a identificar la representación y cualquier identificador oficial del expediente. El hash responde únicamente por esos bytes: no prueba autoría, publicación anterior ni integridad de la cadena de custodia fuera de tu captura.

No trabajes sobre el único ejemplar. Aunque OCRmyPDF puede operar sobre un mismo nombre en determinados usos, una investigación debe mantener una separación visible entre adquisición y derivado.

### 2. Comprueba si el PDF ya contiene texto

Antes de aplicar OCR, intenta extraer una muestra:

```bash
pdftotext originales/acta-042.pdf - | sed -n '1,40p'
```

Un resultado vacío sugiere páginas de imagen, pero no lo demuestra para todo el documento. Un PDF mixto puede combinar texto digital, escaneos y una capa OCR previa. La [documentación de errores de OCRmyPDF](https://ocrmypdf.readthedocs.io/en/stable/errors.html) distingue opciones como `--skip-text`, que evita reprocesar páginas con texto, y `--redo-ocr`, que sustituye una capa OCR existente sin rasterizar el texto imprimible. `--force-ocr` es más invasiva porque rasteriza el contenido; no debe convertirse en el botón reflejo.

Registra la decisión por fichero. Si el original ya permite búsquedas razonables, quizá no necesites transformarlo.

### 3. Instala desde una fuente mantenida y fija el entorno

Sigue las guías oficiales de [instalación de Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html) y [OCRmyPDF](https://ocrmypdf.readthedocs.io/en/latest/installation.html) para tu sistema. Asegúrate de instalar el modelo de idioma adecuado; `spa` corresponde al castellano. Después conserva las versiones realmente usadas:

```bash
tesseract --version > notas/version-tesseract.txt
tesseract --list-langs > notas/idiomas-tesseract.txt
ocrmypdf --version > notas/version-ocrmypdf.txt
```

No escribas en el informe «se usó la última versión». Escribe la salida concreta y, si el trabajo ha de repetirse meses después, documenta también el sistema, los modelos de idioma y las opciones. Tesseract mantiene familias de datos entrenados con distintos compromisos de velocidad y precisión; su [documentación de modelos](https://tesseract-ocr.github.io/tessdoc/Data-Files.html) permite elegirlos conscientemente.

### 4. Crea un derivado buscable y un sidecar

Para un lote en castellano con páginas posiblemente giradas o inclinadas, una primera pasada prudente podría ser:

```bash
ocrmypdf \
  --language spa \
  --rotate-pages \
  --deskew \
  --sidecar derivados/acta-042.txt \
  originales/acta-042.pdf \
  derivados/acta-042-ocr.pdf \
  2> notas/acta-042-ocr.log
```

El fichero `.txt` sirve para búsqueda rápida; el PDF derivado facilita saltar al pasaje y compararlo con la imagen. Conserva también la salida de diagnóstico. No encadenes limpieza agresiva, compresión y OCR sin probar una muestra: cada transformación adicional complica atribuir por qué cambió una lectura.

Si el documento mezcla castellano y otra lengua conocida, Tesseract admite combinaciones como `spa+eng`, pero añadir idiomas «por si acaso» puede cambiar segmentación y resultados. Registra el orden y compara una muestra representativa antes de procesar el lote.

### 5. Usa el texto para recuperar, no para concluir

Busca variantes previsibles y conserva la página donde aparece cada candidata:

```bash
rg -ni "mercado central|mercado-centra|mejora del mercado" \
  derivados/*.txt

pdftotext -f 12 -l 12 -layout \
  derivados/acta-042-ocr.pdf \
  derivados/acta-042-p12.txt
```

Una búsqueda exacta pierde errores de OCR; una expresión demasiado amplia genera ruido. Construye un pequeño diccionario con abreviaturas, guiones de final de línea y confusiones observadas en **esa colección**, no una lista universal inventada de antemano.

Para palabras críticas, Tesseract puede producir TSV:

```bash
tesseract recortes/acta-042-p12.png \
  derivados/acta-042-p12 -l spa tsv
```

El TSV ayuda a volver a las coordenadas y priorizar elementos de baja confianza. La confianza es una señal del reconocedor, no una probabilidad calibrada de que la frase completa sea correcta.

### 6. Verifica cifras, nombres y negaciones en la imagen

Toda afirmación material debe cotejarse con la página visible del original. Amplía el recorte, lee las líneas anteriores y posteriores y, si persiste la ambigüedad, marca el carácter dudoso en vez de adivinarlo.

Presta especial atención a:

- importes, porcentajes, fechas y números de expediente;
- nombres propios y siglas poco frecuentes;
- signos negativos, decimales, puntos y comas;
- palabras partidas entre líneas o columnas;
- casillas, tablas, sellos, notas marginales y texto manuscrito;
- negaciones como «no», que pueden desaparecer y cambiar el sentido.

Una transcripción honesta puede contener `[ilegible]`, alternativas como `[3/8]` o un intervalo. La incertidumbre visible es mejor evidencia que una cifra impecable fabricada por el software.

### 7. Mide el error con una muestra útil

No declares que «el OCR tiene un 95 % de precisión» porque una interfaz muestre confianzas altas. Selecciona páginas representativas: limpias, inclinadas, con tablas, fotocopias y tipografías difíciles. Transcribe manualmente una muestra y clasifica errores según el riesgo del encargo.

| Error | Impacto en el caso | Control recomendado |
| --- | --- | --- |
| acento o puntuación | bajo para recuperar términos | búsqueda con variantes y revisión visual |
| palabra común | medio | contexto de línea y segunda lectura |
| nombre de entidad | alto | cotejo con encabezado e identificador oficial |
| cifra, fecha o negación | crítico | doble comprobación visual y fuente independiente |
| orden de columnas | crítico en tablas | reconstrucción manual de fila y cabeceras |

Las recomendaciones oficiales de [calidad de Tesseract](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html) explican que inclinación, resolución, ruido, bordes y segmentación de página influyen en el resultado. Optimizar una muestra puede ayudar, pero documenta cada preprocesado y conserva la imagen anterior.

### 8. Publica una pista auditable

Para cada cita, conserva al menos:

- URL e identificador del documento público;
- hash y nombre del original adquirido;
- número de página del PDF original y del derivado;
- comando, versiones, idioma y registro de ejecución;
- texto OCR bruto separado de la transcripción verificada;
- recorte o referencia visual proporcionada;
- persona o procedimiento que comprobó el pasaje;
- incertidumbres y corroboración externa.

Si compartes resultados, cita el documento y la página, no solo el `.txt` generado. El lector debe poder inspeccionar la representación visible de la que procede la afirmación.

## Limitaciones y falsos positivos

El OCR falla de formas sistemáticas. Puede unir columnas, insertar encabezados en mitad de una frase, confundir ruido con puntuación, perder superíndices o leer un sello encima del texto. Los formularios y tablas rompen el orden de lectura; la escritura manuscrita requiere modelos y controles distintos. Un PDF con firma digital también merece cautela: producir un derivado puede invalidar o eliminar propiedades que debían examinarse en el original.

Hay otro falso positivo más sutil: creer que encontrar dos veces el mismo nombre identifica a la misma persona. El OCR no resuelve homónimos, cargos ni fechas de vigencia. Solo transforma una imagen en símbolos candidatos. La resolución de entidades sigue exigiendo identificadores, contexto temporal y fuentes independientes.

Tampoco confundas PDF/A con verdad o inmutabilidad. OCRmyPDF puede generar este formato por defecto, pero un contenedor orientado a archivo no autentica el contenido ni reemplaza el hash del fichero adquirido.

## OPSEC, ética y privacidad

Procesar localmente reduce la exposición frente a subir documentos a un servicio desconocido, pero «local» no significa automáticamente seguro. La documentación de [seguridad de PDF de OCRmyPDF](https://ocrmypdf.readthedocs.io/en/latest/pdfsecurity.html) advierte de que la herramienta no está diseñada para proteger frente a PDF malicioso. Trata ficheros no confiables en un entorno aislado, actualizado, sin credenciales ni acceso innecesario a la red. OCR no es un sanitizador.

Aplica además estas reglas:

1. Trabaja solo con material público o autorizado y una finalidad definida.
2. Minimiza el lote, los recortes y los datos personales conservados.
3. No intentes «recuperar» texto deliberadamente censurado ni sortear restricciones.
4. Separa originales, derivados, índices y publicaciones.
5. No expongas un servicio OCR público sin un diseño específico de seguridad y límites de recursos.
6. Revisa manualmente antes de asociar una cifra o identidad a alguien.
7. Elimina derivados temporales cuando termine su finalidad y conserva lo exigido por tu política de evidencia.

## Alternativas y siguientes pasos

Para una sola imagen, Tesseract directo ofrece salidas estructuradas y control de segmentación. Para PDF, OCRmyPDF reduce la necesidad de desmontar y reconstruir manualmente el contenedor. En escritorios existen aplicaciones de OCR y gestores documentales; en archivos de gran escala puede convenir un motor comercial o un flujo especializado en manuscritos. Compáralos con un conjunto de prueba propio, no por una cifra comercial aislada.

Si el documento nació digital y ya contiene texto fiable, `pdftotext`, las propiedades del PDF y una revisión del diseño pueden ser suficientes. Si el reto real son tablas, separa la extracción tabular del reconocimiento y valida filas, columnas y cabeceras contra la página.

El siguiente paso natural será estudiar **cómo extraer tablas de documentos públicos sin desplazar columnas ni fabricar relaciones entre celdas**. Hasta entonces, quédate con una regla operativa: **el OCR encuentra dónde mirar; la evidencia sigue estando en el documento, su procedencia y la comprobación reproducible**.
