---
title: "Companies House en OSINT: registro societario, PSC y filings con contexto"
slug: /companies-house-osint-registro-societario-psc-filings-contexto
authors: [osint-writter]
tags: [osint, due-diligence, data, verification, privacy, investigation]
date: 2026-07-08
image: /img/blog/2026-07-08-companies-house-osint-registro-societario-psc-filings-contexto.png
---

![Ilustracion editorial de una analista OSINT revisando documentos societarios publicos, historial de filings, personas con control significativo y una linea temporal de verificacion](/img/blog/2026-07-08-companies-house-osint-registro-societario-psc-filings-contexto.png)

Una sociedad puede parecer limpia en una web corporativa, pero cambiar de forma cuando lees su numero registral, sus cuentas, sus cargos, sus personas con control significativo, sus direcciones historicas y sus documentos presentados. `Companies House` es una de esas fuentes que obligan a bajar del relato comercial al registro primario: no resuelve una investigacion por si sola, pero ayuda a convertir sospechas vagas en preguntas verificables.

Revisando la documentacion publica el **8 de julio de 2026**, el servicio `Find and update company information` permite buscar gratis datos publicos de empresas britanicas, ver documentos, cargos, personas descalificadas, informacion de hipotecas/charges, insolvencia y seguir empresas para recibir alertas. La guia oficial fue actualizada el **9 de junio de 2026** y recuerda un limite clave: la informacion disponible no debe tratarse como fuente completa de derecho societario ni como sustituto de asesoramiento profesional. Ademas, las reformas de la `Economic Crime and Corporate Transparency Act` han introducido verificaciones de identidad, nuevos poderes de comprobacion y cambios en la calidad del registro.

Este articulo esta escrito para analistas OSINT, equipos de compliance, periodistas, investigadores corporativos y defensores que trabajan con fuentes abiertas de forma proporcionada. No contiene instrucciones para acosar personas, perfilar vidas privadas, doxxing ni automatizacion abusiva contra servicios publicos.

<!-- truncate -->

## Que es Companies House y para que sirve

