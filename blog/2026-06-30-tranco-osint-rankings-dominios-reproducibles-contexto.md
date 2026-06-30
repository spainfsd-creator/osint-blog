---
title: "Tranco en OSINT: rankings de dominios reproducibles sin convertir popularidad en evidencia"
slug: /tranco-osint-rankings-dominios-reproducibles-contexto
authors: [osint-writter]
tags: [osint, methodology, verification, data, research, investigation]
date: 2026-06-30
image: /img/blog/2026-06-30-tranco-osint-rankings-dominios-reproducibles-contexto.png
---

![Ilustracion editorial de una analista OSINT revisando rankings reproducibles de dominios, tablas anonimas, linea temporal y grafos web sin marcas reales](/img/blog/2026-06-30-tranco-osint-rankings-dominios-reproducibles-contexto.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/tranco-osint-rankings-dominios-reproducibles-contexto.m4a)


En una investigacion web, decir que un dominio es "popular" puede parecer un dato menor. No lo es. Ese ranking puede decidir que muestras analizas, que dominios excluyes como ruido, que infraestructura consideras normal y que conclusiones acabas defendiendo. Si la lista cambia cada dia, no puedes reproducir tu trabajo; si la lista se manipula con facilidad, puedes construir un informe sobre arena.

`Tranco` encaja justo en ese punto: no sirve para descubrir secretos ni para atribuir actores, sino para trabajar con rankings publicos de dominios de forma mas estable, citable y reproducible. Revisando su web y documentacion el **30 de junio de 2026**, el proyecto recomienda usar su lista estandar mas reciente: un millon de dominios obtenidos promediando rankings durante los ultimos 30 dias, con identificadores permanentes, descargas historicas, consulta de ranking por dominio, `API`, paquetes de codigo y acceso mediante `BigQuery`.

Este articulo esta escrito para analistas defensivos, investigadores, periodistas de datos y equipos que necesitan muestrear o contextualizar dominios sin exagerar lo que un ranking puede demostrar. No contiene instrucciones para intrusiones, doxxing, acoso ni automatizacion contra terceros.

<!-- truncate -->

## Que es Tranco y para que sirve

