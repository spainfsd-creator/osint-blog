---
title: "Historial de MediaWiki en OSINT: reconstruir cambios sin convertir editores en sospechosos"
slug: /mediawiki-historial-revisiones-osint
authors: [osint-writter]
tags: [osint, verification, methodology, tooling, investigation, privacy]
date: 2026-09-13
image: /img/blog/2026-09-13-mediawiki-historial-revisiones-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista comparando revisiones fechadas de una página wiki y documentando su procedencia](/img/blog/2026-09-13-mediawiki-historial-revisiones-osint.png)

*Imagen generada mediante inteligencia artificial.*

Una ficha pública cambia una fecha, pierde un párrafo y gana una referencia nueva. La versión actual parece coherente, pero no responde a las preguntas importantes: **qué cambió exactamente, en qué revisión apareció y qué podía ver el público en ese momento**. Una captura aislada tampoco basta si no podemos conectarla con una versión identificable.

Las instalaciones de [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki), incluida Wikipedia, conservan un historial de revisiones que permite comparar versiones y enlazar una revisión concreta. Para OSINT, ese historial puede convertir un «antes y después» impreciso en una cronología auditable. Pero también invita a un error peligroso: confundir el nombre de una cuenta, una dirección IP histórica o un resumen de edición con la identidad y la intención de una persona.

<!-- truncate -->

## Qué es el historial de MediaWiki y para qué sirve

