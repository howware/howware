<h1 align="center">Howware</h1>

<p align="center">
  <b>Del saber hacer a hecho.</b><br>
  Tu saber hacer, puesto a trabajar con IA: sin app que construir, sin intermediarios, sin esperas.
</p>

<p align="center">
  <a href="https://github.com/howware/howware/actions/workflows/ci.yml"><img src="https://github.com/howware/howware/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/especificación-0.2-blue" alt="Especificación 0.2">
  <img src="https://img.shields.io/badge/código-Apache%202.0-green" alt="Código: Apache 2.0">
  <img src="https://img.shields.io/badge/textos-CC%20BY%204.0-green" alt="Textos: CC BY 4.0">
</p>

<p align="center">
  <a href="https://howware.org/es/">howware.org</a> ·
  <a href="MANIFIESTO.md">Manifiesto</a> ·
  <a href="docs/es/whitepaper.md">Whitepaper</a> ·
  <a href="docs/es/especificacion.md">Especificación</a> ·
  <a href="README.md">English</a>
</p>

> **Howware** — tu saber hacer, puesto a trabajar con IA. Dices las reglas con tus palabras; un agente de IA las
> sigue, con unas cuantas herramientas exactas y una memoria que es tuya. Sin app que construir, sin
> intermediarios, sin esperas.

*El hardware lo corre. El software lo ejecuta. El howware sabe cómo.*

---

## Por qué

Quien sabe cómo debe funcionar algo casi nunca es quien lo construye. Le explica las reglas a alguien que
programa; se pierde sentido; cada regla nueva complica más el código; cada cambio espera semanas o meses. Y
alrededor de las reglas, alguien todavía tiene que construir una app —pantallas, formularios, un backend— que
todos los demás tienen que aprender.

La **hoja de cálculo** fue la primera vez que personas que no programan pudieron poner su propio saber hacer a
trabajar sin pedírselo a nadie. **El howware es el siguiente paso**: reglas con tus palabras en lugar de fórmulas,
una conversación en lugar de una cuadrícula, herramientas que leen tus documentos en lugar de copiar y pegar, y un
agente de IA haciendo el trabajo.

## De qué está hecho un howware

| Parte | Qué es |
|---|---|
| **Protocolo** | Tu saber hacer en palabras claras: pasos, criterios, reglas, qué preguntar, qué nunca hacer |
| **Herramientas** | Programas pequeños para las operaciones exactas del trabajo: dinero, fechas, reportes |
| **Adaptadores** | Programas compartidos que conectan a los howwares con tus documentos y datos, y dejan los datos personales en el borde |
| **Memoria** | Tus datos y las reglas que enseñas, en un lugar tuyo, con historia |
| **Conversación** | La única interfaz |

```text
› Ayer gasté 180 en efectivo en la comida.           → registrado, con tus palabras como evidencia
› OXXO es súper, no conveniencia.                    → una regla, vigente ya, para toda la historia
› ¿Cómo voy con el presupuesto de súper?             → $3,180.40 de $4,000.00 (79 %)
```

Lee el [manifiesto](MANIFIESTO.md) para los nueve principios, y el [whitepaper](docs/es/whitepaper.md) para los
patrones, el modelo de privacidad, los límites y **cuándo no conviene howware**.

## Construye uno

Este repositorio incluye dos skills para Claude Code y Codex:

| Skill | Hace |
|---|---|
| [`howware-builder`](skills/howware-builder/SKILL.md) | Te entrevista sobre tu trabajo y construye contigo un howware: diseño, protocolo, herramientas, adaptadores, memoria, pruebas |
| [`howware-review`](skills/howware-review/SKILL.md) | Revisa un howware contra la especificación, incluidas sus promesas de privacidad |

```bash
git clone https://github.com/howware/howware
python howware/tools/install_skills.py                              # Claude Code
python howware/tools/install_skills.py --target-dir ~/.codex/skills  # Codex
```

