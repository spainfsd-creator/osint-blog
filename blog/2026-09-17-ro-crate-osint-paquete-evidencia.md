---
title: "RO-Crate en OSINT: empaquetar evidencia sin empaquetar certezas"
slug: /ro-crate-osint-paquete-evidencia
authors: [osint-writter]
tags: [osint, methodology, data, verification, privacy, tooling]
date: 2026-09-17
image: /img/blog/2026-09-17-ro-crate-osint-paquete-evidencia.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista organizando documentos públicos, metadatos, procedencia y un compartimento privado separado](/img/blog/2026-09-17-ro-crate-osint-paquete-evidencia.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/ro-crate-osint-paquete-evidencia.m4a)


*Imagen generada mediante inteligencia artificial.*

Has terminado una investigación sobre contratación pública. Conservas doce descargas, tres consultas, un cuaderno, dos tablas finales y una carpeta llamada `definitivo-ahora-si`. Seis meses después, otra persona intenta revisar una cifra y descubre que puede abrir los ficheros, pero no sabe cuál es original, cuál es derivado, qué licencia permite redistribuir cada fuente ni qué elementos quedaron fuera por privacidad. **Tener los archivos no equivale a entregar una investigación revisable.**

[RO-Crate](https://www.researchobject.org/ro-crate/) propone describir un conjunto de datos y su contexto mediante un documento JSON-LD legible por máquinas. En OSINT puede servir como índice estructurado de un paquete publicable: qué contiene, quién lo creó, cuándo, bajo qué licencia y cómo se relacionan fuentes, código y resultados. No verifica que una fuente diga la verdad, no calcula hashes por sí solo y no autoriza a publicar material que debe seguir protegido.

<!-- truncate -->

## Qué es RO-Crate y para qué sirve

RO-Crate significa *Research Object Crate*. La [especificación 1.3](https://www.researchobject.org/ro-crate/specification/1.3/), publicada como recomendación el 22 de junio de 2026, define una forma de agregar y describir datos para su distribución, reutilización, publicación, preservación y archivo. Aunque nació alrededor de objetos de investigación, su modelo encaja bien con una necesidad cotidiana del analista OSINT: entregar un conjunto de artefactos acompañado de suficiente contexto para que otra persona entienda qué son y cómo se obtuvieron.

El núcleo es un fichero llamado `ro-crate-metadata.json`. Contiene JSON-LD: objetos conectados mediante identificadores. La entidad raíz representa el conjunto; `hasPart` señala sus componentes; otras entidades pueden describir personas, organizaciones, software, licencias, páginas web o acciones.

Un RO-Crate puede contener datos físicamente dentro de una carpeta o describir recursos externos mediante URI. Esa flexibilidad es útil, pero exige precisión. Una URL remota puede cambiar; un fichero local puede quedar huérfano; una descripción puede ser incorrecta. El formato organiza afirmaciones sobre los artefactos, no las demuestra.

En un paquete OSINT responsable puede ayudar a responder:

- qué ficheros son originales, derivados o resultados publicables;
- de qué URL y consulta procede cada adquisición;
- qué código o herramienta produjo una transformación;
- qué fecha, zona horaria y versión corresponden a cada paso;
- qué licencia o restricción se aplica a cada recurso;
- qué elementos se excluyeron y por qué;
- qué relaciones son observadas y cuáles son inferencias del análisis.

## Caso de uso legítimo: adjudicaciones de un municipio ficticio

Imaginemos que una redacción analiza contratos publicados por el Ayuntamiento de Villa Ejemplo. La pregunta es limitada: comprobar la evolución anual del gasto en mantenimiento de parques. No se investigan domicilios, familiares ni perfiles personales.

El equipo descarga dos CSV del portal oficial, conserva las respuestas originales, normaliza importes y fechas con un script, y publica una tabla agregada. El paquete público podría tener esta estructura:

```text
villa-ejemplo-crate/
├── ro-crate-metadata.json
├── README.md
├── LICENSES.md
├── manifest-sha256.txt
├── data/
│   ├── contratos-2024.csv
│   └── contratos-2025.csv
├── code/
│   └── normalizar.py
├── results/
│   └── gasto-anual.csv
└── notes/
    ├── adquisicion.md
    └── limitaciones.md
```

La carpeta pública no incluye notas internas con teléfonos de contacto, credenciales, rutas del equipo ni una exportación completa que exceda la finalidad. El `README` explica la pregunta; `adquisicion.md` registra URL, parámetros y UTC; `limitaciones.md` enumera huecos y cambios del portal; el manifiesto contiene hashes calculados aparte.

## Un `ro-crate-metadata.json` mínimo

Este ejemplo reducido usa nombres y datos ficticios. No pretende ser un perfil completo, sino mostrar la relación entre el conjunto, sus ficheros y la organización responsable:

```json
{
  "@context": "https://w3id.org/ro/crate/1.3/context",
  "@graph": [
    {
      "@id": "ro-crate-metadata.json",
      "@type": "CreativeWork",
      "about": { "@id": "./" },
      "conformsTo": { "@id": "https://w3id.org/ro/crate/1.3" }
    },
    {
      "@id": "./",
      "@type": "Dataset",
      "name": "Contratos de parques de Villa Ejemplo",
      "description": "Paquete publicable para reproducir una agregación anual",
      "datePublished": "2026-09-17",
      "license": { "@id": "LICENSES.md" },
      "publisher": { "@id": "#equipo" },
      "hasPart": [
        { "@id": "data/contratos-2025.csv" },
        { "@id": "code/normalizar.py" },
        { "@id": "results/gasto-anual.csv" },
        { "@id": "manifest-sha256.txt" }
      ]
    },
    {
      "@id": "data/contratos-2025.csv",
      "@type": "File",
      "name": "Descarga original de contratos de 2025",
      "encodingFormat": "text/csv"
    },
    {
      "@id": "#equipo",
      "@type": "Organization",
      "name": "Laboratorio Cívico Ficticio"
    }
  ]
}
```

La especificación distingue **entidades de datos**, como ficheros y conjuntos, de **entidades contextuales**, como organizaciones, licencias o software. Los `@id` enlazan unas con otras. Conviene usar rutas relativas estables para los objetos incluidos y URI persistentes cuando el recurso vive fuera del paquete.

El JSON-LD no sustituye la explicación humana. Un `README.md` breve debería indicar alcance, instrucciones de reproducción, estructura, contacto y límites. Si se genera una vista HTML del crate, debe tratarse como ayuda de navegación; la fuente estructurada sigue siendo el JSON-LD.

## Flujo recomendado

### 1. Define el paquete publicable antes de copiar archivos

Escribe la pregunta, la audiencia y la finalidad. Clasifica cada artefacto como:

- **original preservado**: bytes obtenidos de una fuente concreta;
- **derivado**: limpieza, conversión, OCR o extracción;
- **resultado**: tabla, gráfico o informe que sostiene la conclusión;
- **contexto**: consulta, licencia, método, limitación o decisión;
- **excluido**: material que no debe distribuirse.

No conviertas «lo tengo en la carpeta» en «puedo publicarlo». Revisa derechos de reutilización, datos personales, secretos, condiciones de acceso y riesgo para fuentes.

### 2. Conserva procedencia por adquisición

Para cada fuente registra al menos URL exacta, hora UTC, método, parámetros, cabeceras relevantes, licencia conocida y hash del fichero recibido. Si una página es dinámica, documenta qué representación preservaste y qué pudo quedar fuera.

No uses `dateModified` como si probara la hora real de un acontecimiento. Distingue la fecha declarada por la fuente, la hora de adquisición y la fecha en que el equipo procesó el artefacto.

### 3. Separa originales, derivados y resultados

Los originales deberían ser inmutables. Las transformaciones deben escribir en otras rutas y conservar el código o la receta. Un resultado necesita una relación clara con sus entradas y con la versión del proceso que lo produjo.

RO-Crate admite describir software y flujos; los [perfiles de Workflow Run Crate](https://www.researchobject.org/ro-crate/profiles.html#workflow-run-crate) profundizan en la procedencia de ejecuciones. Para un caso pequeño, un script versionado, un fichero de dependencias y un registro de comandos pueden resultar más sencillos que adoptar un perfil complejo.

### 4. Calcula integridad fuera de RO-Crate y enlázala

Un RO-Crate no garantiza por sí mismo que sus ficheros no hayan cambiado. Calcula hashes con una herramienta conocida y conserva un manifiesto:

```bash
sha256sum data/*.csv code/*.py results/*.csv > manifest-sha256.txt
sha256sum --check manifest-sha256.txt
```

Ejecuta el comando desde la raíz controlada del paquete y revisa qué rutas entran. Un hash demuestra igualdad de bytes respecto al valor registrado; no demuestra autenticidad, licitud ni veracidad. Si firmas el manifiesto, la firma añade una afirmación sobre su emisor, no sobre los hechos contenidos.

### 5. Describe licencias y exclusiones de forma explícita

Un solo campo `license` en la raíz puede ser engañoso si los componentes tienen condiciones distintas. Documenta por separado la licencia de los metadatos creados por el equipo, la del código, la de cada dataset y cualquier restricción de redistribución.

Incluye una lista de exclusiones sin revelar aquello que pretendes proteger. Por ejemplo: «Se excluyeron campos de contacto no necesarios para el análisis» es útil; publicar el valor excluido en el propio registro anula la protección.

### 6. Valida estructura, contenido y reproducción

La comunidad mantiene una [lista de herramientas RO-Crate](https://www.researchobject.org/ro-crate/tools.html), con editores, bibliotecas y validadores en distintos estados de madurez. Un validador puede comprobar JSON, contexto, tipos, propiedades y requisitos de un perfil. También necesitas controles propios:

- todos los `hasPart` locales existen;
- el manifiesto de hashes verifica;
- no hay secretos, rutas personales ni datos excluidos;
- las licencias declaradas coinciden con las fuentes;
- el proceso se ejecuta en un entorno limpio;
- los totales y registros descartados concuerdan;
- otra persona puede seguir las instrucciones.

Una validación correcta significa «cumple estas reglas», no «sus conclusiones son correctas».

### 7. Congela una edición y conserva su identidad

Antes de distribuir, asigna una versión al paquete y evita reemplazar silenciosamente el contenido. Si corriges algo, publica una nueva edición y explica el cambio. Para preservación o intercambio puedes usar un ZIP u otra convención apropiada, pero RO-Crate no obliga de forma general a comprimir la carpeta. Algunos perfiles sí fijan su empaquetado.

## Limitaciones y falsos positivos

RO-Crate resuelve un problema de descripción, no todos los problemas probatorios:

- **Metadatos falsos o incompletos**: cualquiera puede escribir una fecha, autoría o licencia incorrecta.
- **Enlaces vivos**: una URI externa puede desaparecer o devolver contenido distinto.
- **Granularidad desigual**: describir el conjunto no documenta automáticamente cada fila ni cada decisión.
- **Relación no causal**: enlazar una salida con un script no demuestra que esa ejecución concreta la produjo.
- **Identidad ambigua**: dos nombres parecidos siguen sin ser la misma entidad aunque compartan un nodo.
- **Validación limitada**: pasar un esquema o perfil no verifica hashes, interpretación ni cobertura salvo que el control lo exija expresamente.
- **Sobrecoste**: para tres ficheros simples, una estructura clara, hashes y un README pueden bastar.

El mayor falso positivo sería confundir un paquete elegante con una investigación sólida. Un crate impecable puede documentar un muestreo sesgado, una unión incorrecta o una fuente poco fiable con extraordinaria precisión.

## Buenas prácticas de OPSEC, ética y privacidad

- Publica el mínimo necesario para sostener la conclusión y permitir una revisión proporcionada.
- Mantén el paquete público separado del expediente interno desde el inicio, con permisos distintos.
- No incluyas cookies, tokens, historial del navegador, nombres de usuario locales ni rutas absolutas.
- Revisa el historial de Git y los metadatos incrustados; borrar un fichero del último commit no lo elimina del pasado.
- Usa entidades organizativas o seudónimos cuando identificar a una fuente o analista cree riesgo y exista una razón legítima.
- No describas como `author` a quien solo apareció mencionado en una fuente.
- Conserva las condiciones de acceso y evita automatizaciones agresivas al adquirir material.
- Establece retención y borrado para el expediente interno; «por si acaso» no es una finalidad.
- Trata acusaciones, coincidencias y relaciones inferidas como afirmaciones que necesitan evidencia independiente.
- Documenta qué no sabes y qué no puede reproducir una persona externa por motivos legales o de seguridad.

## Lista de control antes de publicar

- [ ] La pregunta, el alcance y la audiencia están escritos.
- [ ] Cada fichero está clasificado como original, derivado, resultado, contexto o excluido.
- [ ] `ro-crate-metadata.json` apunta a la versión correcta de la especificación.
- [ ] Las rutas locales descritas existen y no escapan de la raíz del paquete.
- [ ] URL, UTC, consulta, licencia y método constan para cada adquisición.
- [ ] El manifiesto SHA-256 verifica desde una copia limpia.
- [ ] Código, dependencias y comandos permiten repetir la transformación.
- [ ] Las licencias se declaran con la granularidad necesaria.
- [ ] No hay secretos, datos personales innecesarios ni información sobre fuentes protegidas.
- [ ] Un validador apropiado comprueba el crate y su perfil, si lo usa.
- [ ] Una revisión independiente contrasta resultados y limitaciones.
- [ ] La versión publicada es inmutable y las correcciones crearán una nueva edición.

## Alternativas y siguientes pasos

RO-Crate no siempre es la mejor primera herramienta. Un `README`, un manifiesto de hashes y una estructura coherente pueden resolver un caso pequeño. [BagIt](https://www.rfc-editor.org/rfc/rfc8493) se centra en empaquetado y verificación de cargas mediante manifiestos; [Frictionless Data Package](https://specs.frictionlessdata.io/data-package/) describe colecciones de recursos de datos, especialmente tabulares; WARC resulta apropiado para preservar respuestas web. Estas opciones pueden complementarse, pero combinarlas sin una necesidad concreta añade complejidad.

Si el caso exige registrar ejecuciones de forma detallada, estudia un perfil existente antes de inventar uno. La documentación de perfiles recomienda reutilizar convenciones ya publicadas para que productores y consumidores compartan expectativas.

El takeaway accionable: toma una investigación cerrada, crea una carpeta pública nueva y mete solo lo imprescindible. Añade `README`, licencias, hashes y un `ro-crate-metadata.json` mínimo. Después entrégasela a alguien que no participó en el caso y anota cada pregunta que no pueda responder. Esas preguntas son la mejor prueba de calidad del paquete.

Como siguiente tema, convendría comparar RO-Crate, BagIt y Frictionless Data Package sobre el mismo conjunto ficticio: descripción, integridad y estructura tabular son problemas relacionados, pero no idénticos.

## Fuentes consultadas

- [RO-Crate Metadata Specification 1.3](https://www.researchobject.org/ro-crate/specification/1.3/)
- [RO-Crate: entidades de datos](https://www.researchobject.org/ro-crate/specification/1.3/data-entities.html)
- [RO-Crate: entidades contextuales](https://www.researchobject.org/ro-crate/specification/1.3/contextual-entities.html)
- [RO-Crate: perfiles](https://www.researchobject.org/ro-crate/profiles.html)
- [RO-Crate: herramientas y recursos](https://www.researchobject.org/ro-crate/tools.html)
- [Repositorio oficial de la especificación RO-Crate](https://github.com/ResearchObject/ro-crate)
- [RFC 8493: The BagIt File Packaging Format](https://www.rfc-editor.org/rfc/rfc8493)
