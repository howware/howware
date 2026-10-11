# Especificación de un howware

*Versión 0.1 · [Read in English](../spec.md)*

De qué está hecho un howware, para que cualquiera pueda construir uno, revisar uno o saber si algo lo es. Las
palabras **DEBE**, **DEBERÍA** y **PUEDE** se usan como en el [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119)
(*MUST*, *SHOULD*, *MAY*).

## 1. Términos

| Término | Significado |
|---|---|
| **Howware** | Un saber hacer puesto a trabajar por un agente de IA: protocolo, herramientas y convención de memoria, con la conversación como interfaz |
| **Dueño** | La persona cuyo saber hacer y cuyos datos atiende el howware |
| **Anfitrión** | El entorno del agente que carga el protocolo y ejecuta las herramientas (Claude Code, Codex…). No es parte del howware |
| **Protocolo** | El saber hacer en lenguaje natural (un archivo de skill) |
| **Herramienta** | Un programa pequeño que hace una operación exacta |
| **Memoria** | Donde se guardan el estado, las reglas y la historia del dueño |

## 2. Estructura del repositorio

Un howware DEBERÍA ser un repositorio con esta estructura (la [plantilla](../../template/) la implementa):

```text
<nombre>/
  howware.json                 manifiesto (§3)
  README.md                    qué hace, instalación, privacidad (§7), límites
  skill/<nombre>/SKILL.md      protocolo (§4)
  skill/<nombre>/scripts/      herramientas (§5) y datos iniciales de la memoria
  tests/                       pruebas de herramientas con datos sintéticos; escenarios de conversación
  tools/install_skill.py       instala el skill en un anfitrión
  tools/check_private_data.py  guardia de CI contra datos reales (§7)
  .github/workflows/ci.yml     corre la guardia y las pruebas
  AGENTS.md · CLAUDE.md        reglas para quien desarrolle el howware con IA
  SECURITY.md · LICENSE
```

## 3. Manifiesto: `howware.json`

Todo howware DEBE incluir un manifiesto en la raíz del repositorio. El formato y un ejemplo completo están en la
[especificación en inglés](../spec.md#3-manifest-howwarejson); los nombres de los campos son siempre en inglés.

| Campo | Obligatorio | Significado |
|---|---|---|
| `howware` | DEBE | Versión de esta especificación |
| `name`, `version`, `description`, `license` | DEBE | Identidad; `version` sigue el versionado semántico |
| `languages` | DEBERÍA | Idiomas en los que está escrito el protocolo (el agente responde en el idioma del dueño de todas formas) |
| `hosts` | DEBE | Anfitriones en los que se ha probado |
| `skill` | DEBE | Ruta a la carpeta del protocolo |
| `requires` | DEBE si hay | Otras herramientas o skills, con versión mínima |
| `tools` | DEBE | Cada herramienta, si usa la red y sus dependencias de terceros |
| `memory` | DEBE | Dónde vive el estado y si se conserva la historia |
| `privacy` | DEBE | Las tres listas de §7, en lenguaje claro |

## 4. Protocolo

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
memoria (§6).

## 5. Herramientas

Cada herramienta:

- DEBE ser un programa de línea de comandos que el anfitrión pueda ejecutar, con `--help` y `--version`.
- DEBE escribir su resultado como JSON en la salida estándar y los diagnósticos en la salida de error.
- DEBE reportar errores como JSON (`{"ok": false, "error": {...}}`) con un código de salida distinto de cero y
  documentado. NO DEBE hacer preguntas interactivas.
- DEBE ser determinista para la misma entrada y el mismo estado.
- NO DEBE usar la red salvo que el manifiesto lo declare, y DEBERÍA no tener dependencias de terceros.
- DEBE recibir los secretos solo por variables de entorno, nunca como argumentos ni en archivos del repositorio.
- DEBE hacer escrituras idempotentes: repetir la misma operación no duplica el estado.
- DEBE rechazar entradas que corromperían el estado o filtrarían datos personales, y decir por qué.
- DEBERÍA verificar las versiones de las herramientas y la memoria de las que depende.
- DEBERÍA hacer el trabajo masivo en una sola llamada, para que el agente nunca transcriba registros.

## 6. Memoria

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

## 7. Privacidad

Un howware DEBE:

- Publicar en su README las tres listas de su manifiesto: **qué está diseñado para quedarse local**, **qué ve el
  agente** y **qué no puede garantizar**. Las afirmaciones DEBEN ser exactas; las absolutas («nunca», «100 %») DEBEN
  evitarse salvo que sean estrictamente ciertas para todo el sistema, incluido el proveedor de IA.
- Procesar los documentos sensibles con herramientas locales antes de que el agente vea nada, cuando el trabajo los
  involucra.
- Correr en CI una guardia que rechace documentos, bases de datos e identificadores personales en archivos
  versionados.
- Usar solo datos sintéticos en pruebas y fixtures.

Un howware DEBERÍA recomendar permisos del anfitrión que respalden sus reglas (por ejemplo, negar la lectura de
tipos de documentos sensibles) y decir cuáles son sus límites.

## 8. Pruebas

- Las herramientas DEBEN tener pruebas automatizadas con datos sintéticos, ejecutadas en CI.
- Un howware DEBERÍA incluir escenarios de conversación (`tests/conversations.md`): lo que dice el dueño y lo que
  el agente debe hacer (qué herramientas, qué preguntar, qué rechazar). Mientras no se automaticen, se revisan a
  mano antes de cada versión.
- CI DEBERÍA instalar el skill en una carpeta temporal y ejecutar sus herramientas de punta a punta.

## 9. Versiones

- `version` sigue el [versionado semántico](https://semver.org/lang/es/). Cambiar datos iniciales que afecten
  memorias existentes DEBERÍA subir su propia versión de semilla.
- Un `CHANGELOG.md` DEBERÍA registrar los cambios visibles para el dueño, incluidos los del comportamiento del
  protocolo.

## 10. Lista de conformidad

Un proyecto es un howware conforme cuando:

- [ ] Tiene un `howware.json` válido.
- [ ] Su protocolo tiene reglas, arranque, flujos, frontera de la exactitud, aprobación y presentación.
- [ ] Toda operación exacta la hace una herramienta; se le indica al agente que nunca transcriba ni calcule.
- [ ] Sus herramientas cumplen §5 (salida JSON, códigos de salida, sin preguntas, sin red no declarada,
      idempotentes).
- [ ] Las reglas del dueño viven en la memoria, no en el código.
- [ ] Su README dice qué se queda local, qué ve el agente y qué no puede garantizar, sin afirmaciones absolutas.
- [ ] CI corre una guardia de datos privados y las pruebas de herramientas con datos sintéticos.

El skill [`howware-review`](../../skills/howware-review/SKILL.md) revisa esta lista.

---

*Bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es).*
