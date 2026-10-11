# El manifiesto howware

*[Read in English](MANIFESTO.md)*

> **Howware** /jáu-uer/ — tu saber hacer, puesto a trabajar con IA. Dices las reglas con tus palabras; un agente
> de IA las sigue, con unas cuantas herramientas exactas y una memoria que es tuya. Sin app que construir, sin
> intermediarios, sin esperas.

**Del saber hacer a hecho.**
Sin app. Sin intermediarios. Sin esperas. Tus reglas, en tus palabras, funcionando hoy.

*El hardware lo corre. El software lo ejecuta. El howware sabe cómo.*

---

## El problema de los intermediarios

Quien sabe cómo debe funcionar algo —las reglas, las excepciones, el criterio— casi nunca es quien lo construye.
Tiene que explicárselo a alguien más, que lo traduce a código. En la traducción se pierde sentido. Cada regla
nueva complica más el código. Cada cambio espera su turno, y lo que necesitas esta semana llega en semanas o
meses, si llega.

Las aplicaciones hicieron inevitable ese paso: la única forma de poner un saber hacer a trabajar era que alguien
construyera un programa alrededor de él.

## El siguiente paso después de la hoja de cálculo

Hubo una gran excepción. **La hoja de cálculo** fue la primera vez que personas que no programan pudieron poner
su propio saber hacer a trabajar sin pedírselo a nadie: las reglas eran fórmulas, la interfaz era una cuadrícula
y un cambio surtía efecto en el momento de escribirlo. Por eso las hojas de cálculo mueven buena parte del mundo.

El howware es el siguiente paso:

| | Hoja de cálculo | Howware |
|---|---|---|
| Las reglas se escriben como | Fórmulas | Tus propias palabras |
| La interfaz es | Una cuadrícula | Una conversación |
| Los datos entran | Escribiendo o pegando | Con herramientas que leen tus documentos |
| Quién hace el trabajo | Tú, celda por celda | Un agente de IA, siguiendo tus reglas |
| Un cambio surte efecto | Al escribirlo | En la siguiente conversación |

## Anatomía

Todo howware tiene cuatro partes:

| Parte | Qué es | Ejemplo (finanzas personales) |
|---|---|---|
| **Protocolo** | El saber hacer en lenguaje natural: pasos, criterios, reglas, qué preguntar y qué nunca hacer | `SKILL.md`: cómo importar, cómo proponer categorías, qué no es gasto |
| **Herramientas** | Programas pequeños y deterministas para lo que debe ser exacto | Leer un estado de cuenta, sumar centavos, mantener ids estables |
| **Memoria** | El estado de la persona, suyo, con historia | Un archivo SQLite local que solo agrega |
| **Conversación** | La única interfaz | «¿Cómo voy con el presupuesto de súper?» |

El agente que lo ejecuta —Claude Code, Codex u otro— no es parte del howware, igual que el navegador no es parte
de una página web.

## Principios

1. **Quien tiene el saber hacer es el autor.** Las reglas viven en un texto que la persona puede leer y cambiar.
   Sin traducción a un programador, sin fila de espera: una regla nueva funciona en la siguiente conversación.

2. **La conversación es la interfaz.** No hay pantallas que construir ni menús que aprender. La persona dice lo
   que necesita; el agente pregunta cuando algo no está claro.

3. **Programa solo lo que debe ser exacto.** Leer documentos, la aritmética con dinero, las fechas, los
   identificadores y el almacenamiento van en herramientas pequeñas que se pueden probar. Todo lo que es criterio
   va en el protocolo.

4. **El agente decide; las herramientas hacen el trabajo.** El agente nunca transcribe cientos de registros a mano
   ni hace las cuentas él mismo. Las herramientas mueven y calculan los datos; el agente elige, explica y pregunta.

5. **La persona aprueba.** El agente propone; la persona decide: reglas, categorías, todo lo que dará forma a las
   respuestas futuras. Nada hacia afuera (pagos, mensajes, publicaciones) ocurre sin una petición explícita.

6. **Los datos son de la persona.** El estado vive donde la persona decide, en un formato que puede leer, copiar y
   llevarse. La historia se conserva: los cambios cierran o corrigen registros, no los sobrescriben en silencio.

7. **Privacidad por diseño, dicha con honestidad.** Minimiza lo que llega al modelo: procesa los documentos
   sensibles localmente y dale al agente solo lo que necesita. Luego di con claridad lo que no puedes garantizar.
   Una promesa de privacidad que no es cierta es peor que ninguna.

8. **Tan pequeño que se pueda auditar.** El protocolo es un archivo de texto. Las herramientas son cortas, con
   pocas o ninguna dependencia. Cualquiera debería poder leerlo todo y comprobar lo que promete.

9. **Componible y abierto.** Cada herramienta sirve por sí sola y se puede reemplazar. Un howware es una
   combinación de piezas abiertas, no un producto sellado.

## Límites honestos

- **Sigue habiendo código**, menos y solo donde importa la exactitud. Cambia poco; las reglas, que cambian mucho,
  no lo necesitan.
- **Las palabras son menos precisas que las fórmulas.** Por eso el agente propone y la persona aprueba, las
  operaciones exactas viven en herramientas con pruebas, y todo howware debe decir cuáles son sus límites.
- **No todo debe ser howware.** El trabajo visual, en tiempo real o de alta frecuencia sigue mereciendo una app.
  Ver [cuándo no conviene howware](docs/es/whitepaper.md#cuándo-no-conviene-howware).

## Lo que howware no es

- **No es vibe coding.** Vibe coding usa IA para escribir el código de una app; al final sigues teniendo una app
  y un flujo de desarrollo. Howware significa que no hay app que escribir.
- **No es un chatbot.** Un chatbot responde con lo que sabe. Un howware tiene un protocolo, herramientas exactas y
  la memoria de la persona, y hace un trabajo específico de forma confiable.
- **No es no-code.** No-code construye una app de forma visual. Howware no construye ninguna.

## El primer howware

[finanzas-personales](https://github.com/proteo5/finanzas-personales) lleva las finanzas personales —importar
estados de cuenta, categorías que aprenden, presupuestos, pagos de tarjeta, cierre de mes— sin app: un protocolo
para Claude Code o Codex, un lector de estados de cuenta que elimina los datos personales en la computadora de la
persona y una memoria local.

---

*Howware es una idea abierta. Este manifiesto está bajo licencia
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es): úsalo, tradúcelo, construye sobre él y di de
dónde viene. — [howware.org](https://howware.org)*
