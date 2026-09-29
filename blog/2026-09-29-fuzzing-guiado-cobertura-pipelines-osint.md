---
title: "Fuzzing guiado por cobertura en OSINT: romper el parser sin romper la evidencia"
slug: /fuzzing-guiado-cobertura-pipelines-osint
authors: [osint-writter]
tags: [osint, methodology, testing, automation, data, privacy]
date: 2026-09-29
image: /img/blog/2026-09-29-fuzzing-guiado-cobertura-pipelines-osint.png
aiDisclosure: generated
humanReviewed: false
---

![Ilustración editorial de una analista aislando un fallo hallado mediante fuzzing en un pipeline OSINT](/img/blog/2026-09-29-fuzzing-guiado-cobertura-pipelines-osint.png)

**Descargar el podcast!**: [Descargar el podcast](/podcasts/fuzzing-guiado-cobertura-pipelines-osint.m4a)


*Imagen generada mediante inteligencia artificial.*

El CSV parecía rutinario: cabecera, fechas, importes y una fila por expediente. Bastó una comilla sin cerrar junto a un salto de línea para que el parser mezclara dos registros y asignara una cantidad al identificador equivocado. El proceso no se detuvo; produjo una tabla limpia, un gráfico convincente y una conclusión falsa. **En un pipeline OSINT, el fallo más caro puede ser el que no parece un fallo.**

El *fuzzing* guiado por cobertura somete una función a muchas entradas mutadas y usa la instrumentación del programa para conservar aquellas que alcanzan rutas nuevas. Es especialmente útil en parsers, descompresores, normalizadores y conversores. No comprueba que una fuente sea verdadera, completa o representativa: busca comportamientos técnicos peligrosos dentro de nuestro propio software.

<!-- truncate -->

## Qué es y para qué sirve

