---
title: "Pruebas metamórficas en OSINT: comprobar invariantes cuando no conocemos la respuesta"
slug: /pruebas-metamorficas-osint-invariantes
authors: [osint-writter]
tags: [osint, methodology, data, verification, automation, privacy]
date: 2026-09-23
image: /img/blog/2026-09-23-pruebas-metamorficas-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista comparando dos transformaciones relacionadas de un conjunto de datos público](/img/blog/2026-09-23-pruebas-metamorficas-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/pruebas-metamorficas-osint-invariantes.m4a)


*Imagen generada mediante inteligencia artificial.*

Una canalización suma contratos públicos por proveedor y devuelve 12,4 millones de euros. No disponemos de una segunda contabilidad perfecta con la que comparar cada fila, pero sí sabemos algo más modesto: **ordenar el fichero de otra manera no debería cambiar el total, y dividir cada importe en dos fracciones equivalentes tampoco**. Si alguna de esas transformaciones altera el resultado, hemos encontrado un error útil sin necesitar conocer de antemano la cifra correcta.

Las pruebas metamórficas convierten esas relaciones necesarias en controles repetibles. En OSINT resultan valiosas cuando el resultado exacto es caro o imposible de calcular manualmente, pero podemos describir cómo debería comportarse ante cambios controlados. No prueban que la fuente diga la verdad ni que nuestra lista de invariantes sea completa; ayudan a descubrir contradicciones dentro del proceso analítico.

<!-- truncate -->

## Qué son y para qué sirven

En una prueba convencional proporcionamos una entrada y comparamos la salida con un resultado esperado. Esto se complica cuando analizamos miles de registros, aplicamos varias transformaciones o usamos un algoritmo cuya respuesta correcta no está disponible de antemano. Es el llamado **problema del oráculo**: ejecutar el programa es fácil; decidir automáticamente si acertó puede no serlo.

