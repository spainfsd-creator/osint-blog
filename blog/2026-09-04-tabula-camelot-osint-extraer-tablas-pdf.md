---
title: "Tabula y Camelot en OSINT: extraer tablas de PDF sin fabricar relaciones entre celdas"
slug: /tabula-camelot-osint-extraer-tablas-pdf
authors: [osint-writter]
tags: [osint, investigation, verification, methodology, tooling, privacy]
date: 2026-09-04
image: /img/blog/2026-09-04-tabula-camelot-tablas-pdf-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista contrastando una tabla PDF con su extracción estructurada y un cuaderno de procedencia](/img/blog/2026-09-04-tabula-camelot-tablas-pdf-osint.png)

*Imagen generada mediante inteligencia artificial.*

Un informe público reparte el presupuesto de cuatro ejercicios en una tabla de 40 páginas. La extracción automática entrega un CSV impecable, pero una celda combinada ha desplazado todos los importes una columna a la derecha. La suma cuadra; la historia que cuenta, no. **Convertir un PDF en filas y columnas no es copiar datos: es proponer una estructura que debe demostrarse contra la página original**.

[Tabula](https://tabula.technology/) y [Camelot](https://camelot-py.readthedocs.io/en/stable/) permiten liberar tablas encerradas en PDF de texto. Son útiles para contratos, presupuestos, estadísticas y anexos publicados legítimamente. También pueden producir resultados muy convincentes y completamente equivocados si confundimos líneas dibujadas, espacios o coordenadas con relaciones semánticas.

<!-- truncate -->

Este artículo presenta un flujo reproducible y prudente. Las fuentes oficiales se consultaron el **4 de septiembre de 2026**. La entidad, los documentos, las cifras y todos los resultados del ejemplo son ficticios. El objetivo es verificar documentación pública, no eludir controles de acceso ni tratar datos personales sin una finalidad legítima.

## Qué extraen realmente Tabula y Camelot

Un PDF describe cómo representar una página. Puede contener caracteres posicionados, trazos, rectángulos e imágenes, pero no tiene por qué declarar que un conjunto de objetos constituye una tabla, una fila o una cabecera. Por eso una cuadrícula que el ojo entiende al instante puede ser ambigua para el software.

Tabula ofrece una interfaz visual: el analista selecciona un área de la página, revisa una previsualización y exporta CSV o TSV. Su documentación advierte de una condición decisiva: funciona con PDF basados en texto, no con páginas que solo contienen una imagen escaneada.

Camelot es una biblioteca de Python con distintos métodos de análisis. Su [explicación técnica](https://camelot-py.readthedocs.io/en/stable/user/how-it-works.html) distingue, entre otros, `lattice`, que busca líneas y sus intersecciones, y `stream`, que infiere la estructura a partir de espacios y posiciones del texto. Las versiones documentadas también incluyen enfoques `network` e `hybrid`. Elegir un método cambia la hipótesis estructural; no es un simple ajuste de rendimiento.

| Capa | Pregunta que responde | Lo que no demuestra |
| --- | --- | --- |
| PDF adquirido | ¿Qué bytes y páginas recibió el analista? | autenticidad o veracidad del emisor |
| área seleccionada | ¿Qué región se pidió interpretar? | que todo lo incluido pertenezca a la tabla |
| estructura detectada | ¿Dónde propuso el programa filas y columnas? | significado de celdas o cabeceras |
| CSV exportado | ¿Qué valores produjo esa configuración? | fidelidad respecto al documento |
| tabla verificada | ¿Qué celdas se cotejaron con la página? | que el resto del documento sea correcto |

Una métrica de extracción tampoco sustituye esa última capa. Camelot expone un `parsing_report` con señales como `accuracy` y `whitespace`; sirven para comparar ejecuciones, no para certificar que un importe quedó asociado a la partida correcta.

## Caso de uso legítimo: comparar presupuestos públicos

El consorcio ficticio **Bahía Serena** publica cuatro memorias anuales. Cada PDF incluye una tabla llamada «Inversiones por programa», con partidas, presupuesto inicial, modificaciones y ejecución. Una asociación quiere comprobar la evolución de tres programas sin atribuir irregularidades ni perfilar a empleados.

El encargo se formula así:

> Construir una tabla comparativa de las partidas declaradas en las memorias oficiales, manteniendo para cada valor la referencia exacta a documento, página, fila y cabecera, y marcar como incierto cualquier dato cuya estructura no pueda validarse visualmente.

Esta formulación evita dos atajos peligrosos: asumir que el mismo rótulo identifica la misma categoría todos los años y sumar cifras antes de comprobar unidades, notas al pie y columnas. El resultado debe permitir volver desde cada celda hasta la representación visible que la sustenta.

## Flujo recomendado paso a paso

### 1. Busca primero una fuente estructurada

Antes de extraer un PDF, comprueba si el organismo publica el mismo conjunto como CSV, XLSX, JSON o mediante una API. Una tabla nativa suele conservar tipos, identificadores y relaciones mejor que una reconstrucción visual. Registra su URL, licencia, fecha de actualización y cobertura; no des por hecho que coincide con el PDF.

Si el PDF es la fuente autoritativa o la única disponible, descarga la representación permitida y fija su identidad:

```bash
mkdir -p originales derivados notas
sha256sum originales/memoria-2025.pdf \
  > notas/memoria-2025.sha256
pdfinfo originales/memoria-2025.pdf \
  > notas/memoria-2025.pdfinfo.txt
```

El hash identifica esos bytes. No prueba quién creó el documento, cuándo apareció por primera vez ni si sus afirmaciones son ciertas.

### 2. Clasifica la página antes de elegir herramienta

Intenta seleccionar unas palabras en el visor y extrae una muestra con una herramienta local. Si no hay caracteres, probablemente estás ante una página de imagen y ni Tabula ni Camelot podrán reconstruir por sí solos el contenido. Si existe una capa OCR, puede estar desalineada respecto a lo visible.

Registra por página:

- texto nativo, imagen o combinación de ambos;
- tabla con bordes, sin bordes o diseño mixto;
- cabeceras de varios niveles y celdas combinadas;
- páginas apaisadas, rotadas o recortadas;
- unidades, notas al pie y filas que continúan en otra página.

El post anterior explicó cómo crear y verificar una capa OCR. Aquí esa capa se considera un derivado falible: las cifras críticas siguen cotejándose con la imagen del original.

### 3. Empieza con una página y una tabla

En Tabula, importa una copia local, selecciona únicamente la tabla y revisa la previsualización antes de exportar. No marques toda la página por comodidad: títulos, números de página y notas pueden terminar como filas falsas. Prueba la detección sugerida por la interfaz y ajusta el área si una cabecera o un total queda fuera.

Guarda junto al CSV una captura o una nota con:

- hash del PDF;
- número de página impreso y número de página del fichero;
- coordenadas o descripción del área;
- modo de extracción utilizado;
- fecha, sistema y versión de la herramienta;
- problemas visibles y correcciones manuales.

La selección manual no es un defecto: hace explícito el alcance. El defecto sería conservar solo el CSV y olvidar cómo se obtuvo.

### 4. Automatiza con una configuración declarada

Cuando el diseño se repite, Camelot permite convertir la hipótesis en código. Para una tabla con cuadrícula visible puede probarse `lattice`:

```python
import camelot

tables = camelot.read_pdf(
    "originales/memoria-2025.pdf",
    pages="12",
    flavor="lattice",
)

print(tables[0].parsing_report)
tables[0].to_csv("derivados/memoria-2025-p12-lattice.csv")
```

Si las columnas se separan mediante espacios y no mediante trazos, compara con `stream`:

```python
tables = camelot.read_pdf(
    "originales/memoria-2025.pdf",
    pages="12",
    flavor="stream",
)
tables[0].to_csv("derivados/memoria-2025-p12-stream.csv")
```

La [documentación avanzada de Camelot](https://camelot-py.readthedocs.io/en/stable/user/advanced.html) permite restringir regiones y áreas, definir columnas o inspeccionar visualmente elementos del análisis. No copies coordenadas de una página a cien páginas sin comprobar que tamaño, rotación, márgenes y diseño se mantienen.

### 5. Visualiza la estructura propuesta

Antes de limpiar valores, superpón sobre la página las líneas, intersecciones o cajas que el algoritmo cree haber encontrado. Camelot proporciona utilidades de trazado y [`pdfplumber`](https://github.com/jsvine/pdfplumber) incluye depuración visual de su detector de tablas mediante `debug_tablefinder`, mostrando líneas, intersecciones y áreas detectadas.

Esta vista contesta preguntas que un CSV oculta:

1. ¿Una línea decorativa se convirtió en frontera de celda?
2. ¿Una cabecera combinada se repitió correctamente sobre sus subcolumnas?
3. ¿Una descripción de dos líneas se partió en dos registros?
4. ¿El total quedó unido a la última categoría?
5. ¿La nota al pie se incorporó como una fila ordinaria?

Conserva la imagen de diagnóstico como artefacto de trabajo. No sustituye al PDF, pero documenta la interpretación aplicada.

### 6. Diseña controles antes de escalar

Extrae primero una muestra que incluya páginas fáciles y difíciles. Define comprobaciones que puedan fallar de forma visible:

| Control | Ejemplo | Respuesta ante fallo |
| --- | --- | --- |
| forma | número esperado de columnas | detener esa página, no rellenar a ciegas |
| tipo | importe convertible con separador conocido | conservar texto bruto y marcar revisión |
| dominio | unidad permitida: euros o miles de euros | volver a cabecera y nota al pie |
| aritmética | subtotales frente a filas publicadas | investigar redondeos y celdas omitidas |
| continuidad | rótulo repetido al cambiar de página | comprobar si es cabecera o nuevo dato |
| procedencia | documento, página y fila presentes | no publicar la celda huérfana |

Que una suma cierre no valida la tabla completa. Dos columnas intercambiadas pueden conservar el total; una fila duplicada y otra omitida pueden compensarse. Combina reglas estructurales, revisión visual y muestreo de valores materiales.

### 7. Separa bruto, normalizado y verificado

No edites silenciosamente el primer CSV hasta que «quede bonito». Mantén tres capas:

1. **Bruta**: salida exacta de la herramienta y configuración utilizada.
2. **Normalizada**: espacios, separadores, unidades y cabeceras tratados mediante reglas registradas.
3. **Verificada**: valores cotejados contra la página, con estado y referencia.

Una tabla de auditoría mínima puede incluir `source_sha256`, `pdf_page`, `printed_page`, `table_area`, `extractor`, `extractor_version`, `raw_value`, `normalized_value`, `verification_status` y `note`. Para cifras importantes, añade una referencia al recorte o a las coordenadas, evitando publicar más datos personales de los necesarios.

### 8. Compara entre años por identificadores, no solo por texto

«Ayudas culturales», «Programa cultural» y «Cultura» podrían ser la misma categoría, tres categorías diferentes o una reorganización. No las fusiones por parecido. Busca códigos presupuestarios, definiciones, periodo de vigencia y notas metodológicas. Si no existe un identificador estable, documenta la regla de correspondencia y permite el estado «sin equivalencia demostrada».

Al publicar resultados, ofrece el dato original, la transformación aplicada y la incertidumbre. Una visualización atractiva sin trazabilidad solo hace más persuasivo un posible error.

## Limitaciones y falsos positivos

Las tablas PDF fallan de manera predecible: columnas sin bordes, filas con alturas variables, números partidos, texto vertical, ligaduras, caracteres superpuestos, cabeceras multinivel y páginas que repiten o no repiten títulos. Las líneas pueden estar formadas por pequeños segmentos; el fondo sombreado puede parecer una frontera. En un escaneo, el OCR añade errores de caracteres y coordenadas antes de que comience la extracción tabular.

Tabula y Camelot declaran que trabajan con PDF de texto. Añadir OCR puede hacer que una página sea técnicamente extraíble, pero no convierte la geometría reconocida en fiable. Camelot ofrece distintas estrategias porque ningún supuesto sirve para todos los diseños.

También existen falsos positivos semánticos. Un guion puede significar cero, no disponible o no aplicable. Los paréntesis pueden indicar valores negativos. Una cabecera «miles de euros» cambia todos los números del cuerpo. Una nota al pie puede excluir categorías del total. Ningún parser conoce automáticamente la política contable del documento.

## OPSEC, ética y privacidad

Extraer localmente reduce la exposición respecto a subir un expediente a un conversor desconocido, pero exige controles. Abre PDF no confiables en un entorno aislado y actualizado; no presupongas que una herramienta de extracción sanitiza contenido malicioso. Respeta las restricciones legítimas de acceso y no intentes romper cifrado o permisos.

Minimiza el material procesado y publicado. Una tabla administrativa puede contener nombres, firmas, teléfonos o identificadores que no son necesarios para responder a la pregunta. Que un dato esté accesible no elimina la obligación de valorar finalidad, proporcionalidad, normativa aplicable y riesgo para las personas.

No conviertas coincidencias en acusaciones. Si una fila parece anómala, verifica la página, el documento completo, la definición de la columna y una fuente oficial independiente antes de describirla. Contacta con la entidad cuando una ambigüedad material pueda aclararse.

## Alternativas y siguientes pasos

Tabula resulta práctica para selección visual y lotes pequeños. Camelot facilita repetir configuraciones, comparar métodos y conservar el flujo como código. `pdfplumber` ofrece acceso detallado a caracteres, líneas, rectángulos y depuración visual cuando necesitas entender por qué falla una página. Para escaneos complejos, formularios o manuscritos quizá haga falta un sistema especializado, pero debe evaluarse con una muestra representativa y criterios propios.

La mejor alternativa sigue siendo una fuente estructurada publicada por el organismo. Si no existe, documenta la extracción como una inferencia reproducible, no como una transcripción infalible.

El siguiente paso natural será estudiar **cómo validar y reconciliar tablas extraídas de varias ediciones sin borrar cambios de esquema ni unidades**. Hasta entonces, conserva esta regla: **cada celda publicada debe poder regresar a su página, su cabecera y su contexto; si no puede, aún no es un dato verificado**.
