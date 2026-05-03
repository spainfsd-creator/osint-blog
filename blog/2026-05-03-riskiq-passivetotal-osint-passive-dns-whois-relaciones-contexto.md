---
title: "RiskIQ PassiveTotal en OSINT: passive DNS, WHOIS y relaciones con contexto"
slug: /riskiq-passivetotal-osint-passive-dns-whois-relaciones-contexto
authors: [osint-writter]
tags: [osint, dns, infrastructure, threat-intelligence, verification, due-diligence]
date: 2026-05-03
image: /img/blog/2026-05-03-riskiq-passivetotal-osint-passive-dns-whois-relaciones-contexto.png
---

![Ilustracion editorial de una analista OSINT correlacionando passive DNS, WHOIS, certificados SSL y relaciones entre dominios en varios monitores](/img/blog/2026-05-03-riskiq-passivetotal-osint-passive-dns-whois-relaciones-contexto.png)

Hay investigaciones donde una IP parece no decir gran cosa, un dominio cambia de manos demasiado deprisa y el rastro tecnico de una operacion se dispersa entre DNS, certificados, paginas intermedias y relaciones web apenas visibles. En ese terreno, `RiskIQ PassiveTotal` resulta util porque no se limita a una sola fuente: **intenta ordenar varias capas de infraestructura publica en una misma vista para que el analista pueda pivotar con menos intuicion y mas metodo**.

Eso no convierte la plataforma en una maquina de atribucion. Un solapamiento historico, un `tracker` compartido o un `WHOIS` parecido no demuestran por si solos autoria ni intencion. Lo que si hacen es reducir la niebla: ayudan a montar cronologias, detectar relaciones plausibles y decidir que merece un contraste adicional con otras fuentes abiertas o con validacion interna.

<!-- truncate -->

## Que es y para que sirve

La documentacion oficial de `PassiveTotal` describe la plataforma como un punto de agregacion de multiples datasets para analisis de infraestructura en Internet. Su manual resume un nucleo bastante claro:

- `Passive DNS`, para ver que dominios resolvieron a una IP y viceversa a lo largo del tiempo;
- `WHOIS`, para encontrar datos compartidos entre registros;
- `SSL certificates`, para seguir donde aparecio un mismo certificado;
- `trackers`, para correlacionar sitios mediante identificadores embebidos;
- y `host pairs`, para observar relaciones entre dominios detectadas en crawls web.

La lectura OSINT de todo esto es potente pero muy concreta: `PassiveTotal` sirve menos para "encontrar una respuesta magica" y mas para **convertir infraestructura publica dispersa en una red de pistas contrastables**.

Ademas, a fecha de `3 de mayo de 2026`, el conector oficial `RiskIQ Illuminate` de `Microsoft Learn` sigue documentando operaciones como `Get subdomains`, `Get WHOIS`, `Get SSL certificate history`, `Get trackers` y `Get summary data card`. Esa lista encaja bien con la idea practica del producto: enriquecer un selector y abrir pivotes ordenados sobre dominio, IP y artefactos relacionados.

## Caso de uso legitimo: revisar una infraestructura dudosa sin precipitarse

Imagina que en una investigacion defensiva aparece `dominio-ejemplo.test` asociado a una campaña de suplantacion o a un proveedor que genera dudas. Antes de elevar nada, un flujo sensato con `PassiveTotal` podria ser este:

1. consultar el dominio para ver resoluciones historicas y subdominios;
2. revisar si comparte `WHOIS`, certificados o `trackers` con otros activos;
3. observar `host pairs` para detectar redirecciones o dependencias web relevantes;
4. anotar fechas, solapamientos y huecos de informacion;
5. contrastar despues con otras fuentes antes de sacar conclusiones.

El valor esta en la secuencia. Si una IP alojaba varios dominios en una ventana temporal concreta, si un certificado reaparece en otra infraestructura dias despues o si dos sitios comparten un identificador de analitica, ya tienes hilos razonables para seguir. Pero siguen siendo hilos, no veredictos.

## Flujo recomendado

### 1. Empezar por la dimension temporal

El propio manual define `Passive DNS` como un sistema de registro de resoluciones por ubicacion, tipo de registro y periodo de tiempo. Esa palabra, "tiempo", es la mitad de su utilidad.

En OSINT de infraestructura, muchas confusiones nacen por mezclar estados viejos con estados actuales. Por eso conviene empezar preguntando:

- cuando aparecio esta resolucion;
- cuanto duro;
- que mas resolvia a esa IP en ese tramo;
- y si el cambio coincide con otros hitos tecnicos o publicos.

La vista `Timebar` del manual insiste justo en eso: una investigacion madura no solo necesita relacionar entidades, sino **fijarlas en una cronologia**.

### 2. Usar WHOIS y certificados para enlazar, no para sobreafirmar

La documentacion de datasets explica dos cosas utiles:

- `WHOIS` permite conectar entidades por datos compartidos en el registro;
- y `SSL certificates` ayudan a relacionar infraestructura que `Passive DNS` o `WHOIS` pueden no capturar.

Traducido a practica diaria:

- un correo de registro repetido puede abrir una hipotesis de relacion;
- un certificado reutilizado puede revelar migraciones o continuidad operativa;
- pero ambos tambien pueden reflejar proveedor comun, plantilla heredada o reutilizacion inocente.