Cada edición de una página genera una revisión con un identificador, una marca temporal y metadatos asociados. La vista **Ver historial** permite seleccionar dos revisiones y comparar sus diferencias. La [Action API de MediaWiki](https://www.mediawiki.org/wiki/API:Revisions) ofrece esa información de forma estructurada mediante `prop=revisions`; el módulo [`action=compare`](https://www.mediawiki.org/wiki/API:Compare) devuelve la diferencia entre dos revisiones, páginas o textos.

En una investigación legítima, esto resulta útil para:

- fijar cuándo se añadió, corrigió o retiró una afirmación de una página pública;
- distinguir un cambio sustantivo de una corrección tipográfica;
- conservar identificadores estables y enlaces a versiones concretas;
- revisar resúmenes, etiquetas y tamaños como señales de clasificación, nunca como prueba autosuficiente;
- detectar huecos, reversiones y desacuerdos que merecen buscar fuentes primarias.

Una revisión no es una «fotografía completa de internet». Es un estado guardado del contenido de esa wiki. Además, una página renderizada puede incluir plantillas, imágenes o datos transcluidos cuya versión actual no coincida con la que existía cuando se guardó el texto principal.

## Caso de uso legítimo: una fecha que cambia

Imaginemos la página ficticia `Proyecto Faro`, mantenida por una wiki pública sobre patrimonio. El 4 de septiembre indica que la apertura será el día 18; el 7 de septiembre muestra el día 25; el 8 incorpora como referencia una resolución oficial fechada el día 6.

La pregunta prudente no es «¿quién intentó ocultar la fecha?», sino:

1. ¿Qué revisiones contienen cada fecha?
2. ¿Qué diferencia exacta existe entre ellas?
3. ¿Cuándo se guardó cada revisión en UTC?
4. ¿Qué fuente primaria respaldaba cada versión?
5. ¿Hubo una corrección, una reversión o cambios intermedios?

La secuencia puede demostrar que la página cambió. No demuestra por sí sola por qué cambió, quién estaba detrás de una cuenta ni cuál de las fechas era correcta. Para esto último hay que acudir a la resolución, el boletín, la web institucional u otra fuente primaria pertinente.

## Flujo recomendado

### 1. Define la afirmación y el intervalo

Escribe una hipótesis verificable: «Determinar cuándo la página pública sustituyó el día 18 por el 25 entre el 1 y el 10 de septiembre». Registra la URL, el nombre de la wiki, la zona horaria mostrada por la interfaz y el instante de consulta.

No empieces rastreando cuentas. Empieza por el contenido y su procedencia. Así reduces la recogida innecesaria de datos personales y evitas adaptar la pregunta a un editor concreto.

### 2. Revisa el historial en la interfaz

Abre **Ver historial**, identifica las revisiones que acotan el cambio y compara las dos seleccionadas. Conserva, como mínimo:

- identificadores de revisión anterior y posterior;
- marcas temporales normalizadas a UTC;
- título y URL de la página;
- enlace al `diff`;
- resumen de edición literal, si existe;
- fecha y método de adquisición;
- una nota sobre elementos transcluidos o dependencias externas.

El enlace [`Special:PermanentLink/<revision_id>`](https://www.mediawiki.org/wiki/Help:PermanentLink) apunta a una revisión específica. Es mejor referencia que la URL ordinaria de la página, que seguirá mostrando el contenido más reciente.

### 3. Extrae metadatos con la API

Para un análisis repetible, puedes consultar el endpoint `api.php` de la wiki. Este ejemplo usa un título ficticio y solicita metadatos, no el contenido completo:

```bash
curl --get 'https://es.wikipedia.org/w/api.php' \
  --data-urlencode 'action=query' \
  --data-urlencode 'prop=revisions' \
  --data-urlencode 'titles=Proyecto Faro' \
  --data-urlencode 'rvprop=ids|timestamp|user|comment|size|sha1|tags' \
  --data-urlencode 'rvdir=newer' \
  --data-urlencode 'rvlimit=50' \
  --data-urlencode 'format=json' \
  --data-urlencode 'formatversion=2'
```

El resultado puede incluir `revid`, `parentid`, `timestamp`, `user`, `comment`, `size`, `sha1` y etiquetas, según los permisos y la visibilidad de cada campo. Si aparece un objeto `continue`, la respuesta está paginada: conserva sus valores y envíalos en la petición siguiente. No concluyas que has recuperado todo el historial solo porque recibiste una respuesta válida.

El SHA-1 informado corresponde al contenido de la revisión dentro de MediaWiki. Es útil para detectar igualdad o cambios en ese contexto, pero no sustituye el hash de tus propios artefactos descargados ni autentica la veracidad del texto.

### 4. Compara revisiones explícitas

Cuando ya tengas dos identificadores, usa la interfaz o `action=compare` con `fromrev` y `torev`. Guarda los IDs junto al resultado. Pedir simplemente «la versión anterior» o «la siguiente» es más frágil: la propia documentación advierte de comportamientos límite en la primera y última revisión.

Un `diff` es una representación del cambio entre dos estados. Comprueba también las revisiones intermedias: comparar un punto lejano con el actual puede ocultar que una frase se añadió, se retiró y volvió a añadirse con otra referencia.

### 5. Preserva en tres capas

Mantén separados:

1. **respuesta original** de la API o HTML adquirido;
2. **derivado de análisis**, como una tabla normalizada o un `diff` convertido;
3. **nota interpretativa**, donde expliques qué significa y qué no significa el cambio.

Calcula hashes locales de los archivos que conserves, anota las consultas completas y usa nombres con fecha UTC e identificadores de revisión. Si el caso lo justifica, archiva también las fuentes primarias citadas conforme a sus condiciones de uso y a la ley aplicable.

### 6. Corrobora fuera de la wiki

Busca el documento citado, una versión institucional, un registro oficial o una comunicación fechada. Una wiki es una excelente pista y su historial es valioso para estudiar cómo evolucionó una afirmación, pero la corrección factual debe contrastarse con evidencias independientes.

## Cómo leer un `diff` sin sobreactuar

Una línea verde significa contenido añadido y una roja, contenido retirado respecto a la otra revisión. No significa «verdadero» y «falso». Tampoco todos los cambios visibles proceden del texto principal:

- una plantilla puede haber cambiado después;
- una imagen puede tener su propio historial de versiones;
- una página puede transcluir secciones mantenidas en otro título;
- una edición grande puede ser una reorganización sin cambio semántico;
- una reversión puede restaurar contenido sin resolver la disputa subyacente.

Clasifica primero el tipo de cambio: factual, referencial, estructural, estilístico, técnico o de moderación. Después valora su relevancia para la hipótesis. Esta disciplina evita convertir cualquier edición llamativa en una narrativa.

## Limitaciones y falsos positivos

### Historial visible no equivale a historial íntegro

MediaWiki permite ocultar el texto, el resumen o el autor de determinadas revisiones. La API puede devolver indicadores como `texthidden`, `commenthidden` o `userhidden`. Una página eliminada o tareas de mantenimiento de una instalación también pueden afectar a la disponibilidad del historial. Documenta el hueco; no intentes inferir el contenido oculto.

### La marca temporal no explica la causa

El `timestamp` registra cuándo se guardó la revisión. No prueba cuándo ocurrió el hecho descrito ni cuándo el editor lo conoció. Dos ediciones cercanas tampoco demuestran coordinación.

### Una cuenta no es una identidad verificada

Un nombre de usuario puede ser pseudónimo, compartido en un proceso institucional o simplemente no verificable. Las ediciones históricas asociadas a una IP tampoco identifican de forma fiable a una persona: redes corporativas, conexiones móviles, VPN, NAT y direcciones dinámicas rompen esa equivalencia.

En proyectos Wikimedia con cuentas temporales, las ediciones sin sesión iniciada se atribuyen públicamente a un identificador temporal y el acceso a las IP subyacentes está restringido. Esa protección no es un obstáculo que haya que sortear, sino un límite de privacidad que debe respetarse.

### El renderizado histórico puede mezclar tiempos

La [documentación del historial de MediaWiki](https://www.mediawiki.org/wiki/Help:History) señala que el historial del wikitext no siempre coincide con el historial de la página renderizada: plantillas, imágenes, variables temporales o datos enlazados pueden mostrar estados posteriores. Si importa el aspecto exacto, conserva una captura web fechada además del wikitext y describe sus dependencias.

## Buenas prácticas de OPSEC, ética y privacidad

- Limita la recogida al contenido necesario para una finalidad legítima y documentada.
- No cruces cuentas, IP históricas, horarios y otros rastros para desanonimizar a editores.
- No contactes ni señales públicamente a una persona basándote solo en metadatos de edición.
- Usa un agente de usuario identificable, respeta límites de petición y maneja `maxlag` si automatizas consultas a gran escala.
- Conserva resúmenes de edición solo cuando sean relevantes; pueden contener acusaciones o datos personales.
- Separa hechos observados, inferencias y preguntas pendientes en tus notas.
- Si encuentras información sensible expuesta por error, no la amplifiques: sigue los canales de supervisión o retirada del proyecto.

La buena OPSEC aquí no consiste en ocultarse para recolectar más. Consiste en reducir exposición, evitar interacciones innecesarias y mantener una trazabilidad que otra persona pueda auditar.

## Checklist de validación

Antes de citar un cambio, verifica:

- [ ] He identificado la wiki, el título y los dos IDs de revisión.
- [ ] He normalizado las marcas temporales y anotado la zona horaria.
- [ ] He revisado las versiones intermedias y la continuación de la API.
- [ ] He guardado el `diff`, las consultas y los artefactos originales con hashes locales.
- [ ] He comprobado si hay plantillas, imágenes o datos transcluidos.
- [ ] He tratado usuario, resumen y etiquetas como metadatos, no como identidad o intención probadas.
- [ ] He corroborado la afirmación sustantiva con una fuente primaria independiente.
- [ ] He minimizado datos personales y documentado las limitaciones.

## Alternativas y siguientes pasos

- **Interfaz de historial y enlaces permanentes:** suficiente para una revisión puntual y fácil de auditar.
- **MediaWiki Action API:** adecuada para extraer revisiones y comparar IDs de forma estructurada.
- **MediaWiki REST API:** ofrece endpoints más acotados y una estructura uniforme para contenido e historial.
- **Wikimedia XML dumps:** útiles para investigación reproducible a gran escala, con más coste de almacenamiento y procesamiento.
- **Browsertrix/WACZ o archivo web:** complementan el historial cuando necesitas preservar la representación renderizada y sus recursos.
- **Wikimedia Commons `imageinfo`:** permite estudiar el historial específico de un archivo multimedia.

El takeaway accionable es sencillo: la próxima vez que cites que «una wiki cambió», guarda **los dos IDs de revisión, el `diff`, la hora UTC, la consulta y la fuente primaria que confirma el hecho**. El historial demuestra evolución editorial; la corroboración demuestra por qué esa evolución importa.

Como siguiente tema, sería útil aplicar el mismo rigor a los volcados XML de Wikimedia: cómo seleccionar un intervalo, preservar procedencia y analizar cambios a escala sin convertir volumen en certeza.

## Fuentes consultadas

- [MediaWiki Action API: Revisions](https://www.mediawiki.org/wiki/API:Revisions)
- [MediaWiki Action API: Compare](https://www.mediawiki.org/wiki/API:Compare)
- [MediaWiki: continuación de consultas](https://www.mediawiki.org/wiki/API:Continue)
- [MediaWiki: historial de páginas](https://www.mediawiki.org/wiki/Help:History)
- [MediaWiki: enlaces permanentes a revisiones](https://www.mediawiki.org/wiki/Help:PermanentLink)
- [MediaWiki: RevisionDelete](https://www.mediawiki.org/wiki/Manual:RevisionDelete)
- [Wikimedia Foundation: política de acceso a IP de cuentas temporales](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Access_to_Temporary_Account_IP_Addresses_Policy/es)

