---
title: "Mutation testing en OSINT: sembrar fallos para saber si tus pruebas vigilan de verdad"
slug: /mutation-testing-pipelines-osint
authors: [osint-writter]
tags: [osint, methodology, verification, data, automation, privacy]
date: 2026-09-25
image: /img/blog/2026-09-25-mutation-testing-pipelines-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista examinando mutaciones controladas en un pipeline de datos públicos](/img/blog/2026-09-25-mutation-testing-pipelines-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/mutation-testing-pipelines-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

Un pipeline de contratación pública supera 186 pruebas y produce el informe esperado. Después alguien cambia por accidente `importe > 10000` por `importe >= 10000`: las pruebas siguen verdes, pero ahora la tabla incluye expedientes que antes quedaban fuera. **Tener pruebas no significa que esas pruebas sean capaces de detectar los fallos que más importan.**

El *mutation testing* —pruebas de mutación— introduce pequeños cambios deliberados en el código y vuelve a ejecutar la batería de tests. Si un test falla, el mutante ha sido «matado». Si todo continúa verde, el mutante sobrevive y señala una posible carencia: quizá no alcanzamos esa rama, quizá no comprobamos la salida adecuada o quizá el cambio no altera el comportamiento observable.

En OSINT esta técnica sirve para evaluar los controles de parsers, normalizadores y agregaciones sin manipular fuentes reales. No demuestra que un dato público sea verdadero, que la adquisición esté completa ni que una conclusión sea correcta. Comprueba algo más acotado: si nuestras pruebas reaccionan ante ciertos errores artificiales del software.

<!-- truncate -->

## Qué es y para qué sirve

Una prueba convencional pregunta: «¿el programa produce el resultado esperado para este caso?». Una prueba de mutación añade otra pregunta: «¿esta batería detectaría que el programa ha cambiado de una forma peligrosa?».

El proceso conceptual es:

```text
código original + tests verdes
            │
            ├── mutante A: > cambia a >= ──> falla un test ──> matado
            ├── mutante B: elimina un filtro ─> tests verdes ─> sobrevive
            └── mutante C: True cambia a False > falla un test ─> matado
```

La idea tiene una larga historia. DeMillo, Lipton y Sayward describieron en 1978 el uso de variaciones incorrectas de un programa y el llamado **efecto de acoplamiento**: los datos de prueba capaces de distinguir errores simples pueden ayudar también a revelar errores más complejos. Es una hipótesis práctica, no una garantía de que un conjunto de mutantes represente todos los defectos posibles.

Las herramientas actuales automatizan parte del trabajo. [mutmut](https://mutmut.readthedocs.io/en/latest/) está orientado a Python y puede ejecutar las pruebas, conservar resultados y permitir inspeccionar los mutantes. [Stryker](https://stryker-mutator.io/docs/) ofrece implementaciones para varios ecosistemas y clasifica sus resultados. [PIT](https://pitest.org/quickstart/basic_concepts/) aplica mutaciones al *bytecode* de Java y dispone de operadores configurables. La herramienta cambia; el razonamiento no: un superviviente es una pregunta para el equipo, no una sentencia automática.

## Caso legítimo: el umbral de Villa Serena

Imaginemos que el ayuntamiento ficticio de **Villa Serena** publica adjudicaciones en CSV. El objetivo legítimo es elaborar una serie mensual agregada de contratos de mantenimiento, sin perfilar a empleados ni proveedores individuales. El pipeline:

1. lee una copia fijada por hash;
2. valida columnas y tipos;
3. conserva expedientes con estado `adjudicado`;
4. normaliza importes y fechas;
5. deduplica por `expediente_id` y `lote_id`;
6. agrupa por mes y procedimiento;
7. exporta una tabla agregada junto con su procedencia.

Una función simplificada podría contener esta regla ficticia:

```python
def entra_en_muestra(expediente):
    return (
        expediente.estado == "adjudicado"
        and expediente.importe_eur > 10_000
        and expediente.fecha_adjudicacion is not None
    )
```

La cobertura de líneas puede confirmar que el test ejecutó la comparación del importe. Sin embargo, no prueba que exista un caso exactamente igual a 10.000 euros ni que se compruebe su exclusión. Un mutador que sustituya `>` por `>=` convierte esa laguna en una señal visible: si el mutante sobrevive, falta una aserción de frontera o el requisito no está bien definido.

Otros mutantes relevantes para este ejemplo serían:

| Cambio controlado | Riesgo que simula | Prueba que debería detectarlo |
| --- | --- | --- |
| `>` pasa a `>=` | frontera mal interpretada | casos de 9.999,99; 10.000 y 10.000,01 euros |
| igualdad pasa a desigualdad | filtro de estado invertido | mezcla mínima de estados admitidos y excluidos |
| se elimina la deduplicación | doble recuento | dos filas iguales y dos lotes legítimamente distintos |
| suma pasa a resta | agregado corrupto | total manual sobre un fixture pequeño |
| condición vacía pasa a verdadera | fecha ausente aceptada | registro sin fecha y política explícita de descarte |

Los ejemplos usan datos inventados. No hace falta introducir fallos en una copia de producción ni enviar expedientes reales a un servicio externo.

## Flujo recomendado

### 1. Define primero el contrato

Antes de mutar nada, escribe qué debe permanecer cierto: unidad de análisis, campos obligatorios, tratamiento de nulos, zona horaria, criterio de inclusión, deduplicación y reglas de redondeo. Si el significado de `10.000` no está acordado, matar el mutante de frontera solo consolidará una decisión accidental.

Prepara un *fixture* mínimo con identificadores ficticios y salidas exactas conocidas. Incluye fronteras, ausencias, duplicados y una fila que deba quedar fuera. Mantén por separado una prueba de integración con una adquisición pública preservada cuando sea legal y necesario.

### 2. Comprueba una línea base limpia

Ejecuta todos los tests sobre el código sin modificar. Deben pasar de forma determinista. Registra el commit, el entorno y la duración. Una prueba intermitente puede «matar» mutantes por ruido y generar una falsa sensación de vigilancia.

```text
commit:       identificador fijado
entrada:      fixture sintético versionado
resultado:    tests verdes
duración:     referencia para detectar timeouts anómalos
```

### 3. Acota el objetivo

Empieza por el código que transforma evidencia: filtros, conversión de unidades, parsing de fechas, claves de unión, deduplicación y agregados. Excluye código generado, adaptadores triviales y registros de depuración si no aportan comportamiento verificable.

En Python, la documentación de mutmut propone una puesta en marcha mínima con `pip install mutmut` y `mutmut run`. No ejecutes a ciegas sobre todo el repositorio: revisa primero qué rutas se mutarán, que los tests no tengan red y que los artefactos temporales no puedan sobrescribir adquisiciones.

### 4. Ejecuta cada mutante en aislamiento

La herramienta debe aplicar un cambio controlado, ejecutar los tests pertinentes y restaurar el código. Hazlo en una rama o entorno efímero, con escritura limitada y sin credenciales. Nunca despliegues mutantes ni los mezcles con el commit que produce el informe.

Los estados varían entre herramientas. La [clasificación de Stryker](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/) distingue, entre otros, mutantes matados, supervivientes, sin cobertura, inválidos y con *timeout*. Conviene conservar esos matices en vez de reducir todo a un único porcentaje.

### 5. Investiga supervivientes por riesgo

Ordena los supervivientes por impacto en la pregunta investigable:

1. cambios que alteran inclusión, exclusión o identidad de registros;
2. cambios en importes, unidades, tiempo o agregación;
3. cambios que afectan a la procedencia o al registro de errores;
4. cambios cosméticos o de bajo impacto.

Para cada uno, decide una de estas salidas documentadas:

- añadir una prueba que falle por la razón correcta;
- aclarar el requisito antes de escribir el test;
- marcarlo como mutante equivalente con una justificación revisable;
- excluir una zona sin valor analítico y explicar el alcance;
- aceptar el riesgo de manera explícita.

### 6. Repite sobre cambios relevantes

No es necesario mutar cada línea en cada commit. Una estrategia razonable es ejecutar un conjunto acotado en las transformaciones modificadas y reservar una campaña más amplia para revisiones periódicas. El coste computacional y la duración son límites reales; [PIT](https://pitest.org/quickstart/mutators/) agrupa operadores y selecciona por defecto mutadores diseñados para ser estables y reducir mutaciones equivalentes.

## Cómo leer el resultado sin convertirlo en un fetiche

Un cálculo habitual es:

```text
mutation score = mutantes detectados / mutantes válidos × 100
```

Stryker documenta esta métrica y también una variante sobre código cubierto. Es útil para observar una tendencia con el mismo alcance y configuración. No permite comparar limpiamente proyectos con lenguajes, operadores, exclusiones o arquitecturas diferentes.

Un 92 % no significa que el pipeline tenga un 92 % de probabilidades de ser correcto. Tampoco garantiza que los datos sean auténticos, completos o actuales. El score puede subir añadiendo tests superficiales contra mutantes fáciles mientras sobrevive una inversión crítica del filtro temporal.

El informe útil conserva al menos:

- operador y ubicación del cambio;
- estado final y test que lo detectó;
- alcance de código incluido y excluido;
- mutantes equivalentes justificados;
- timeouts y errores de compilación por separado;
- relación del superviviente con un riesgo investigativo concreto.

## Limitaciones y falsos positivos

### Mutantes equivalentes

Algunos cambios sintácticos no modifican el comportamiento posible. Si una cantidad ya ha sido validada como estrictamente positiva, cambiar `x >= 0` por `x > 0` en una rama posterior puede ser indistinguible. Ningún test puede matar un mutante realmente equivalente; perseguirlo consume tiempo y distorsiona el score.

### Operadores poco representativos

Las herramientas suelen cambiar comparadores, booleanos, retornos u operaciones aritméticas. Un fallo real de OSINT puede estar en otro lugar: una página no descargada, una licencia mal entendida, una columna cuyo significado cambió o dos entidades homónimas fusionadas. La mutación del programa no modela por sí sola esos riesgos.

### Tests que fallan por la razón equivocada

Un mutante puede aparecer como matado porque expiró una llamada de red, cambió la hora local o falló un servicio externo. Ese resultado no acredita una buena aserción. Los tests de mutación deben ser locales, deterministas y capaces de mostrar qué salida cambió.

### Coste y sesgo de selección

Ejecutar muchos mutantes puede resultar caro. Acotar el código acelera la campaña, pero también decide qué fallos quedan invisibles. Documenta esa selección y evita presentar un score parcial como evaluación de todo el pipeline.

### No prueba la fuente ni la hipótesis

Matar un mutante que duplica importes demuestra que un test detectó esa alteración. No demuestra que el CSV municipal contenga todos los expedientes, que el campo represente el valor que suponemos ni que exista una irregularidad. La corroboración vuelve siempre a documentación, fuente primaria y contexto.

## Buenas prácticas de OPSEC, ética y privacidad

- Muta código en una copia aislada; nunca datos originales ni sistemas de terceros.
- Usa fixtures sintéticos o minimizados para comprobar reglas delicadas.
- Bloquea red y credenciales durante la ejecución cuando el pipeline no las necesite.
- Monta adquisiciones preservadas como solo lectura.
- Impide que un mutante publique, envíe alertas o sobrescriba resultados canónicos.
- No vuelques filas con datos personales en informes HTML o logs de CI.
- Define límites de CPU, memoria y tiempo para mutantes que creen bucles.
- Separa fallo simulado, observación técnica e inferencia factual.
- Prioriza riesgos institucionales y agregados; evita convertir la técnica en perfilado de personas.
- Exige revisión humana antes de publicar una conclusión sensible.

## Lista de control

- [ ] La pregunta investigable y la unidad de análisis están escritas.
- [ ] El baseline pasa con fixtures deterministas.
- [ ] Originales y adquisiciones están fijados y en solo lectura.
- [ ] Las mutaciones se limitan al código de transformación pertinente.
- [ ] La ejecución no dispone de credenciales ni efectos externos.
- [ ] Hay casos de frontera, nulos, duplicados y exclusión.
- [ ] Cada superviviente se prioriza por impacto, no por orden de aparición.
- [ ] Los mutantes equivalentes llevan una justificación concreta.
- [ ] Timeouts, falta de cobertura y errores se informan por separado.
- [ ] El score no se presenta como probabilidad de verdad.
- [ ] Los hallazgos regresan a la fuente y a corroboración independiente.

## Alternativas y siguientes pasos

Las [pruebas diferenciales](/pruebas-diferenciales-osint-pipelines) comparan implementaciones; las [pruebas metamórficas](/pruebas-metamorficas-osint-invariantes) relacionan ejecuciones cuyas salidas deben mantener una propiedad; y los tests unitarios con una salida conocida verifican ejemplos concretos. El *mutation testing* no reemplaza esos controles: los somete a una prueba de resistencia.

El takeaway accionable es pequeño: toma hoy una función crítica de filtrado o agregación, crea un fixture ficticio con tres fronteras y cambia manualmente un comparador en una rama desechable. Si ningún test falla, has encontrado una mejora concreta sin tocar una fuente real. Después automatiza solo donde el coste y el riesgo lo justifiquen.

Como siguiente tema, merece la pena estudiar **contract testing entre adquisición y transformación OSINT**: cómo detectar que una fuente cambió su interfaz antes de que el pipeline produzca una tabla aparentemente válida.

## Fuentes consultadas

- [DeMillo, Lipton y Sayward: *Hints on Test Data Selection* (1978)](https://gse.ufsc.br/bezerra/disciplinas/Confiabilidade/docs/demillo-mutants.pdf)
- [mutmut: documentación oficial](https://mutmut.readthedocs.io/en/latest/)
- [Stryker: qué es mutation testing](https://stryker-mutator.io/docs/)
- [Stryker: estados de mutantes y métricas](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/)
- [PIT: conceptos básicos](https://pitest.org/quickstart/basic_concepts/)
- [PIT: operadores de mutación](https://pitest.org/quickstart/mutators/)
