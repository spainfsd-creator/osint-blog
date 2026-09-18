---
title: "BagIt en OSINT: transferir evidencia sin confundir integridad con verdad"
slug: /bagit-osint-transferencia-evidencia
authors: [osint-writter]
tags: [osint, methodology, verification, data, privacy, tooling]
date: 2026-09-18
image: /img/blog/2026-09-18-bagit-osint-transferencia-evidencia.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista verificando manifiestos y recibiendo un paquete digital de evidencia](/img/blog/2026-09-18-bagit-osint-transferencia-evidencia.png)

*Imagen generada mediante inteligencia artificial.*

Una redacción entrega a su equipo jurídico 48 GB de documentos públicos, capturas web y tablas derivadas. La copia termina sin avisos, pero dos ficheros llegan truncados, un nombre cambia al descomprimir y nadie puede distinguir un original de una exportación posterior. El hallazgo quizá siga siendo correcto; **la transferencia que debía sostenerlo ya no es verificable**.

[BagIt](https://www.rfc-editor.org/rfc/rfc8493) aporta una estructura mínima para almacenar y transferir conjuntos de ficheros con inventarios y sumas de comprobación. En OSINT permite que emisor y receptor comprueben que la carga esperada está completa y conserva los mismos bytes. No demuestra que un documento sea auténtico, que una captura represente toda la página ni que la investigación esté bien interpretada.

<!-- truncate -->

## Qué es BagIt y para qué sirve

BagIt es un formato jerárquico descrito en la [RFC 8493](https://www.rfc-editor.org/rfc/rfc8493), publicada en octubre de 2018 como documento informativo. Una «bolsa» contiene una carga —el *payload*— dentro de `data/` y varios ficheros de control —los *tag files*— en su raíz.

Su estructura esencial es pequeña:

```text
entrega-osint/
├── bagit.txt
├── manifest-sha256.txt
└── data/
    ├── README.md
    ├── fuentes/
    ├── notas/
    └── resultados/
```

`bagit.txt` declara la versión del formato y la codificación. Cada `manifest-<algoritmo>.txt` enumera **todos** los ficheros del *payload* y asocia su ruta con una suma de comprobación. Puede añadirse `bag-info.txt` con metadatos legibles por personas y un `tagmanifest-<algoritmo>.txt` que proteja también los ficheros de control.

La especificación distingue dos conceptos que conviene no mezclar:

- una bolsa **completa** contiene los elementos obligatorios y todos los ficheros enumerados;
- una bolsa **válida** es completa y, además, todas las sumas de los manifiestos coinciden con los ficheros recibidos.

Eso prueba integridad con respecto al manifiesto, no verdad factual. Un PDF falso puede viajar intacto; una selección sesgada puede estar perfectamente empaquetada; un hash correcto no identifica por sí solo al autor ni la fecha real del contenido.

## Caso de uso legítimo: entregar una investigación sobre contratación pública

Imaginemos una investigación ficticia sobre contratos de mantenimiento de Villa Ejemplo. El equipo ha descargado expedientes de un portal oficial, conservado respuestas web, normalizado importes y producido una tabla agregada. Debe entregar una copia revisable a otra unidad sin incluir datos personales irrelevantes ni notas sobre fuentes confidenciales.

Antes de crear la bolsa prepara una carpeta de trabajo nueva:

```text
entrega-villa-ejemplo/
├── README.md
├── fuentes/
│   ├── contratos-2025.csv
│   └── ficha-descarga.md
├── codigo/
│   └── normalizar.py
└── resultados/
    └── gasto-anual.csv
```

El `README` explica la pregunta, alcance y límites. `ficha-descarga.md` registra URL, consulta, fecha y hora UTC, licencia y método de adquisición. Los nombres, identificadores e importes del ejemplo publicado son sintéticos; la adquisición real permanece en el entorno autorizado.

BagIt resulta útil en la frontera entre dos responsabilidades: quien envía declara qué entrega y quien recibe valida qué ha llegado. No reemplaza el inventario intelectual, el control de accesos, la cadena de custodia organizativa ni la corroboración de las conclusiones.

## Flujo recomendado, paso a paso

### 1. Definir el alcance antes de empaquetar

Escribe qué debe cruzar la frontera de la entrega y qué debe quedarse fuera. Clasifica cada elemento como original preservado, derivado, resultado publicable, documentación o material excluido. Revisa datos personales, credenciales, rutas locales, cookies, consultas sensibles y nombres de fuentes protegidas.

No conviertas la carpeta de trabajo cotidiana directamente. Crea una copia de entrega minimizada y revísala como si fuera a abrirla una persona ajena al caso.

### 2. Preparar procedencia y contexto

BagIt trata los ficheros como secuencias opacas de bytes: no interpreta un CSV ni entiende la relación entre una captura y su URL. Por eso el *payload* necesita documentación propia.

Como mínimo, registra para cada adquisición:

- URL o identificador de origen;
- fecha y hora UTC;
- consulta, filtros y paginación;
- herramienta y método utilizados;
- licencia o condiciones de reutilización;
- transformaciones aplicadas;
- huecos, errores y decisiones de exclusión.

Un esquema como [RO-Crate](https://www.researchobject.org/ro-crate/specification) puede añadir metadatos estructurados y relaciones semánticas. Ambas piezas resuelven problemas distintos: BagIt se concentra en estructura, inventario e integridad de transferencia; RO-Crate describe qué son los recursos y cómo se relacionan.

### 3. Crear una bolsa de laboratorio

La implementación abierta [bagit-python de la Library of Congress](https://github.com/LibraryOfCongress/bagit-python) ofrece biblioteca y utilidad de línea de comandos. Instálala en un entorno aislado y verifica primero sus opciones locales:

```bash
python3 -m venv .venv-bagit
. .venv-bagit/bin/activate
python -m pip install bagit
python -m bagit --help
```

Trabaja con una copia y no con los únicos originales. Para convertir el directorio ficticio y generar un manifiesto SHA-256:

```bash
cp -a entrega-villa-ejemplo entrega-villa-ejemplo-bag
python -m bagit --sha256 entrega-villa-ejemplo-bag
```

La herramienta reorganiza el contenido como *payload* y genera los ficheros BagIt. Antes de enviarlo, inspecciona la estructura y valida:

```bash
find entrega-villa-ejemplo-bag -maxdepth 2 -type f -print
python -m bagit --validate entrega-villa-ejemplo-bag
```

La documentación de `bagit-python` también ofrece validación rápida basada en estructura y `Payload-Oxum`. Úsala solo como *triage*: cuando importa comprobar los bytes, ejecuta la validación completa de los manifiestos.

### 4. Cerrar la entrega sin borrar el original

Una vez creados los manifiestos, cualquier cambio legítimo en `data/` exige regenerarlos de forma consciente y documentar una nueva versión. No «arregles» el contenido recibido y actualices el hash silenciosamente: eso destruye la posibilidad de comparar la entrega con lo que salió del emisor.

Conserva por separado:

- la copia de origen preservada;
- la bolsa exacta que se envía;
- el identificador de la entrega, fecha UTC y canal;
- el resultado de la validación previa;
- la confirmación y validación del receptor.

Si serializas la carpeta como ZIP o TAR para transportarla, acuerda formato, convenciones de nombres y procedimiento de extracción. BagIt define una estructura de directorios; un contenedor comprimido y su cifrado son capas adicionales.

### 5. Validar en recepción y guardar el informe

El receptor debe validar desde su propia copia y entorno, no aceptar una captura verde enviada por el emisor. Un procedimiento mínimo es:

```bash
python -m bagit --validate entrega-villa-ejemplo-bag
```

Registra herramienta, entorno, hora UTC y resultado. Si falla, conserva la copia defectuosa, identifica si falta un fichero, sobra uno o no coincide una suma, y solicita una nueva transferencia con un identificador distinto. No sobrescribas la evidencia del fallo.

Para intercambios repetidos, un [BagIt Profile](https://bagit-profiles.github.io/bagit-profiles-specification/) puede fijar algoritmos admitidos, versión de BagIt, ficheros obligatorios y reglas de serialización. Un perfil reduce ambigüedad entre organizaciones; no convierte automáticamente su implementación en segura.

## `fetch.txt`: útil, pero no una descarga inocente

BagIt permite un `fetch.txt` opcional con URL, longitud y ruta de destino para cargas que el receptor debe obtener. Es práctico para objetos grandes, pero introduce red, disponibilidad, autenticación y contenido cambiante en el proceso.

Un receptor responsable debe tratarlo como entrada no confiable:

- permitir solo esquemas y destinos previstos;
- impedir que una ruta escape de la raíz de la bolsa;
- aplicar límites de tamaño, tiempo y redirecciones;
- aislar la descarga de redes y credenciales sensibles;
- no ejecutar ni previsualizar automáticamente lo descargado;
- comprobar después la suma declarada en el manifiesto;
- registrar la URL efectiva, UTC y errores de recuperación.

La propia RFC advierte de caracteres especiales de directorio y exige que una implementación no acceda a ficheros fuera de la estructura. Una suma válida después de descargar confirma que se obtuvo el objeto esperado por el manifiesto, no que la URL siga siendo la fuente legítima ni que el contenido sea seguro.

## Limitaciones y falsos positivos

### Un hash no autentica la fuente

SHA-256 puede demostrar que dos copias contienen los mismos bytes con una probabilidad práctica muy alta. No demuestra quién creó el fichero, cuándo ni si fue manipulado **antes** de calcular el hash. Para sostener autenticidad necesitas procedencia documentada, preservación temprana, firmas cuando existan y corroboración independiente.

### `bag-info.txt` no es un registro probado

Los campos de `bag-info.txt` son metadatos declarados. Ayudan a operar y entender la entrega, pero una persona puede escribir valores equivocados. Si un dato es crítico, contrástalo con registros externos y separa observaciones, declaraciones e inferencias.

### La validez no mide calidad ni suficiencia

Una bolsa puede ser válida y contener un conjunto incompleto para la pregunta investigada. También puede incluir duplicados, fechas mal interpretadas o una transformación defectuosa. Añade pruebas de esquema, recuentos, controles de duplicados y revisión metodológica; no los confundas con la validación BagIt.

### La interoperabilidad tiene bordes

Codificaciones, nombres de fichero, sensibilidad a mayúsculas y restricciones distintas entre Windows y Unix pueden romper intercambios. La [suite de conformidad de BagIt](https://github.com/LibraryOfCongress/bagit-conformance-suite) reúne bolsas válidas e inválidas para probar implementaciones. Ensaya con el mismo perfil y plataformas reales antes de una entrega crítica.

## Buenas prácticas de OPSEC, ética y privacidad

- Empaqueta solo material necesario para una finalidad legítima y documentada.
- Separa originales, derivados, resultados publicables y notas restringidas.
- Elimina secretos, cookies, tokens, rutas personales y metadatos innecesarios.
- No incluyas identidades de fuentes protegidas en nombres, logs ni `bag-info.txt`.
- Cifra el transporte cuando el riesgo lo requiera; los hashes no aportan confidencialidad.
- Usa canales y destinatarios verificados, con permisos mínimos y caducidad razonable.
- Trata toda bolsa recibida como contenido no confiable y analízala en un entorno aislado.
- Evita abrir automáticamente HTML, documentos activos, enlaces o binarios.
- Conserva la versión recibida antes de cualquier normalización o extracción.
- Documenta quién creó, envió, recibió y validó cada entrega, sin exagerar lo que ese registro prueba.
- Define retención y borrado: empaquetar no crea derecho a conservar indefinidamente.
- Publica límites, exclusiones y errores junto con los resultados.

## Lista de control antes de aceptar una bolsa

- [ ] El alcance y el identificador de la entrega están escritos.
- [ ] El *payload* contiene solo datos necesarios y autorizados.
- [ ] `bagit.txt`, `data/` y al menos un manifiesto están presentes.
- [ ] Cada fichero del *payload* aparece exactamente una vez en cada manifiesto aplicable.
- [ ] La validación completa termina correctamente en la copia recibida.
- [ ] El resultado de validación conserva herramienta, entorno y UTC.
- [ ] Las rutas no escapan de la raíz ni provocan colisiones en la plataforma destino.
- [ ] Cualquier `fetch.txt` se procesa con red, tamaño y destinos restringidos.
- [ ] Los ficheros activos se analizan sin ejecución ni previsualización automática.
- [ ] Procedencia, consulta, licencia y transformaciones están documentadas aparte.
- [ ] La conclusión se ha corroborado; no se deduce de un hash correcto.
- [ ] La retención, acceso y procedimiento de borrado están definidos.

## Alternativas y siguientes pasos

Para una entrega pequeña, un directorio coherente, un `README` y un manifiesto SHA-256 firmado pueden bastar. [RO-Crate](/ro-crate-osint-paquete-evidencia) aporta una descripción más rica de entidades y relaciones. [Frictionless Data Package](https://specs.frictionlessdata.io/data-package/) describe colecciones de recursos y resulta especialmente útil para datos tabulares. WARC conserva respuestas web con su contexto de captura, y sistemas de almacenamiento con versionado ayudan a mantener objetos a lo largo del tiempo.

No elijas por acumulación de siglas. Pregunta qué necesitas demostrar: que llegaron los mismos bytes, que el conjunto se entiende, que una tabla cumple un esquema o que una página fue capturada con cabeceras y respuestas. Esas necesidades pueden combinarse, pero no son equivalentes.

El takeaway accionable: crea hoy una bolsa con tres ficheros sintéticos, valídala, modifica un byte de una copia y observa el fallo. Después entrégala a otra máquina y registra la validación de recepción. Entender ese circuito sencillo vale más que añadir manifiestos que nadie comprueba.

Como siguiente tema, convendría comparar BagIt, RO-Crate y Frictionless Data Package sobre el mismo conjunto ficticio para decidir qué capa aporta integridad, contexto o validación tabular.

## Fuentes consultadas

- [RFC 8493: The BagIt File Packaging Format (V1.0)](https://www.rfc-editor.org/rfc/rfc8493)
- [bagit-python, Library of Congress](https://github.com/LibraryOfCongress/bagit-python)
- [BagIt Conformance Suite, Library of Congress](https://github.com/LibraryOfCongress/bagit-conformance-suite)
- [BagIt Profiles Specification 1.4.0](https://bagit-profiles.github.io/bagit-profiles-specification/)
- [RO-Crate: combinar con otros esquemas de empaquetado](https://www.researchobject.org/ro-crate/1.1/appendix/implementation-notes.html#combining-with-other-packaging-schemes)
- [Frictionless Data Package](https://specs.frictionlessdata.io/data-package/)