La [propuesta original de Chen, Cheung y Yiu](https://www.cse.ust.hk/faculty/scc/publ/CS98-01-metamorphictesting.pdf) planteó aprovechar ejecuciones que no revelaban fallos para derivar nuevos casos. La pieza central es una **relación metamórfica**: una propiedad necesaria que conecta varias entradas relacionadas con sus salidas. Una [revisión posterior de la literatura](https://i.cs.hku.hk/~tse/Papers/2010s/hlmtCSUR.html) describe la técnica como un enfoque tanto para generar casos de prueba como para verificar resultados.

El patrón mínimo tiene cinco movimientos:

1. elegir una entrada base;
2. ejecutar la transformación o análisis y conservar su salida;
3. modificar la entrada de una forma deliberada y documentada;
4. ejecutar exactamente el mismo proceso sobre la entrada derivada;
5. comprobar la relación esperada entre ambas salidas.

No siempre esperamos igualdad. Si multiplicamos todos los importes válidos por diez, el agregado debería multiplicarse por diez. Si añadimos un expediente fuera del intervalo temporal consultado, el resultado filtrado debería permanecer igual. Si partimos una fila de 100 euros en dos de 40 y 60 conservando la misma clave lógica, el total debería mantenerse, aunque el número de filas cambie.

## Caso legítimo: contratos de Villa Serena

Imaginemos una investigación ficticia sobre la evolución trimestral de contratos de mantenimiento en **Villa Serena**. El portal abierto publica un CSV con estas columnas:

- `expediente_id`;
- `lote_id`;
- `fecha_adjudicacion`;
- `proveedor_id`;
- `importe_eur`;
- `estado`.

La pregunta es institucional y agregada: cuánto importe neto fue adjudicado por trimestre y procedimiento. No se pretende perfilar a personas. El equipo conserva la descarga original, registra URL y hora UTC, calcula un hash y trabaja sobre una copia minimizada.

El resultado del pipeline no tiene un «libro de respuestas» completo. Sí permite proponer relaciones candidatas:

| Transformación controlada | Relación esperada | Error que podría revelar |
| --- | --- | --- |
| Reordenar filas | mismos agregados y claves | dependencia accidental del orden |
| Duplicar el fichero completo | importes y recuentos se duplican exactamente | deduplicación oculta o agregación incoherente |
| Añadir una fila fuera del periodo | resultado del periodo sin cambios | filtro temporal incorrecto |
| Partir un importe en dos movimientos equivalentes | mismo importe neto | granularidad o `join` defectuoso |
| Cambiar solo espacios y mayúsculas en categorías normalizables | mismas categorías canónicas | normalización incompleta |
| Multiplicar todos los importes por un factor positivo | total multiplicado por ese factor | redondeo, conversión o filtrado inesperado |

La tabla es un punto de partida, no un catálogo universal. Duplicar filas **no** debe duplicar un resultado si el contrato funcional del pipeline incluye deduplicación por identificador. Cambiar mayúsculas solo debería ser invariante si la fuente declara que la categoría no distingue caja. La relación correcta depende de la semántica documentada.

## Flujo recomendado

### 1. Fija la unidad de análisis

Antes de automatizar, escribe una frase como: «una fila analítica representa un expediente, lote y movimiento». Después declara qué salida se compara: total, conjunto de claves, distribución por trimestre o tabla completa ordenada de forma canónica.

Sin esa decisión, una prueba puede pasar mientras compara entidades distintas. Un recuento estable no compensa un importe atribuido al proveedor equivocado.

### 2. Preserva una entrada base pequeña

Conserva el original adquirido y crea un fixture minimizado con datos sintéticos o anonimizados. Registra:

- origen y momento de adquisición;
- hash del original y del fixture;
- versión del código y dependencias;
- esquema y tipos esperados;
- supuestos que justifican cada relación.

El fixture debe contener límites relevantes: cero, decimales, abonos, lotes múltiples, fechas en el borde del periodo y categorías desconocidas. No copies datos personales al repositorio para hacer una prueba que puede expresarse con identificadores ficticios.

### 3. Formula la relación antes de mirar el resultado

Una relación útil separa tres piezas:

```text
precondición -> transformación de entrada -> relación entre salidas
```

Ejemplo: «si todos los importes son valores decimales no nulos y los multiplicamos por 10, entonces el total neto debe ser diez veces el original». La precondición evita aplicar la regla a símbolos de moneda, ausencias o valores que el pipeline descarta deliberadamente.

Escribir la relación después de observar una discrepancia facilita racionalizar el comportamiento actual. Trátala como una especificación revisable, no como una explicación improvisada.

### 4. Genera una entrada derivada sin tocar el original

Cada transformación debe crear un artefacto nuevo. Así se puede inspeccionar el par base/derivado y repetir el fallo. Guarda una descripción legible de la mutación y, si el volumen lo permite, un diff.

Un ejemplo mínimo en Python, con datos totalmente ficticios, puede comprobar la independencia del orden:

```python
from decimal import Decimal
from random import Random


def importe_neto(filas):
    return sum(
        (Decimal(fila["importe_eur"]) for fila in filas
         if fila["estado"] == "ADJUDICADO"),
        start=Decimal("0"),
    )


base = [
    {"id": "EXP-001", "estado": "ADJUDICADO", "importe_eur": "120.50"},
    {"id": "EXP-002", "estado": "ANULADO", "importe_eur": "90.00"},
    {"id": "EXP-003", "estado": "ADJUDICADO", "importe_eur": "40.25"},
]

derivada = base.copy()
Random(20260923).shuffle(derivada)

assert importe_neto(derivada) == importe_neto(base)
```

La semilla facilita reproducir ese orden concreto, pero una sola permutación ofrece cobertura limitada. Una biblioteca de pruebas basadas en propiedades puede explorar más casos. La [documentación oficial de Hypothesis](https://hypothesis.readthedocs.io/en/latest/) explica cómo describir dominios de entrada, generar ejemplos y reducir un fallo a un caso más sencillo. La biblioteca automatiza la exploración; no decide qué relación tiene sentido para la investigación.

### 5. Compara artefactos canónicos

Dos salidas equivalentes pueden diferir en el orden de filas, la representación de fechas o metadatos volátiles. Antes de comparar:

- ordena por claves declaradas;
- normaliza zonas horarias solo con una regla explícita;
- usa aritmética decimal para importes;
- excluye marcas de ejecución si no forman parte del resultado;
- conserva por separado la salida cruda y la canónica.

No normalices hasta borrar el síntoma que querías detectar. Si el orden tiene significado en una cronología, ordenarlo antes de comparar podría ocultar el fallo.

### 6. Triangula cada incumplimiento

Una violación demuestra que el programa y la relación declarada no pueden ser correctos a la vez bajo esas precondiciones. Todavía hay que determinar cuál falla:

1. conserva entrada base, entrada derivada y ambas salidas;
2. reduce el caso sin modificar el original;
3. revisa la definición de la relación y sus precondiciones;
4. localiza la primera etapa donde divergen los resultados;
5. contrasta las filas afectadas con el documento o portal primario;
6. corrige código o especificación mediante un cambio trazable;
7. incorpora el caso mínimo como prueba de regresión.

Una anomalía técnica es una pista sobre el pipeline, no una acusación contra quien publicó los datos.

## Relaciones útiles por capa

### Adquisición

Repetir una petición paginada con el mismo snapshot o identificador de versión debería recuperar el mismo conjunto, si la API ofrece esa garantía. Si la fuente es viva y no proporciona snapshot, la igualdad deja de ser una relación válida: una diferencia puede ser una actualización legítima.

### Normalización

Aplicar dos veces una normalización idempotente debería producir lo mismo que aplicarla una vez. También puede comprobarse que una transformación reversible —por ejemplo, serializar y leer un formato bajo un contrato definido— preserve campos y tipos relevantes.

### Uniones y agregados

Dividir un grupo en particiones disjuntas, agregar cada una y recombinar debería coincidir con agregar el conjunto completo cuando la operación lo permita. Esta relación puede descubrir pérdidas, duplicados o filtros distintos entre lotes.

### Resolución de entidades

Aquí conviene ser especialmente prudente. Añadir una variante ortográfica no debe obligatoriamente mantener el mismo número de entidades: podría ser otra organización real. Es más seguro probar propiedades mecánicas del proceso —estabilidad ante reordenación, conservación de identificadores fijados o simetría de una función de similitud— y revisar manualmente las decisiones de fusión.

## Limitaciones y falsos positivos

### La relación puede estar equivocada

Ordenar filas solo es inocuo si no representan eventos cuya secuencia afecta al estado. Multiplicar valores puede cruzar umbrales de redondeo o desbordamiento. Añadir un duplicado puede activar una deduplicación prevista. Toda relación necesita alcance y precondiciones.

### Varias implementaciones pueden compartir el mismo error

Comparar dos rutas de cálculo aporta información, pero no independencia si ambas usan la misma tabla ya dañada o la misma función defectuosa. Conserva procedencia por etapa y contrasta con una fuente primaria cuando la conclusión sea importante.

### Pasar pruebas no demuestra completitud

El pipeline puede respetar todas las relaciones elegidas y seguir omitiendo un mes completo, interpretando mal una categoría o partiendo de una fuente falsa pero coherente. Las pruebas cubren propiedades concretas, no «la verdad» en general.

### El azar puede complicar la reproducción

Registra semillas, entradas reducidas, versiones y configuración. Aun así, no conviertas una semilla fija en el único caso: la exploración debe ser amplia y los fallos deben quedar convertidos en regresiones deterministas.

### El coste puede crecer deprisa

Cada relación añade ejecuciones. Prioriza invariantes ligados a errores con impacto real, usa fixtures pequeños para la mayoría de pruebas y reserva conjuntos grandes para controles programados.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja únicamente con fuentes abiertas o accesos autorizados.
- Minimiza y seudonimiza los fixtures antes de compartirlos.
- No generes mutaciones que disparen acciones contra servicios reales.
- Ejecuta transformaciones sobre copias locales, no enviando datos sensibles a terceros.
- Revisa logs, informes de fallo y artefactos de CI: pueden reproducir filas completas.
- Separa observación, transformación, resultado e inferencia en las notas.
- Documenta por qué una relación debería cumplirse y quién la revisó.
- Trata el incumplimiento como un defecto o supuesto a investigar, no como evidencia automática de manipulación.
- Conserva originales inmutables y aplica retención limitada a derivados con datos personales.

## Lista de control

- [ ] La entrada base tiene procedencia, UTC y hash.
- [ ] La unidad de análisis y el resultado comparable están definidos.
- [ ] Cada relación incluye precondición, mutación y relación de salida.
- [ ] Los fixtures usan datos ficticios o minimizados.
- [ ] La transformación derivada nunca sobrescribe el original.
- [ ] La comparación canónica no elimina señales relevantes.
- [ ] Semillas, versiones y configuración quedan registradas.
- [ ] Un fallo conserva las cuatro piezas: dos entradas y dos salidas.
- [ ] Las relaciones críticas incluyen casos positivos y negativos.
- [ ] Las conclusiones importantes se corroboran fuera del pipeline.
- [ ] Un resultado verde se presenta como conformidad parcial, no como verdad factual.

## Alternativas y siguientes pasos

Los `unit tests` son preferibles cuando conocemos una salida exacta para un caso pequeño. Las pruebas basadas en propiedades exploran muchos valores de un dominio y encajan bien para expresar relaciones metamórficas; Hypothesis es una opción en Python. [dbt](/dbt-osint-pruebas-transformaciones) integra pruebas alrededor de modelos SQL. [Soda Core](/soda-core-osint-contratos-datos-deriva-esquema) comprueba contratos y calidad de una fuente consultable. [Frictionless Data Package](/frictionless-data-package-osint-validacion-tabular) describe la estructura de paquetes tabulares.

También existen frameworks especializados. El repositorio de [GeMTest](https://github.com/tum-i4/gemtest) muestra una integración con `pytest` basada en transformaciones y relaciones. Antes de añadir una dependencia, prueba la idea con una función pequeña y una relación cuya justificación pueda entender otra persona.

El takeaway accionable: elige hoy una transformación crítica de tu investigación y formula dos relaciones. Primero, reordena la entrada y exige estabilidad donde el orden no tenga significado. Después, divide una cantidad en partes equivalentes y exige que el agregado se conserve. Guarda entradas y salidas. Si una relación falla, investiga el supuesto antes de corregir el síntoma.

Como siguiente tema, merece la pena estudiar **pruebas diferenciales en OSINT**: comparar dos implementaciones independientes sin confundir acuerdo entre herramientas con verdad factual.

## Fuentes consultadas

- [Metamorphic Testing: A New Approach for Generating Next Test Cases (informe técnico original, 1998)](https://www.cse.ust.hk/faculty/scc/publ/CS98-01-metamorphictesting.pdf)
- [Metamorphic Testing: A Review of Challenges and Opportunities (ACM Computing Surveys)](https://i.cs.hku.hk/~tse/Papers/2010s/hlmtCSUR.html)
- [Documentación oficial de Hypothesis](https://hypothesis.readthedocs.io/en/latest/)
- [Repositorio oficial de GeMTest](https://github.com/tum-i4/gemtest)