[`Companies House`](https://www.gov.uk/government/organisations/companies-house) es el registro mercantil del Reino Unido para sociedades constituidas bajo el marco correspondiente de Inglaterra y Gales, Escocia o Irlanda del Norte. Su funcion practica para OSINT es permitir que una investigacion societaria empiece por una entidad legal concreta, no solo por una marca, dominio o nombre comercial.

El servicio publico [`Find and update company information`](https://find-and-update.company-information.service.gov.uk/) permite buscar por nombre de empresa, numero societario u oficial. La pagina de busqueda muestra funciones como ver datos y documentos, buscar directores descalificados, seguir empresas, consultar busqueda avanzada y acceder a registros disueltos.

Para un flujo de investigacion responsable, Companies House ayuda a responder preguntas como estas:

- que entidad legal concreta existe detras de un nombre;
- cual es su numero de compania y su estado actual;
- cuando se incorporo, si esta activa, disuelta, en liquidacion o con otra situacion;
- que direccion registrada declara y como ha cambiado;
- que `SIC codes` usa para describir su actividad;
- que cuentas, confirmation statements y otros documentos ha presentado;
- que cargos actuales o historicos aparecen;
- que personas con control significativo (`PSC`) declara;
- que cargas, hipotecas o insolvencias figuran cuando aplica;
- que fechas de proximas cuentas o declaraciones conviene vigilar.

La guia oficial de busqueda explica que los datos publicos pueden verse gratis sin registrarse y que tambien existe una `API` para acceder a actualizaciones en tiempo real. Esa combinacion es potente: interfaz web para revision humana, `API` para flujos documentados y alertas de seguimiento para cambios relevantes.

## Caso de uso legitimo con ejemplo ficticio

Imagina que una ONG ficticia, `Puente Claro`, evalua un proveedor britanico que ofrece servicios de verificacion documental. La web habla de "grupo internacional", "oficinas en Londres" y "decadas de experiencia", pero el equipo de due diligence necesita separar tres planos:

| Pregunta | Dato que buscaria | Lectura prudente |
| --- | --- | --- |
| Identidad legal | Numero de compania, estado y fecha de incorporacion | Confirma que entidad estas investigando, no si es fiable |
| Continuidad | Filing history, cuentas y confirmation statements | Muestra habitos de presentacion, no calidad operativa |
| Control | PSC y cargos | Sugiere estructura formal, no control real fuera del registro |
| Actividad | SIC codes y cuentas | Ayuda a contextualizar, pero puede ser generico |
| Riesgo temporal | cambios recientes de direccion, cargos o nombre | Senala preguntas, no culpabilidad |

Un flujo sano no empezaria con una acusacion. Empezaria con una ficha de entidad:

```text
Entidad: Northbridge Verification Services Ltd (ficticia)
Numero: 00000000 (ficticio)
Estado: active / dissolved / liquidation, segun registro
Fecha de consulta: 2026-07-08
Fuente primaria: URL de Companies House
Hipotesis: comprobar si el proveedor real coincide con la entidad legal citada
```

Despues vendria la trazabilidad: capturar la URL consultada, anotar fecha y hora, descargar solo documentos necesarios, guardar hashes de los documentos relevantes y separar hechos registrales de inferencias analiticas.

## Flujo recomendado

### 1. Empieza por el identificador estable

El nombre de una empresa puede tener variantes, errores, marcas comerciales o traducciones. El numero de compania es mucho mas estable. Si partes de una web, factura o nota de prensa, busca:

- razon social exacta;
- numero de compania;
- direccion registrada;
- nombres anteriores;
- dominios o marcas que la propia entidad declare.

Si varias empresas se parecen, no las fusiones deprisa. Crea una tabla de candidatos y descarta con evidencia: jurisdiccion, fecha, direccion, cargos, documento fuente y relacion declarada.

### 2. Lee el perfil como una linea temporal

El error habitual es abrir el perfil actual y copiar tres campos. En investigacion, la pregunta suele ser temporal:

- cuando se creo la sociedad;
- cuando cambio de nombre;
- cuando cambio de direccion;
- cuando entraron o salieron cargos;
- cuando se presentaron cuentas;
- si hubo periodos de retraso, strike off, disolucion o restauracion;
- que documentos explican cada cambio.

La `filing history` es el hilo conductor. No todos los documentos tienen el mismo peso, y muchos solo registran una declaracion formal. Aun asi, ordenarlos por fecha permite detectar cambios que merecen verificacion adicional.

### 3. Trata los PSC como senal, no como sentencia

Las personas con control significativo (`PSC`) son una pieza central de transparencia societaria, pero conviene leerlas con cuidado. Un PSC puede aparecer por porcentaje de acciones, derechos de voto, capacidad de nombrar directores u otras formas de influencia significativa. La ausencia, el cambio o la naturaleza de una declaracion PSC no deberian convertirse automaticamente en acusacion.

Desde el **18 de noviembre de 2025**, la verificacion de identidad paso a ser requisito legal para directores y PSC dentro de un periodo transitorio de 12 meses, segun la pagina oficial de cambios de Companies House. Para OSINT, esto no significa que todo dato historico sea perfecto ni que la verificacion resuelva estructuras complejas. Significa que el contexto normativo esta cambiando y que los informes deben fechar claramente la consulta.

### 4. Cruza con fuentes primarias, no solo agregadores

`OpenCorporates`, bases de sanciones, prensa, webs corporativas, dominios, registros de contratacion y archivos web pueden ayudar a encontrar pistas. Pero cuando investigas una sociedad britanica, Companies House debe funcionar como fuente primaria para los datos registrales britanicos.

Un cruce razonable seria:

- Companies House para entidad, filings, cargos, PSC y cambios;
- web corporativa para afirmaciones comerciales;
- Wayback Machine o Archive.today para versiones historicas de la web;
- OpenSanctions si hay coincidencias de sanciones o PEP que deban verificarse;
- OpenCorporates si necesitas ampliar a otras jurisdicciones;
- registros de contratacion o licitaciones si el caso trata de proveedor publico;
- prensa y comunicados solo como contexto, nunca como sustituto del documento registral.

### 5. Usa la API con moderacion y trazabilidad

El `Developer Hub` de Companies House describe una `REST API` que devuelve datos en `JSON` y una lista de especificaciones `OpenAPI`. La autenticacion de API usa una clave mediante autenticacion basica; algunas funciones requieren `OAuth 2.0`.

Para un flujo OSINT responsable, la API tiene sentido cuando:

- necesitas revisar cambios de una lista acotada de entidades;
- quieres construir una tabla reproducible con campos concretos;
- vas a documentar consultas y fechas;
- respetas limites, terminos y uso aceptable;
- evitas descargar mas informacion personal de la necesaria.

No uses automatizacion para degradar el servicio, hacer scraping masivo innecesario ni construir bases de datos de personas sin base legitima. La propia guia de servicio advierte que las bases de datos buscables no estan pensadas como fuente de descargas masivas y que el uso que degrade el servicio puede ser bloqueado.

## Limitaciones y falsos positivos

Companies House es fuerte porque es una fuente primaria, pero no es infalible. La guia oficial incluye varios matices que deberian aparecer en cualquier informe serio:

- el servicio no pretende ser una fuente completa de derecho societario;
- puede haber errores u omisiones;
- algunos documentos se revisan con comprobaciones basicas, no con auditoria sustantiva completa;
- el registro puede contener informacion que despues se corrige, elimina o anota;
- los enlaces externos dentro de documentos no implican respaldo;
- los datos personales publicados deben tratarse con minimizacion y proporcionalidad.

Tambien hay falsos positivos tipicos:

- dos personas con el mismo nombre tratadas como una sola;
- empresas con nombres parecidos mezcladas por error;
- direccion de agente o proveedor leida como oficina operativa;
- SIC code generico tratado como descripcion exacta del negocio;
- PSC formal interpretado como beneficiario real absoluto;
- documento presentado tarde interpretado automaticamente como fraude;
- sociedad disuelta confundida con actividad actual.

La buena practica es escribir en condicional cuando toca. "Figura como director" no es lo mismo que "controla". "Comparte direccion registrada" no es lo mismo que "opera desde el mismo lugar". "Cambio de nombre" no es lo mismo que "intento de ocultacion".

## Buenas practicas de OPSEC, etica y privacidad

Trabajar con registros societarios no elimina la obligacion de cuidar a personas reales. Algunas recomendaciones practicas:

- minimiza datos personales en notas, capturas y entregables;
- evita publicar fechas de nacimiento parciales o direcciones si no aportan valor proporcional;
- separa empresas, cargos y personas en entidades distintas;
- documenta fuentes, fechas y capturas sin crear expedientes innecesarios;
- no contactes a domicilios, familiares ni terceros no relacionados;
- no uses la investigacion para acoso, exposicion publica o presion personal;
- da derecho de replica o verificacion adicional cuando el contexto lo exija;
- conserva evidencias de forma segura y con control de acceso.

En due diligence, la pregunta no es "cuanto puedo encontrar", sino "que necesito saber para tomar una decision proporcionada y verificable".

## Alternativas y siguientes pasos

Companies House funciona muy bien para entidades britanicas. Si el caso cruza fronteras o sectores, conviene combinarlo con:

- `OpenCorporates`, para descubrir entidades en varias jurisdicciones y llegar a registros primarios;
- `OpenOwnership`, para modelos de beneficiarios reales cuando existan datos estructurados;
- `OpenSanctions`, para revisar coincidencias de sanciones, PEP y listas relevantes con cautela;
- `EDGAR`, si hay companias cotizadas o filings estadounidenses;
- registros mercantiles nacionales, cuando la entidad no sea britanica;
- herramientas de limpieza como `OpenRefine`, si vas a reconciliar muchas variantes de nombres.

El takeaway accionable es sencillo: usa Companies House como **registro primario fechado**, no como maquina de conclusiones. Primero identifica la entidad correcta, luego ordena documentos en una linea temporal, despues cruza con fuentes independientes y solo al final formula hipotesis. En investigacion societaria, la precision suele venir de escribir menos y comprobar mas.

Como siguiente paso editorial, tendria sentido construir una plantilla de due diligence OSINT para entidades legales: campos minimos, fuentes primarias, criterios de incertidumbre y un ejemplo ficticio completo de informe.

## Fuentes consultadas

- [Companies House: Find and update company information](https://find-and-update.company-information.service.gov.uk/)
- [Searching the Companies House register - GOV.UK](https://www.gov.uk/guidance/searching-the-companies-house-register)
- [Companies House API overview](https://developer.company-information.service.gov.uk/)
- [Companies House REST API](https://developer.company-information.service.gov.uk/overview)
- [API authentication - Companies House Developer Hub](https://developer.company-information.service.gov.uk/authentication)
- [Identity verification - Changes to UK company law](https://changestoukcompanylaw.campaign.gov.uk/identity-verification/)
- [Changes at a glance - Changes to UK company law](https://changestoukcompanylaw.campaign.gov.uk/changes-at-a-glance/)
- [Progress made in cleaning up Companies House register - GOV.UK](https://www.gov.uk/government/news/progress-made-in-cleaning-up-companies-house-register-as-further-steps-taken-to-tackle-economic-crime)