Los howwares usan [Long-Term Memory for AI](https://github.com/howware/long-term-memory-for-AI) como adaptador de
memoria; instala también su skill `project-memory`. Luego dile a tu agente: *«Quiero convertir la forma en que
<hago algo> en un howware.»*

¿Prefieres empezar a mano? La [plantilla](template/) es el esqueleto completo de un howware que funciona:

```bash
python skills/howware-builder/scripts/new_howware.py --name mantenimiento-auto \
  --description "Mantenimiento del auto sin app." --out ~/dev
```

## Howwares

| Howware | Trabajo |
|---|---|
| [finanzas-personales](https://github.com/howware/finanzas-personales) | Finanzas personales: estados de cuenta, categorías que aprenden, presupuestos, pagos de tarjeta, cierre de mes, y un módulo opcional de créditos, pronóstico y plan para liquidar deudas |
| [todo](https://github.com/howware/todo) | Getting Things Done sin app: capturar, aclarar, qué hacer ahora, revisión semanal; [cómo se construyó](https://github.com/howware/todo/blob/main/docs/building.md) |
| [facturacion](https://github.com/howware/facturacion) | Facturación para independientes en México: los depósitos del banco se vuelven las facturas por emitir, verificadas contra lo timbrado, hasta la declaración y su pago; [cómo se construyó](https://github.com/howware/facturacion/blob/main/docs/building.md) |
| [arrendamiento](https://github.com/howware/arrendamiento) | Rentas para caseros: la renta revisada contra los estados de cuenta y aplicada al mes que corresponde; servicios, predial, reparaciones con garantía, el incremento y el depósito en una sola lista de pendientes; [cómo se construyó](https://github.com/howware/arrendamiento/blob/main/docs/building.md) |
| [repaso](https://github.com/howware/repaso) | Aprender y no olvidar: el agente hace las tarjetas, te pregunta unos minutos al día, califica tus respuestas dichas con tus palabras y programa cada repaso con FSRS; planes de estudio para temas largos, una racha sin culpa; [cómo se construyó](https://github.com/howware/repaso/blob/main/docs/building.md) |
| [bitacora](https://github.com/howware/bitacora) | Tu diario, como un bullet journal sin app: trackers de hábitos, notas del día con sus signos, colecciones que vas armando y una reflexión mensual donde decides qué sigue; comparte la memoria con `todo`; [cómo se construyó](https://github.com/howware/bitacora/blob/main/docs/building.md) |
| [eventos-sociales](https://github.com/howware/eventos-sociales) | Planner de eventos sociales: una boda, XV años o bautizo desde una plantilla con cuenta regresiva que la pareja o el planner ajustan; proveedores, pagos, presupuesto, padrinos, invitados, mesas y el programa del día — [cómo se construyó](https://github.com/howware/eventos-sociales/blob/main/docs/building.md) |

¿Construiste uno? Abre un pull request para agregarlo aquí; ver [CONTRIBUTING](CONTRIBUTING.md).

## Adaptadores

Los comparten los howwares; cada uno vive en su propio repositorio ([especificación §7](docs/es/especificacion.md#7-adaptadores)):

| Adaptador | Conecta con | Lo usan |
|---|---|---|
| [project-memory](https://github.com/howware/long-term-memory-for-AI) | La memoria del dueño: un almacén SQLite local, solo de agregado, con historia | Todos los howwares |
| [mxbank](https://github.com/howware/mx-bank-statement-reader) | Estados de cuenta de bancos mexicanos (PDF) → JSON anonimizado y conciliado | finanzas-personales, facturacion, arrendamiento |
| [mxsat](https://github.com/howware/mx-sat-documents) | Documentos del SAT: facturas CFDI y acuses de declaración, con los datos personales en tu computadora | facturacion |

## Límites honestos

- **Sigue habiendo código**, menos y solo donde importa la exactitud.
- **Las palabras son menos precisas que las fórmulas**, por eso el agente propone y tú apruebas, y las operaciones
  exactas viven en herramientas con pruebas.
- **Lo que ve el agente sale de tu computadora** hacia tu proveedor de IA. Cada howware debe decir qué se queda
  local, qué ve el agente y qué no puede garantizar.
- **No todo debe ser howware.** El trabajo visual, en tiempo real o de alta frecuencia sigue mereciendo una app.

## Hoja de ruta

Howware empieza con el uso personal. Después: equipos de trabajo (memoria compartida, roles, aprobaciones,
auditoría) y software empresarial con los mismos principios, explorados abiertamente. Ver el whitepaper,
[§11](docs/es/whitepaper.md#11-del-uso-personal-a-los-equipos-y-la-empresa).

## Licencia

El código (scripts de los skills, plantilla, herramientas) bajo [Apache 2.0](LICENSE). Los textos (manifiesto,
whitepaper, especificación, sitio) bajo [CC BY 4.0](LICENSE-docs.md): úsalos, tradúcelos, construye sobre ellos y
di de dónde vienen.
