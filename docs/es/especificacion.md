# Especificación de un howware

*Versión 0.2 · [Read in English](../spec.md)*

De qué está hecho un howware, para que cualquiera pueda construir uno, revisar uno o saber si algo lo es. Las
palabras **DEBE**, **DEBERÍA** y **PUEDE** se usan como en el [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
(*MUST*, *SHOULD*, *MAY*).

## 1. Términos

| Término | Significado |
|---|---|
| **Howware** | Un saber hacer puesto a trabajar por un agente de IA: protocolo, herramientas, adaptadores y memoria, con la conversación como interfaz |
| **Dueño** | La persona cuyo saber hacer y cuyos datos atiende el howware |
| **Anfitrión** | El entorno del agente que carga el protocolo y ejecuta las herramientas (Claude Code, Codex…). No es parte del howware |
| **Protocolo** | El saber hacer en lenguaje natural (un archivo de skill) |
| **Herramienta** | Un programa pequeño, parte de un howware, que hace las operaciones exactas de su trabajo |
| **Adaptador** (*adapter*) | Un programa reutilizable que conecta a los howwares con su entorno (documentos, almacenes de datos, servicios) y no tiene reglas de ningún trabajo (§7) |
| **Memoria** | Donde se guardan el estado, las reglas y la historia del dueño; se usa a través de un adaptador de memoria |

## 2. Arquitectura

Un howware sigue la idea de puertos y adaptadores (arquitectura limpia): el núcleo no conoce el entorno en el que
corre.

```text
dueño ⇄ conversación ⇄ anfitrión ── protocolo (núcleo: el saber hacer y las reglas del dueño)
                                  └─ herramientas (operaciones exactas de este trabajo)
                                       └─ adaptadores ⇄ entorno: documentos · memoria · servicios
```

| Capa | Contiene | Ejemplo |
|---|---|---|
| **Núcleo** | El protocolo y las reglas que enseña el dueño (guardadas como datos en la memoria) | «La renta se factura por el mes siguiente»; «OXXO es súper» |
| **Herramientas** | Las operaciones exactas de este trabajo | Presupuestos, recurrencias, reportes |
| **Adaptadores** | El acceso al entorno, compartido por varios howwares | Leer un estado de cuenta, leer documentos del SAT, el almacén de la memoria |

De ahí salen tres reglas:

1. **Los adaptadores no tienen reglas de ningún trabajo.** Qué es un ingreso, cómo tributa o a qué categoría
   pertenece un comercio se decide en el núcleo; un adaptador lee, escribe, calcula y verifica.
2. **La privacidad se protege en el borde.** Un adaptador que lee fuentes sensibles quita o reemplaza con
   seudónimos los datos personales antes de que algo llegue al agente.
3. **El núcleo llega al entorno solo a través de adaptadores.** El protocolo le dice al agente qué adaptador o
   herramienta ejecutar; las herramientas llaman a adaptadores en lugar de abrir documentos o almacenes por su
   cuenta.

## 3. Estructura del repositorio

Un howware DEBERÍA ser un repositorio con esta estructura (la [plantilla](../../template/) la implementa):

```text
<nombre>/
  howware.json                 manifiesto (§4)
  README.md                    qué hace, instalación, privacidad (§9), límites
  skill/<nombre>/SKILL.md      protocolo (§5)
  skill/<nombre>/scripts/      herramientas (§6) y datos iniciales de la memoria
  tests/                       pruebas de herramientas con datos sintéticos; escenarios de conversación
  tools/install_skill.py       instala el skill en un anfitrión
  tools/check_private_data.py  guardia de CI contra datos reales (§9)
  .github/workflows/ci.yml     corre la guardia y las pruebas
  AGENTS.md · CLAUDE.md        reglas para quien desarrolle el howware con IA
  SECURITY.md · LICENSE
```

Los adaptadores viven en sus propios repositorios, con su versión, pruebas y guardia, para que varios howwares
puedan usarlos.

## 4. Manifiesto: `howware.json`

Todo howware DEBE incluir un manifiesto en la raíz del repositorio. El formato y un ejemplo completo están en la
[especificación en inglés](../spec.md#4-manifest-howwarejson); los nombres de los campos son siempre en inglés.

| Campo | Obligatorio | Significado |
|---|---|---|
| `howware` | DEBE | Versión de esta especificación |
| `name`, `version`, `description`, `license` | DEBE | Identidad; `version` sigue el versionado semántico |
| `languages` | DEBERÍA | Idiomas en los que está escrito el protocolo (el agente responde en el idioma del dueño de todas formas) |
| `hosts` | DEBE | Anfitriones en los que se ha probado |
| `skill` | DEBE | Ruta a la carpeta del protocolo |
| `adapters` | DEBE si hay | Los adaptadores que usa (§7), con versión mínima y dónde conseguirlos |
| `requires` | PUEDE | Otros skills o howwares de los que depende, con versión mínima |
| `tools` | DEBE | Cada herramienta, si usa la red y sus dependencias de terceros |
| `memory` | DEBE | Dónde vive el estado y si se conserva la historia |
| `privacy` | DEBE | Las tres listas de §9, en lenguaje claro |

Los manifiestos de la versión 0.1 listaban los adaptadores en `requires`; quien los lea DEBERÍA aceptar ambos.

## 5. Protocolo

El protocolo DEBE ser un archivo de skill (`SKILL.md`) con encabezado (`name`, `description`) que el anfitrión usa
para decidir cuándo cargarlo. La `description` DEBE decir qué trabajos atiende, con las palabras que usaría el
dueño.

El protocolo DEBE incluir:

1. **Reglas (no negociables).** Lo que el agente siempre y nunca debe hacer, empezando por la privacidad y las
   acciones hacia afuera.
2. **Arranque.** Qué ejecutar al inicio de una sesión y qué mostrar primero (los pendientes).
3. **Flujos de trabajo.** Una sección por trabajo: cuándo aplica, qué herramientas usar, qué mostrar, qué preguntar.
4. **La frontera de la exactitud.** Qué operaciones el agente DEBE delegar a herramientas (aritmética, lectura de
   formatos, escribir el estado) y nunca hacer por sí mismo.
5. **Aprobación.** Qué decisiones aprueba el dueño y cómo se presentan las propuestas (en bloque, guardando las
   palabras del dueño como evidencia).
6. **Presentación de resultados.** Formato, idioma, qué es dato y qué es estimación.

El protocolo DEBERÍA ser legible para el dueño: oraciones claras, ejemplos con sus palabras, sin más código que los
comandos a ejecutar. Las reglas del trabajo viven en el protocolo; las reglas que enseña el dueño viven en la
memoria (§8).

## 6. Herramientas

Estos requisitos aplican a las herramientas y a los adaptadores. Cada uno:

- DEBE ser un programa de línea de comandos que el anfitrión pueda ejecutar, con `--help` y `--version`.
- DEBE escribir su resultado como JSON en la salida estándar y los diagnósticos en la salida de error.
- DEBE reportar errores como JSON (`{"ok": false, "error": {...}}`) con un código de salida distinto de cero y
  documentado. NO DEBE hacer preguntas interactivas.
- DEBE ser determinista para la misma entrada y el mismo estado.
- NO DEBE usar la red salvo que el manifiesto lo declare, y DEBERÍA no tener dependencias de terceros.
- DEBE recibir los secretos solo por variables de entorno, nunca como argumentos ni en archivos del repositorio.
- DEBE hacer escrituras idempotentes: repetir la misma operación no duplica el estado.
- DEBE rechazar entradas que corromperían el estado o filtrarían datos personales, y decir por qué.
- DEBERÍA verificar las versiones de los adaptadores de los que depende.
- DEBERÍA hacer el trabajo masivo en una sola llamada, para que el agente nunca transcriba registros.

## 7. Adaptadores

Además de §6, un adaptador:

- NO DEBE contener las reglas de un trabajo ni decisiones que le corresponden al dueño. Cuando hace falta una
  decisión (un tratamiento fiscal, una categoría), viene de los datos del dueño: una plantilla tomada de un
  documento real, una regla en la memoria.
- DEBE, cuando lee fuentes sensibles, entregar solo lo que el trabajo necesita, reemplazar los identificadores con
  seudónimos que solo son estables con una llave que guarda el dueño, y retener su salida si un valor personal se
  fuera a colar (falla cerrado).
- DEBE guardar los datos privados que almacene (plantillas, fichas, cachés) fuera de todo repositorio, y DEBERÍA
  decirle al dueño cómo mantenerlos fuera del alcance del agente.
- PUEDE tener dependencias de terceros cuando el entorno las exige (leer PDF, por ejemplo), declaradas en su
  paquete.
- NO DEBE usar la red salvo que lo declare. Un adaptador que actúa fuera de la computadora (enviar, presentar,
  pagar) DEBE exigir un argumento explícito para cada acción, para que el protocolo pueda poner antes la aprobación
  del dueño.
- DEBERÍA vivir en su propio repositorio, con README, guía para agentes, pruebas sintéticas y guardia de datos
  privados.

## 8. Memoria

- El estado DEBE vivir donde decida el dueño, fuera del repositorio del howware.
- DEBERÍA conservarse la historia: los cambios cierran, corrigen o anulan registros con un motivo; no los
  sobrescriben en silencio.
- El dinero DEBE guardarse en la unidad mínima (centavos enteros) con una unidad declarada. Igual otras cantidades
  exactas.
- Los registros DEBERÍAN tener claves estables derivadas de su fuente, para que las importaciones sean idempotentes.
- Las fechas de calendario DEBERÍAN guardarse a mediodía en la zona local.
- Las reglas que enseña el dueño (categorías, presupuestos, nombres) DEBEN guardarse como datos en la memoria, con
  las palabras del dueño como evidencia, no como cambios al código.
- Los registros de alto volumen DEBERÍAN quedar fuera del resumen de inicio de sesión.
- Las preguntas repetidas DEBERÍAN guardarse como consultas con nombre y parámetros.

## 9. Privacidad

Un howware DEBE:

- Publicar en su README las tres listas de su manifiesto: **qué está diseñado para quedarse local**, **qué ve el
  agente** y **qué no puede garantizar**. Las afirmaciones DEBEN ser exactas; las absolutas («nunca», «100 %») DEBEN
  evitarse salvo que sean estrictamente ciertas para todo el sistema, incluido el proveedor de IA.
- Procesar los documentos sensibles con adaptadores locales antes de que el agente vea nada, cuando el trabajo los
  involucra.
- Correr en CI una guardia que rechace documentos, bases de datos e identificadores personales en archivos
  versionados.
- Usar solo datos sintéticos en pruebas y fixtures.

Un howware DEBERÍA recomendar permisos del anfitrión que respalden sus reglas (por ejemplo, negar la lectura de
tipos de documentos sensibles) y decir cuáles son sus límites.

## 10. Pruebas

- Las herramientas y los adaptadores DEBEN tener pruebas automatizadas con datos sintéticos, ejecutadas en CI.
- Un howware DEBERÍA incluir escenarios de conversación (`tests/conversations.md`): lo que dice el dueño y lo que
  el agente debe hacer (qué herramientas, qué preguntar, qué rechazar). Mientras no se automaticen, se revisan a
  mano antes de cada versión.
- CI DEBERÍA instalar el skill en una carpeta temporal y ejecutar sus herramientas de punta a punta.

## 11. Versiones

- `version` sigue el [versionado semántico](https://semver.org/lang/es/). Cambiar datos iniciales que afecten
  memorias existentes DEBERÍA subir su propia versión de semilla.
- Un `CHANGELOG.md` DEBERÍA registrar los cambios visibles para el dueño, incluidos los del comportamiento del
  protocolo.

## 12. Lista de conformidad

Un proyecto es un howware conforme cuando:

- [ ] Tiene un `howware.json` válido.
- [ ] Su protocolo tiene reglas, arranque, flujos, frontera de la exactitud, aprobación y presentación.
- [ ] Toda operación exacta la hace una herramienta o un adaptador; se le indica al agente que nunca transcriba ni
      calcule.
- [ ] Sus herramientas cumplen §6 (salida JSON, códigos de salida, sin preguntas, sin red no declarada,
      idempotentes).
- [ ] Llega a documentos y almacenes solo a través de adaptadores que cumplen §7, listados en su manifiesto.
- [ ] Las reglas del dueño viven en la memoria, no en el código.
- [ ] Su README dice qué se queda local, qué ve el agente y qué no puede garantizar, sin afirmaciones absolutas.
- [ ] CI corre una guardia de datos privados y las pruebas de herramientas con datos sintéticos.

El skill [`howware-review`](../../skills/howware-review/SKILL.md) revisa esta lista.

---

*Bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es).*