La disciplina buena consiste en apuntar la coincidencia y pedirle una segunda opinion a otras fuentes, no en convertirla en atribucion automatica.

### 3. Aprovechar trackers y host pairs para salir del eje dominio-IP

Aqui `PassiveTotal` se vuelve especialmente interesante. Su manual define los `trackers` como codigos o valores unicos encontrados en paginas web y los `host pairs` como dos dominios que compartieron una conexion observada en un crawl de `RiskIQ`, desde una redireccion `302` hasta referencias de `iframe` o scripts.

Para un analista OSINT esto abre preguntas muy utiles:

- que sitios comparten una misma telemetria o analitica;
- que relaciones web existieron entre un dominio "limpio" y otro sospechoso;
- y si esa conexion fue estructural o solo accidental.

Son pivotes muy valiosos para cartografiar ecosistemas, aunque exigen prudencia. Un `tracker` compartido puede apuntar a propiedad comun, pero tambien a una agencia, una plataforma de afiliacion o una mala configuracion de terceros. Un `host pair` puede ser revelador o meramente circunstancial. Contexto, siempre.

### 4. Si la investigacion es recurrente, guardar el trabajo en proyectos y monitorizacion

El manual tambien describe `Projects` como una forma ligera de gestion de caso y `Infrastructure Monitoring` como una capa para vigilar cambios en `Passive DNS`, `WHOIS`, `SSL`, `OSINT` y otras asociaciones.

Eso encaja muy bien con OSINT responsable:

- agrupar artefactos relacionados;
- mantener una historia de investigacion trazable;
- y recibir avisos cuando cambie algo que importa.

Cuando una investigacion dura dias o semanas, esta parte vale casi mas que el primer hallazgo. La memoria automatizada evita depender de capturas sueltas y hace mas facil explicar luego por que una pista merecia seguimiento.

## Limitaciones y falsos positivos

`PassiveTotal` agrega mucho contexto, pero no elimina los problemas clasicos del analisis:

- los datos historicos nunca son equivalentes a observacion total del ecosistema;
- una relacion tecnica no implica control comun;
- algunos enlaces existen por proveedores compartidos, `CDN`, analitica o reventa de infraestructura;
- y la ausencia de una asociacion visible no significa que la relacion no exista.

Tambien conviene recordar otra cosa: la propia pagina de `Passive DNS Sources` deja claro que el producto combina fuentes propias, asociadas y comerciales. Eso es una fortaleza, pero tambien una razon para documentar bien de donde sale cada senal y evitar hablar de cobertura "absoluta".

## Buenas practicas de OPSEC, etica y privacidad

- Trabaja con objetivos justificados por defensa, investigacion periodistica legitima o verificacion de riesgo.
- Registra fecha, consulta exacta y razon del pivote para que otro analista pueda reproducirlo.
- No publiques datos personales o corporativos sensibles si no aportan valor metodologico claro.
- Separa en tus notas lo observado, lo inferido y lo que sigue pendiente de corroboracion.
- Si una coincidencia tecnica puede tener explicacion inocente, escribe esa alternativa al lado en lugar de enterrarla.

La mejor manera de usar `PassiveTotal` no es exprimir cada relacion, sino **frenar a tiempo tus propias ganas de cerrar la historia demasiado pronto**.

## Alternativas y siguientes pasos

Segun la pregunta concreta, `PassiveTotal` suele convivir bien con otras piezas ya tratadas en el blog:

- `SecurityTrails` o `RDAP/WHOIS` para ampliar historico de registro;
- `CT logs` para seguir emisiones de certificados con otra perspectiva;
- `urlscan.io` si quieres observar comportamiento web y recursos cargados;
- y `Amass`, `Netlas` o `Censys` si la prioridad real es expandir superficie externa.

La gracia de `PassiveTotal` esta en que junta varios de esos angulos en una sola mesa de trabajo. No sustituye el contraste, pero si ayuda a que el contraste empiece mejor ordenado.

## Takeaway

Si investigas dominios, IPs o pequenas constelaciones de infraestructura, `RiskIQ PassiveTotal` merece sitio en tu flujo no porque "sepa mas", sino porque te obliga a pensar en **cronologia, asociaciones y trazabilidad** a la vez. Ese cambio de enfoque es justo lo que reduce errores cuando una infraestructura publica parece conectada, pero todavia no sabes de que manera.

Como siguiente puente metodologico, el paso natural seria bajar aun mas al detalle y comparar `trackers`, `host pairs` y `web components` como senales de relacion que a veces parecen obvias y a veces solo son ruido bien disfrazado.

## Fuentes

- [PassiveTotal Manual](https://help.passivetotal.org/)
- [Primary Datasets - PassiveTotal Manual](https://help.passivetotal.org/passivetotal_data_sets.html)
- [Passive DNS Sources - PassiveTotal Manual](https://help.passivetotal.org/passive_dns_sources.html)
- [DNS - PassiveTotal Manual](https://help.passivetotal.org/dns.html)
- [Host Pairs - PassiveTotal Manual](https://help.passivetotal.org/host_pairs.html)
- [Projects - PassiveTotal Manual](https://help.passivetotal.org/projects.html)
- [Infrastructure Monitoring - PassiveTotal Manual](https://help.passivetotal.org/infrastructure_monitoring.html)
- [RiskIQ Illuminate connector - Microsoft Learn](https://learn.microsoft.com/en-us/connectors/riskiqpassivetotal/)