Un *fuzzer* ejecuta repetidamente un objetivo pequeño con entradas cambiantes. En el modelo guiado por cobertura, esas mutaciones no se tratan todas igual. Si una entrada activa una rama que el corpus aún no recorría, se conserva para producir nuevas variaciones. La documentación de [libFuzzer](https://llvm.org/docs/LibFuzzer.html) lo describe como un motor evolutivo, en proceso y guiado por cobertura que alimenta una función objetivo con datos mutados.

El ciclo básico tiene cinco piezas:

1. **Objetivo o *harness*:** una función estrecha que acepta bytes y llama al código que queremos probar.
2. **Corpus semilla:** muestras pequeñas, variadas y preferiblemente sintéticas.
3. **Instrumentación:** señales sobre qué zonas del código ejecutó cada entrada.
4. **Mutación:** cambios de bytes, tamaños, delimitadores o combinaciones del corpus.
5. **Oráculo de fallo:** una caída, una excepción no esperada, un timeout o una aserción que viola una propiedad explícita.

La cobertura orienta la exploración; no es el objetivo editorial. Alcanzar una rama nueva solo significa que el fuzzer encontró otro camino de ejecución. No prueba que esa rama sea correcta, relevante ni segura. Del mismo modo, un 100 % de líneas recorridas no implica que hayamos formulado todas las aserciones necesarias.

### Diferencia frente a las pruebas basadas en propiedades

Las [pruebas basadas en propiedades](/property-based-testing-pipelines-osint) empiezan por un dominio y una propiedad: por ejemplo, «normalizar dos veces debe producir el mismo resultado». Su generador intenta encontrar un contraejemplo dentro de ese modelo.

El fuzzing guiado por cobertura empieza por una superficie ejecutable y usa las rutas del programa para decidir qué entradas merecen nuevas mutaciones. Puede descubrir combinaciones que no habíamos modelado, pero necesita un buen objetivo y oráculos útiles. Ambas técnicas se complementan: una propiedad puede convertirse en aserción del *harness*, y un crash reducido puede pasar a la batería de regresión.

### Qué significa realmente un crash

En Python, [Atheris](https://github.com/google/atheris) informa de una excepción no capturada en el código probado. En código nativo, libFuzzer suele combinarse con sanitizadores. [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html), por ejemplo, detecta accesos fuera de límites, usos después de liberar memoria y dobles liberaciones, entre otros errores de memoria.

Un crash es una entrada que dispara un comportamiento técnico observable. Todavía hay que reproducirlo, minimizarlo, identificar su causa y decidir su impacto. No demuestra manipulación de la fuente ni convierte el contenido mutado en evidencia del mundo real.

## Caso legítimo: un parser CSV para Villa Serena

Imaginemos un observatorio que analiza contratos del municipio ficticio de **Villa Serena**. Descarga ficheros CSV públicos, conserva los originales y produce estadísticas agregadas. El equipo quiere endurecer su parser antes de actualizarlo. No ejecutará el fuzzer contra el portal ni usará expedientes reales: prepara semillas inventadas con la misma estructura general.

El formato de prueba contiene cinco columnas:

```text
expediente_id,lote_id,fecha,estado,importe_eur
VS-1001,01,2026-08-12,adjudicado,1250.00
```

El riesgo no es solo que el parser termine con error. También importa que acepte una entrada ambigua y desplace columnas, duplique filas o cambie una cantidad sin marcar el registro como inválido. El equipo define por adelantado estos resultados aceptables:

- entrada válida: estructura normalizada y trazabilidad hasta los bytes originales;
- entrada inválida: rechazo explícito, sin derivados publicables;
- entrada grande o costosa: límite de tiempo o tamaño, sin agotar el entorno;
- cualquier otro comportamiento: fallo que debe investigarse.

## Flujo recomendado paso a paso

### 1. Escoge una frontera pequeña

Empieza por una función pura o casi pura: `parsear_csv(bytes)`, `leer_fecha(texto)` o `extraer_tabla(documento)`. No apuntes el fuzzer al pipeline completo. La red, las credenciales, las colas y la publicación crean efectos laterales, ralentizan cada iteración y dificultan saber qué causó el fallo.

Una buena frontera recibe datos en memoria y devuelve una estructura o un error definido. Si el código solo acepta rutas, envuélvelo con un directorio temporal controlado y elimina todo al terminar. El objetivo nunca debe escribir en el almacén canónico.

### 2. Construye un corpus pequeño y diverso

Incluye unas pocas semillas que representen decisiones estructurales, no miles de copias:

- fichero vacío y solo con cabecera;
- una fila válida y varias filas válidas;
- comillas, comas y saltos de línea dentro de campos;
- UTF-8 y caracteres no ASCII;
- fin de línea `LF` y `CRLF`;
- campo opcional vacío;
- fila corta, fila larga y columna desconocida.

Usa valores ficticios. Un corpus con nombres, correos o contratos reales puede acabar copiado a logs, artefactos de CI o informes de crashes. La documentación de libFuzzer recomienda semillas válidas e inválidas variadas y explica que una entrada que descubre cobertura nueva se incorpora al corpus. También permite minimizar un corpus conservando la cobertura alcanzada.

### 3. Escribe un objetivo determinista

Para un parser Python, un boceto con Atheris puede ser tan pequeño como este:

```python
import sys
import atheris

with atheris.instrument_imports():
    from villa_serena import parsear_csv, ErrorDeFormato


def test_one_input(data: bytes) -> None:
    if len(data) > 64_000:
        return

    try:
        filas = parsear_csv(data)
    except ErrorDeFormato:
        return

    assert all(fila["expediente_id"].startswith("VS-") for fila in filas)
    assert len({fila["clave"] for fila in filas}) == len(filas)


atheris.Setup(sys.argv, test_one_input)
atheris.Fuzz()
```

El ejemplo solo ilustra la forma del *harness*. Las aserciones deben corresponder al contrato real del parser; exigir el prefijo `VS-` sería incorrecto si el formato admite otros municipios. Captura únicamente los errores que forman parte de la interfaz. Un `except Exception` indiscriminado ocultaría precisamente los fallos que buscamos.

El objetivo debe producir el mismo resultado con los mismos bytes y el mismo binario. Evita reloj, aleatoriedad no fijada, peticiones HTTP, dependencias remotas y estado global acumulado. LibFuzzer ejecuta el objetivo muchas veces dentro del mismo proceso; el estado que sobrevive entre iteraciones puede generar resultados engañosos.

### 4. Pon límites antes de ejecutar

Ejecuta en un contenedor o usuario sin credenciales, sin acceso al almacén de originales y con red denegada. Limita tamaño de entrada, memoria, CPU, tiempo por caso, duración total y espacio de artefactos. Un parser puede no caer, pero sí entrar en una expansión desproporcionada o un bucle muy lento.

Separa campañas breves y largas. [ClusterFuzzLite](https://google.github.io/clusterfuzzlite/) distingue el fuzzing rápido asociado a cambios de código de ejecuciones por lotes más prolongadas que enriquecen el corpus. El patrón es útil aunque no adoptes esa plataforma: en cada cambio, reproduce el corpus y los crashes conocidos; fuera del camino crítico, explora durante más tiempo con límites explícitos.

### 5. Trata el crash como una pista reproducible

Cuando aparezca un artefacto:

1. guarda sus bytes, hash, comando, revisión del código y entorno;
2. vuelve a ejecutarlo sin iniciar una campaña nueva;
3. minimízalo conservando el mismo fallo;
4. clasifica si es crash, timeout, consumo excesivo o aserción;
5. corrige la causa y añade el caso reducido como regresión;
6. ejecuta el corpus anterior y el nuevo antes de cerrar.

La documentación de [OSS-Fuzz sobre reproducción](https://google.github.io/oss-fuzz/advanced-topics/reproducing/) insiste en reconstruir el fuzzer y alimentar el caso reproductor al objetivo correspondiente. Esa trazabilidad evita atribuir a una entrada un error que en realidad dependía de otra compilación, un estado residual o una configuración distinta.

### 6. Mide algo más que ejecuciones por segundo

La velocidad ayuda, pero no basta. Registra:

| Señal | Pregunta útil |
| --- | --- |
| Cobertura del objetivo | ¿Qué rutas siguen sin alcanzarse? |
| Tamaño del corpus | ¿Cada semilla aporta comportamiento distinto? |
| Estabilidad | ¿Los mismos bytes reproducen el mismo resultado? |
| Crashes únicos | ¿Comparten causa o solo apariencia? |
| Tiempo y memoria | ¿Hay entradas con coste desproporcionado? |
| Regresiones | ¿Cada fallo corregido se ejecuta siempre? |

No conviertas la cobertura en una competición. Un *harness* puede recorrer mucho código irrelevante y omitir la transformación crítica. Revisa qué funciones alcanza, qué errores absorbe y qué invariantes observa.

## Limitaciones y falsos positivos

- **El objetivo define el horizonte.** Lo que queda fuera del *harness* no se prueba.
- **La cobertura no mide semántica.** Ejecutar una rama no demuestra que el resultado sea correcto.
- **Un crash puede ser del propio objetivo.** Aserciones equivocadas y adaptadores defectuosos también fallan.
- **El corpus introduce sesgo.** Semillas muy parecidas pueden encerrar la exploración en una zona cómoda.
- **La falta de crash no es ausencia de defectos.** El presupuesto de tiempo y las mutaciones son finitos.
- **Los fallos no reproducibles requieren cautela.** Estado global, concurrencia o recursos externos pueden contaminar el resultado.
- **El código nativo exige instrumentación adecuada.** Una corrupción puede no manifestarse como una caída clara sin sanitizadores.
- **Los parsers tolerantes plantean un oráculo difícil.** Aceptar una entrada extraña puede ser compatible con la especificación.

Hay un falso positivo especialmente peligroso en investigación: interpretar un crash provocado por bytes mutados como una anomalía de la fuente pública. El fuzzer fabrica entradas para probar nuestro software. Salvo que una muestra real, preservada y autorizada reproduzca el problema, el hallazgo habla del parser, no del publicador.

## Buenas prácticas de OPSEC, ética y privacidad

- Trabaja solo sobre software propio o expresamente autorizado.
- Usa datos sintéticos y elimina identificadores plausibles del corpus.
- Desactiva red, secretos y credenciales dentro del entorno de fuzzing.
- Monta originales reales como solo lectura o, mejor, déjalos fuera.
- Prohíbe que el objetivo publique, envíe avisos o modifique registros canónicos.
- Limita recursos para que una entrada hostil no afecte a otros trabajos.
- Protege los artefactos de crash: pueden contener fragmentos de las semillas.
- Versiona corpus, diccionarios, objetivo, compilador y opciones relevantes.
- Distingue fallo técnico, impacto editorial y conclusión factual.
- Somete cualquier publicación sensible a revisión humana independiente.

## Lista de control

- [ ] El objetivo cubre una frontera pequeña y valiosa.
- [ ] No tiene acceso a red, secretos ni producción.
- [ ] El corpus es sintético, pequeño y estructuralmente diverso.
- [ ] Entradas válidas e inválidas tienen resultados explícitos.
- [ ] Solo se capturan errores esperados por contrato.
- [ ] Hay límites de tamaño, tiempo, memoria y disco.
- [ ] El mismo artefacto reproduce el mismo fallo.
- [ ] Cada crash conserva hash, revisión y comando de reproducción.
- [ ] Los casos reducidos pasan a regresiones permanentes.
- [ ] La cobertura se revisa por relevancia, no solo por porcentaje.
- [ ] Un pipeline verde no se presenta como prueba de veracidad.
- [ ] Ningún artefacto contiene datos personales innecesarios.

## Alternativas y siguientes pasos

El [property-based testing](/property-based-testing-pipelines-osint) es preferible cuando puedes expresar un dominio y propiedades fuertes. El [mutation testing](/mutation-testing-pipelines-osint) comprueba si los tests reaccionan a cambios sembrados en el código. El [contract testing](/contract-testing-osint) protege la interfaz con una fuente y las [pruebas de caos](/pruebas-caos-pipelines-osint) ensayan fallos operativos controlados. El fuzzing guiado por cobertura ocupa otro lugar: explora rutas del programa mediante entradas mutadas y convierte los fallos reproducibles en regresiones.

El takeaway accionable es concreto: toma hoy el parser más pequeño de tu pipeline, crea cinco semillas ficticias, bloquea la red y ejecútalo con un límite corto. Si aparece un crash, no lances otra campaña todavía: reprodúcelo, redúcelo y conviértelo en test. Si no aparece, inspecciona qué rutas alcanzó antes de afirmar que el parser es robusto.

Como próximo tema, merece la pena estudiar **fuzzing consciente de la estructura**: cómo mutar árboles sintácticos o modelos de datos sin perder toda la validez de entrada, y cómo evitar que un generador sofisticado esconda las fronteras defectuosas que precisamente queremos descubrir.

## Fuentes consultadas

- [LLVM: documentación oficial de libFuzzer](https://llvm.org/docs/LibFuzzer.html)
- [Google: repositorio y documentación de Atheris](https://github.com/google/atheris)
- [Clang: documentación oficial de AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)
- [ClusterFuzzLite: documentación oficial](https://google.github.io/clusterfuzzlite/)
- [ClusterFuzzLite: modos de ejecución](https://google.github.io/clusterfuzzlite/running-clusterfuzzlite/)
- [OSS-Fuzz: reproducir un crash](https://google.github.io/oss-fuzz/advanced-topics/reproducing/)
