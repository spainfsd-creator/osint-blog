---
title: "Property-based testing en OSINT: buscar contraejemplos antes de confiar en el pipeline"
slug: /property-based-testing-pipelines-osint
authors: [osint-writter]
tags: [osint, methodology, verification, data, automation, privacy]
date: 2026-09-28
image: /img/blog/2026-09-28-property-based-testing-pipelines-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista reduciendo un contraejemplo dentro de un pipeline OSINT](/img/blog/2026-09-28-property-based-testing-pipelines-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/property-based-testing-pipelines-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

Una prueba con tres expedientes ficticios pasa. Otra con diez también. En producción aparece una combinación que nadie escribió a mano: dos lotes comparten identificador, uno lleva importe nulo y la misma fecha llega con dos zonas horarias. El pipeline no se rompe; **duplica una cantidad y entrega una tabla perfectamente presentable**.

El *property-based testing* —pruebas basadas en propiedades— cambia la pregunta. En lugar de comprobar solamente unos ejemplos elegidos, describe qué entradas son válidas y qué propiedad debe conservar el sistema. La herramienta genera muchas combinaciones, busca una que contradiga esa propiedad y, cuando la encuentra, intenta reducirla a un contraejemplo pequeño. En OSINT resulta útil para endurecer parsers, normalizadores y agregaciones con datos sintéticos. No demuestra que una fuente sea cierta, completa o representativa.

<!-- truncate -->

## Qué es y para qué sirve

Una prueba tradicional suele fijar entrada y salida: «para estas tres filas, espero este total». Es clara, rápida y muy valiosa como regresión. Su límite es que solo cubre los casos que alguien imaginó.

Una prueba basada en propiedades combina cuatro piezas:

1. **Dominio:** la forma de los datos posibles, incluidas sus restricciones.
2. **Generador o estrategia:** el mecanismo que produce ejemplos de ese dominio.
3. **Propiedad:** una afirmación verificable que debería mantenerse.
4. **Oráculo parcial:** la observación que decide si el caso contradice la propiedad.

[Hypothesis](https://hypothesis.readthedocs.io/en/latest/quickstart.html), una biblioteca para Python, usa estrategias para describir entradas y `@given` para alimentar una prueba con ejemplos generados. Su documentación indica que el valor predeterminado es 100 ejemplos, pero ese número se puede configurar. No hay magia en el cien: una ejecución verde solo informa de los casos explorados y de las propiedades que escribimos.

El antecedente más conocido es QuickCheck. El trabajo de Claessen y Hughes lo presentó como una forma de expresar propiedades ejecutables y probarlas con datos generados. Hoy existen implementaciones en numerosos ecosistemas, como [fast-check](https://fast-check.dev/docs/introduction/why-property-based/) para TypeScript y JavaScript o [jqwik](https://jqwik.net/docs/current/user-guide.html) para Java. La herramienta depende del lenguaje; el método consiste en formular buenas propiedades, generar datos pertinentes y entender los límites del resultado.

### Generar no es tirar valores al azar

Una estrategia útil respeta la estructura del dominio. Para expedientes sintéticos podría generar:

- identificadores con un formato inventado;
- uno o varios lotes por expediente;
- importes decimales dentro de límites explícitos;
- fechas válidas en una ventana ficticia;
- estados de un vocabulario controlado;
- nulos solo donde el contrato los admita;
- duplicados deliberados con una frecuencia visible.

Generar campos independientes y descartar después casi todo puede ocultar problemas: el test emplea tiempo creando entradas imposibles y apenas recorre las combinaciones importantes. Hypothesis permite componer estrategias y crear datos dependientes; por ejemplo, generar primero una fecha inicial y después una fecha final que nunca sea anterior. La distribución de los casos también importa. Si el 99,9 % son expedientes ordinarios, quizá nunca examinemos el borde que motivó la prueba.

### Reducir el fallo

Cuando aparece un caso que falla, muchas herramientas intentan simplificarlo mediante *shrinking*. Un lote de cincuenta filas puede terminar reducido a dos registros, un importe y un identificador duplicado. Ese resultado pequeño suele revelar mejor la regla rota que el dataset original.

Reducido no significa único ni matemáticamente mínimo. El proceso sigue el orden y las decisiones de la herramienta. Conviene conservar el contraejemplo explícito como regresión. La documentación de Hypothesis explica que los fallos se guardan localmente y se vuelven a probar; también recomienda usar `@example` cuando un caso debe ejecutarse siempre, porque la base interna puede cambiar o perder su asociación con el test.

## Caso legítimo: contratos agregados de Villa Serena

Imaginemos un observatorio que resume la contratación del municipio ficticio de **Villa Serena**. Trabaja con un fixture sintético, sin nombres reales ni acceso a un portal durante las pruebas. Cada fila contiene:

```text
expediente_id, lote_id, fecha, estado, importe_eur
VS-1042,        01,      2026-04-30, adjudicado, 1250.00
```

La pregunta técnica es si la función de normalización conserva unidades y evita contar dos veces el mismo lote. El equipo expresa tres propiedades:

- el total nunca cambia al permutar el orden de las filas;
- añadir una copia exacta no cambia el total tras deduplicar;
- normalizar dos veces produce lo mismo que normalizar una vez.

La tercera es una propiedad de idempotencia. La primera se parece a una relación metamórfica. Las etiquetas se solapan porque describen ángulos distintos: aquí lo característico es que un generador explora numerosas tablas válidas y trata de encontrar un contraejemplo.

Un boceto reducido con Hypothesis podría ser:

```python
from decimal import Decimal
from hypothesis import given, strategies as st

fila = st.fixed_dictionaries({
    "expediente_id": st.sampled_from(["VS-1001", "VS-1002"]),
    "lote_id": st.integers(min_value=1, max_value=3),
    "importe_eur": st.decimals(
        min_value=Decimal("0.00"),
        max_value=Decimal("50000.00"),
        places=2,
        allow_nan=False,
        allow_infinity=False,
    ),
})

@given(st.lists(fila, max_size=30))
def test_duplicar_no_altera_total_tras_deduplicar(filas):
    assert total_normalizado(filas + filas) == total_normalizado(filas)
```

El ejemplo no prueba un portal ni descarga datos. Tampoco presupone que deduplicar por esos dos campos sea correcto para un contrato real: esa clave debe justificarse con documentación del dominio. Si el test falla con dos filas idénticas, hemos encontrado una discrepancia entre propiedad e implementación. Aún debemos decidir si el fallo está en el código, en el generador o en una propiedad mal formulada.

## Flujo recomendado paso a paso

### 1. Elige una frontera pequeña

Empieza por una función pura o una transformación aislada: parsear fechas, normalizar importes, deduplicar claves o agrupar filas. Evita comenzar con un proceso que consulta internet, escribe en producción y envía alertas. Cuantos más efectos externos intervengan, más difícil será reproducir el fallo y saber qué observamos.

### 2. Escribe primero el riesgo

Una propiedad merece existir porque protege una decisión. Ejemplos útiles:

- ninguna fila aceptada pierde su referencia al artefacto de origen;
- serializar y volver a leer conserva los campos relevantes;
- dividir un dataset en fragmentos y recombinar resultados da el mismo agregado;
- una entrada inválida se rechaza de forma explícita, no se convierte en cero;
- el orden de descarga no altera un resultado que se define como no ordenado.

«La salida parece razonable» no es una propiedad ejecutable. «El número de claves únicas de salida no supera al de claves únicas de entrada» sí lo es, aunque quizá sea insuficiente por sí sola.

### 3. Modela datos válidos e inválidos por separado

Usa estrategias distintas para casos conformes y para violaciones del contrato. Así puedes exigir que los primeros se procesen y que los segundos se rechacen con un error identificable. Mezclarlos y envolver todo en `try/except` suele convertir defectos en pruebas verdes.

Incluye fronteras deliberadas: lista vacía, un solo elemento, cero, máximos documentados, Unicode, cambios de zona horaria, valores nulos y claves repetidas. No generes datos personales realistas cuando unos identificadores ficticios cumplen la misma función.

### 4. Observa la distribución

Registra cuántos casos contienen duplicados, nulos o fechas límite. Una prueba puede ejecutar miles de ejemplos y no alcanzar la región importante del dominio. Ajusta estrategias antes de aumentar ciegamente el número de ejecuciones.

### 5. Aísla y conserva el contraejemplo

Cuando falle:

1. guarda propiedad, semilla o mecanismo de reproducción, versión del entorno y salida reducida;
2. reproduce el caso sin red y sobre una copia;
3. decide si contradice el contrato real o solo una suposición del test;
4. corrige la causa;
5. añade el caso reducido como ejemplo de regresión legible.

La reproducción es parte del hallazgo. Un fallo que depende de la hora, de una API viva o de un orden no registrado todavía no es una explicación fiable.

### 6. Mantén una batería mixta

Combina propiedades con ejemplos concretos, contract testing, fixtures fijados por hash y revisión manual de salidas. Los tests de ejemplo documentan escenarios conocidos; las propiedades amplían la exploración; los contratos delimitan entradas; la comprobación humana evalúa significado y contexto.

## Propiedades útiles y trampas frecuentes

| Patrón | Pregunta útil en un pipeline OSINT | Trampa |
| --- | --- | --- |
| Idempotencia | ¿Normalizar dos veces equivale a una? | Algunas operaciones son acumulativas por diseño |
| Invariancia al orden | ¿Permutar filas conserva el agregado? | El orden puede ser semántico en una cronología |
| Ida y vuelta | ¿Exportar e importar conserva campos y tipos? | Un formato puede perder precisión legítimamente |
| Conservación | ¿El total antes y después mantiene una magnitud definida? | Deduplicar o filtrar puede cambiarla correctamente |
| Monotonicidad | ¿Añadir un registro válido nunca reduce cierto contador? | Correcciones o estados sustitutivos rompen la premisa |
| Rechazo explícito | ¿Una entrada incompatible queda en cuarentena? | Rechazar todo también hace pasar una propiedad pobre |

Las propiedades demasiado débiles ofrecen una falsa sensación de cobertura. Una función que devuelve siempre una lista vacía satisface «la salida no contiene duplicados». Por eso conviene combinar varias propiedades y ejemplos conocidos.

Las precondiciones excesivas son otra señal de alarma. Si descartamos todos los nulos, duplicados y límites, la prueba describe precisamente la zona cómoda. Es mejor construir directamente datos que cumplan las restricciones necesarias y mantener pruebas separadas para entradas inválidas.

## Limitaciones y falsos positivos

- **La propiedad puede estar equivocada.** Un contraejemplo puede revelar una mala especificación, no un defecto del pipeline.
- **El generador define el horizonte.** Lo que nunca genera tampoco se prueba.
- **Más ejemplos no equivalen a cobertura exhaustiva.** El dominio habitual es demasiado grande.
- **El shrinking simplifica según una heurística.** Puede perder rasgos narrativos del caso original aunque conserve el fallo.
- **La aleatoriedad no sustituye la reproducibilidad.** Hay que guardar el caso reducido y el contexto suficiente.
- **Los efectos externos introducen ruido.** Red, reloj, concurrencia y APIs vivas pueden producir fallos intermitentes.
- **Una propiedad técnica no valida hechos.** Conservar sumas no demuestra que los importes publicados sean correctos ni completos.

También existe un falso positivo editorial: presentar cada contraejemplo como una anomalía de la fuente. En este flujo trabajamos con datos generados para poner a prueba nuestro software. El resultado habla primero de nuestro modelo y nuestra implementación.

## Buenas prácticas de OPSEC, ética y privacidad

- Genera datos sintéticos y evita nombres, teléfonos, correos o direcciones plausibles.
- Ejecuta las pruebas sin credenciales y con la red bloqueada cuando no sea imprescindible.
- Monta adquisiciones reales como solo lectura; nunca las uses como material mutable del generador.
- Impide que una ejecución de test publique artefactos, envíe avisos o modifique el almacén canónico.
- Minimiza logs y contraejemplos: un fallo no justifica copiar expedientes personales al CI.
- Versiona la propiedad, el generador y la decisión de dominio que los sustenta.
- Establece límites de tiempo, memoria y tamaño para evitar casos explosivos.
- Distingue siempre fallo del test, defecto de software, limitación de la fuente e inferencia factual.
- Exige revisión humana antes de convertir una observación técnica en una conclusión pública.

## Lista de control

- [ ] La propiedad protege un riesgo concreto y está escrita en lenguaje de dominio.
- [ ] La frontera probada no tiene efectos externos innecesarios.
- [ ] Los datos generados son sintéticos y cumplen restricciones explícitas.
- [ ] Casos válidos e inválidos se modelan por separado.
- [ ] La distribución incluye vacíos, límites, nulos y duplicados pertinentes.
- [ ] Hay ejemplos fijos para escenarios críticos ya conocidos.
- [ ] El fallo reducido puede reproducirse sin consultar una fuente viva.
- [ ] Cada contraejemplo se clasifica: código, modelo, generador o propiedad.
- [ ] La prueba no puede pasar con una implementación trivial evidentemente inútil.
- [ ] Versiones y entorno quedan registrados cuando afectan a la reproducción.
- [ ] Ningún test dispone de permisos para publicar o sobrescribir originales.
- [ ] Un resultado verde se presenta como exploración acotada, no como verdad factual.

## Alternativas y siguientes pasos

Las [pruebas metamórficas](/pruebas-metamorficas-osint-invariantes) ayudan cuando no conocemos una salida exacta pero sí una relación entre ejecuciones. El [mutation testing](/mutation-testing-pipelines-osint) comprueba si la batería detecta cambios peligrosos; el [contract testing](/contract-testing-osint) vigila la frontera con una fuente; y las [pruebas de caos](/pruebas-caos-pipelines-osint) ensayan fallos operativos en un entorno controlado. El *property-based testing* aporta la exploración automática de muchas entradas y la búsqueda de contraejemplos pequeños.

El takeaway accionable es sencillo: escoge hoy una función de normalización, escribe una propiedad de idempotencia y genera únicamente cinco campos ficticios con límites explícitos. Mira la distribución, conserva el primer contraejemplo reducido y conviértelo en regresión. Si no puedes explicar por qué la propiedad debería cumplirse, todavía no tienes un test: tienes una intuición que conviene documentar.

Como próximo tema, merece la pena estudiar **fuzzing guiado por cobertura en pipelines OSINT**: cómo distinguirlo de las pruebas basadas en propiedades, aislar parsers y tratar cada crash como un fallo técnico, no como una afirmación sobre la fuente.

## Fuentes consultadas

- [Hypothesis: guía de inicio](https://hypothesis.readthedocs.io/en/latest/quickstart.html)
- [Hypothesis: referencia de estrategias](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html)
- [Hypothesis: reproducción de fallos](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)
- [Claessen y Hughes: *QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs*](https://doi.org/10.1145/1988042.1988046)
- [fast-check: por qué usar property-based testing](https://fast-check.dev/docs/introduction/why-property-based/)
- [jqwik: guía oficial](https://jqwik.net/docs/current/user-guide.html)