[`Tranco`](https://tranco-list.eu/) es un ranking de sitios web orientado a investigacion. Nacio como respuesta a problemas clasicos de listas de popularidad: volatilidad, poca transparencia, dificultad para citar una version concreta y riesgo de manipulacion. El paper original, publicado en `NDSS 2019`, explicaba que las listas populares usadas en estudios de seguridad y privacidad podian discrepar mucho entre si y alterar resultados si no se controlaban bien.

La idea practica es sencilla: si vas a medir algo sobre la web, necesitas saber exactamente que dominios entraron en la muestra y por que. `Tranco` ayuda a responder preguntas como estas:

- que version concreta de una lista de dominios use;
- si mi muestra es de dominios raiz o incluye subdominios;
- durante que ventana temporal se agrego el ranking;
- como citar la lista para que otro analista pueda repetir el trabajo;
- si un dominio aparece en una posicion aproximada o ha variado con el tiempo;
- que limites metodologicos debo explicar antes de convertir "popular" en "importante".

Para OSINT, el valor no esta en tratar el ranking como verdad absoluta. Esta en usarlo como una capa de contexto cuando necesitas priorizar, muestrear o comparar dominios publicos con trazabilidad.

## Caso de uso legitimo con ejemplo ficticio

Imagina que el equipo de seguridad de `Liria Seguros`, una empresa ficticia, quiere revisar la exposicion de formularios de contacto en webs de su sector. No quiere rastrear personas ni forzar servicios. Quiere construir una muestra defendible de dominios para una revision pasiva y documentada.

Un planteamiento prudente podria ser:

| Decision | Ejemplo ficticio | Por que importa |
| --- | --- | --- |
| Lista base | `Tranco Top 100k` de una fecha concreta | Evita una muestra improvisada |
| Version | ID permanente de la lista | Permite reproducir el estudio |
| Alcance | Dominios raiz, sin subdominios | Reduce ruido y ambiguedad |
| Observacion | Cabeceras, tecnologias visibles, enlaces publicos | Mantiene el flujo pasivo |
| Conclusion | Tendencias agregadas, no acusaciones por dominio | Evita sobreatribuir |

El resultado sano no seria "estos dominios son seguros" ni "estos dominios son sospechosos". Seria algo mas humilde: "en esta muestra reproducible, con esta fecha y estas reglas, observamos estos patrones visibles".

## Flujo recomendado

### 1. Define la pregunta antes de descargar la lista

`Tranco` no arregla una pregunta mal formulada. Antes de tocar datos, escribe que intentas medir:

- prevalencia de una tecnologia visible;
- comparacion de respuestas HTTP entre dominios populares;
- validacion de un conjunto de dominios frente a una referencia estable;
- seleccion de una muestra para revision manual;
- exclusion razonada de dominios muy populares en un flujo de triage.

Si la pregunta es sobre riesgo, propiedad, intencion o impacto, un ranking de popularidad solo aporta contexto. No demuestra ninguna de esas cosas por si solo.

### 2. Elige configuracion y fecha con cuidado

La web de `Tranco` permite recuperar la lista estandar, listas con subdominios, versiones pasadas y listas personalizadas. Su metodologia explica que la configuracion estandar busca mejorar acuerdo y estabilidad agregando rankings durante una ventana temporal y aplicando una regla de puntuacion.

En un informe OSINT, deja por escrito:

- fecha de descarga;
- ID permanente de la lista;
- si incluye subdominios;
- tamano usado: `Top 10k`, `Top 100k`, `Top 1M` u otro corte;
- motivo del corte;
- cualquier filtro adicional aplicado despues.

Ese detalle puede parecer burocratico, pero es lo que separa una muestra defendible de una captura imposible de repetir.

### 3. Usa el ranking como contexto, no como veredicto

Un dominio alto en `Tranco` suele indicar visibilidad o uso amplio, no legitimidad. Un dominio bajo o ausente no implica malicia, irrelevancia ni abandono. La lectura correcta depende de la pregunta:

- para muestreo web, puede ayudarte a evitar sesgos de seleccion;
- para triage defensivo, puede explicar por que un dominio aparece en muchos entornos;
- para investigacion de infraestructura, puede ayudarte a distinguir servicios muy comunes de hallazgos raros;
- para periodismo de datos, puede dar un marco reproducible a una medicion agregada.

Pero no conviene usarlo como whitelist ciega. El propio paper de `Tranco` nacio, en parte, del problema de usar rankings populares sin entender su estabilidad, representatividad y manipulabilidad.

### 4. Documenta cada transformacion

Una lista descargada rara vez se usa tal cual. Normalmente se corta, se cruza, se filtra o se enriquece. Cada transformacion debe quedar registrada:

```text
entrada: Tranco list ID concreto
corte: primeros 100.000 dominios
normalizacion: dominios en minusculas, sin esquema ni ruta
exclusion: dominios internos de prueba y duplicados
enrichment: tecnologia visible mediante fuente pasiva
salida: tabla agregada sin datos personales
```

Si otro analista no puede reconstruir el camino desde la lista original hasta tu tabla final, el ranking ya no aporta reproducibilidad real.

## Limitaciones y falsos positivos

`Tranco` mejora varias debilidades de rankings anteriores, pero no elimina los problemas de interpretacion:

- **Popularidad no es legitimidad**: un dominio muy visitado puede alojar contenido comprometido, abusado o simplemente irrelevante para tu caso.
- **Ausencia no es prueba**: dominios nuevos, regionales, nicho o internos pueden no aparecer aunque sean importantes.
- **El corte importa**: `Top 10k` y `Top 1M` responden preguntas muy distintas.
- **Subdominios cambian el significado**: incluirlos puede ser util para ciertos estudios, pero tambien aumenta ruido y mezcla capas.
- **Los rankings tienen sesgos de fuente**: cualquier agregacion depende de los proveedores y senales disponibles.
- **La estabilidad tiene coste**: suavizar fluctuaciones ayuda a reproducir, pero puede retrasar cambios bruscos de popularidad.

La mejor practica es no presentar `Tranco` como "la web". Presentalo como una muestra concreta, con configuracion, fecha y limites.

## Buenas practicas de OPSEC, etica y privacidad

Trabajar con rankings de dominios no autoriza a rastrear usuarios, perfilar personas ni lanzar escaneos agresivos. Algunas reglas ayudan a mantener el trabajo en una zona responsable:

- usa dominios publicos como unidades de analisis, no personas;
- evita publicar listas de objetivos sensibles si no hay interes publico claro;
- no conviertas un ranking en una lista de ataque;
- respeta `robots.txt`, terminos de uso y limites de consulta cuando hagas mediciones;
- separa muestreo, observacion, inferencia y conclusion;
- anonimiza resultados cuando el analisis agregado sea suficiente;
- conserva el ID de lista, fecha y scripts para auditoria interna.

La disciplina clave es proporcionalidad. Si tu pregunta puede responderse con agregados, no necesitas exponer dominios concretos ni ampliar el tratamiento de datos.

## Alternativas y siguientes pasos

`Tranco` funciona bien cuando necesitas una referencia reproducible de popularidad web. Segun el caso, puede combinarse con:

- `Common Crawl`, si necesitas contenido web historico o corpus amplio;
- `HTTP Archive`, si buscas mediciones tecnicas agregadas de la web;
- `urlscan.io`, para observacion puntual de carga, redirecciones y recursos;
- `BuiltWith` o `Wappalyzer`, si el foco es huella tecnologica visible;
- `Datasette` o `SQLite`, si quieres convertir mediciones en una base consultable;
- notas metodologicas propias, porque ninguna lista sustituye el diseno de investigacion.

El takeaway practico es este: `Tranco` sirve para **hacer mas reproducibles tus muestras de dominios**, no para decidir que es verdad, seguro o malicioso. Si lo citas con fecha, ID, corte y limites, mejora la calidad de tus informes. Si lo usas como oraculo, solo cambia una intuicion fragil por otra con apariencia de tabla.

Como siguiente paso natural del blog, tendria sentido publicar un flujo comparado para construir una muestra web reproducible con `Tranco`, guardar resultados en `SQLite` y documentar cada transformacion sin perder trazabilidad.

## Fuentes consultadas

- [Tranco, pagina principal](https://tranco-list.eu/)
- [Tranco, metodologia](https://tranco-list.eu/methodology)
- [Tranco, paper en arXiv](https://arxiv.org/abs/1806.01156)
- [Tranco, paper NDSS 2019](https://www.ndss-symposium.org/ndss-paper/tranco-a-research-oriented-top-sites-ranking-hardened-against-manipulation/)
- [Repositorio DistriNet/tranco-list](https://github.com/DistriNet/tranco-list)
- [Tranco, PDF del paper](https://tranco-list.eu/assets/tranco-ndss19.pdf)
