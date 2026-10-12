# The Howware Manifesto

*[Leer en español](MANIFIESTO.md)*

> **Howware** /ˈhaʊ.wɛr/ — your know-how, put to work by AI. You state the rules in your own words; an AI agent
> follows them, with a few exact tools and a memory you own. No app to build, no one to hand it off to, no
> waiting.

**From know-how to done.**
No app. No handoff. No waiting. Your rules, in your words, working today.

*Hardware runs it. Software executes it. Howware knows how.*

---

## The handoff problem

The person who knows how something should work — the rules, the exceptions, the judgment — is almost never the
person who builds it. They have to explain it to someone else, who translates it into code. Meaning gets lost
in translation. Every new rule makes the code more complicated. Every change waits in a queue, and what you need
this week arrives in weeks or months, if it arrives.

Applications made that handoff unavoidable: the only way to put know-how to work was to have someone build a
program around it.

## The next step after the spreadsheet

There was one big exception. **The spreadsheet** was the first time people who don't program could put their
own know-how to work without asking anyone: the rules were formulas, the interface was a grid, and a change took
effect the moment you typed it. That is why spreadsheets run so much of the world.

Howware is the next step:

| | Spreadsheet | Howware |
|---|---|---|
| Rules are written as | Formulas | Your own words |
| The interface is | A grid | A conversation |
| Data gets in by | Typing or pasting | Tools that read your documents |
| Who does the work | You, cell by cell | An AI agent, following your rules |
| A change takes effect | When you type it | In the next conversation |

## Anatomy

Every howware has five parts:

| Part | What it is | Example (personal finance) |
|---|---|---|
| **Protocol** | The know-how in natural language: steps, criteria, rules, what to ask and what never to do | `SKILL.md`: how to import, how to propose categories, what is not spending |
| **Tools** | Small, deterministic programs for the exact operations of the job | Add cents, budgets, monthly reports |
| **Adapters** | Shared programs that connect howwares to documents and stores, removing personal data at the edge | Read a bank statement without the owner's identity; the memory store |
| **Memory** | The person's state, owned by them, with history | A local, append-only SQLite file |
| **Conversation** | The only interface | "How am I doing with my grocery budget?" |

The agent that runs it — Claude Code, Codex or another host — is not part of the howware, just as the browser is
not part of a web page.

## Principles

1. **The person with the know-how is the author.** Rules live in text that the person can read and change. No
   translation to a developer, no queue: a new rule works in the next conversation.

2. **The conversation is the interface.** No screens to build, no menus to learn. The person says what they need;
   the agent asks when something is unclear.

3. **Code only what must be exact.** Reading documents, arithmetic with money, dates, identifiers and storage
   belong in small tools that can be tested. Everything that is judgment belongs in the protocol.

4. **The agent decides; the tools do the work.** The agent never transcribes hundreds of records by hand and
   never does the arithmetic itself. Tools move and compute the data; the agent chooses, explains and asks.

5. **The person approves.** The agent proposes; the person decides — rules, categories, anything that will shape
   future answers. Nothing outward-facing (payments, messages, publishing) happens without an explicit request.

6. **The person owns the data.** State lives where the person decides, in a format they can read, copy and take
   elsewhere. History is kept: changes close or correct records, they don't silently overwrite them.

7. **Privacy by design, stated honestly.** Minimize what reaches the model: process sensitive documents locally
   and give the agent only what it needs. Then say plainly what you cannot guarantee. A privacy promise that
   isn't true is worse than none.

8. **Small enough to audit.** The protocol is a text file. Tools and adapters are short, with few dependencies.
   Anyone should be able to read the whole thing and verify what it claims.

9. **Composable and open.** Each adapter is useful on its own, shared by many howwares, and replaceable. A howware is a combination of open
   pieces, not a sealed product.

## Honest limits

- **There is still code** — less of it, and only where exactness matters. It changes rarely; the rules, which
  change often, don't need it.
- **Words are less precise than formulas.** That is why the agent proposes and the person approves, why exact
  operations live in tested tools, and why every howware should state its limits.
- **Not everything should be howware.** Visual, real-time or high-frequency work still deserves an app. See
  [when not to use howware](docs/whitepaper.md#when-not-to-use-howware).

## What howware is not

- **Not vibe coding.** Vibe coding uses AI to write an app's code; you still end up with an app and a developer
  workflow. Howware means there is no app to write.
- **Not a chatbot.** A chatbot answers from what it knows. A howware has a protocol, exact tools and the
  person's memory, and does a specific job reliably.
- **Not no-code.** No-code builds an app visually. Howware doesn't build one.

## The first howware

[finanzas-personales](https://github.com/howware/finanzas-personales) handles personal finances — importing
bank statements, categories that learn, budgets, card payments, monthly close — with no app: a protocol for
Claude Code or Codex, a bank statement reader that removes personal data on the person's computer, and a local
memory.

---

*Howware is an open idea. This manifesto is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use it, translate it, build on it, and say where it
came from. — [howware.org](https://howware.org)*
