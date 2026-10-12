<h1 align="center">Howware</h1>

<p align="center">
  <b>From know-how to done.</b><br>
  Your know-how, put to work by AI — no app to build, no one to hand it off to, no waiting.
</p>

<p align="center">
  <a href="https://github.com/howware/howware/actions/workflows/ci.yml"><img src="https://github.com/howware/howware/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/spec-0.1-blue" alt="Spec 0.1">
  <img src="https://img.shields.io/badge/code-Apache%202.0-green" alt="Code: Apache 2.0">
  <img src="https://img.shields.io/badge/texts-CC%20BY%204.0-green" alt="Texts: CC BY 4.0">
</p>

<p align="center">
  <a href="https://howware.org">howware.org</a> ·
  <a href="MANIFESTO.md">Manifesto</a> ·
  <a href="docs/whitepaper.md">Whitepaper</a> ·
  <a href="docs/spec.md">Specification</a> ·
  <a href="README.es.md">Español</a>
</p>

> **Howware** — your know-how, put to work by AI. You state the rules in your own words; an AI agent follows
> them, with a few exact tools and a memory you own. No app to build, no one to hand it off to, no waiting.

*Hardware runs it. Software executes it. Howware knows how.*

---

## Why

The person who knows how something should work is almost never the person who builds it. They explain the rules
to someone who codes; meaning gets lost; every new rule makes the code more complicated; every change waits weeks
or months. And around the rules, someone still has to build an app — screens, forms, a backend — that everyone
else has to learn.

The **spreadsheet** was the first time people who don't program could put their own know-how to work without
asking anyone. **Howware is the next step**: rules in your own words instead of formulas, a conversation instead
of a grid, tools that read your documents instead of copy and paste, and an AI agent doing the work.

## What a howware is made of

| Part | What it is |
|---|---|
| **Protocol** | Your know-how in plain words: steps, criteria, rules, what to ask, what never to do |
| **Tools** | Small programs for whatever must be exact: reading documents, money, dates, storage |
| **Memory** | Your data and the rules you teach, in a place you own, with history |
| **Conversation** | The only interface |

```text
› Yesterday I spent 180 on lunch in cash.            → recorded, with your words as evidence
› OXXO is groceries, not convenience.                → a rule, effective now, for the whole history
› How am I doing with my grocery budget?             → $3,180.40 of $4,000.00 (79 %)
```

Read the [manifesto](MANIFESTO.md) for the nine principles, and the [whitepaper](docs/whitepaper.md) for the
patterns, the privacy model, the limits and **when not to use howware**.

## Build one

This repository includes two skills for Claude Code and Codex:

| Skill | Does |
|---|---|
| [`howware-builder`](skills/howware-builder/SKILL.md) | Interviews you about your job and builds a howware with you: design, protocol, tools, memory, tests |
| [`howware-review`](skills/howware-review/SKILL.md) | Reviews a howware against the specification, including privacy claims |

```bash
git clone https://github.com/howware/howware
python howware/tools/install_skills.py                              # Claude Code
python howware/tools/install_skills.py --target-dir ~/.codex/skills  # Codex
```

The tools a howware creates use [Long-Term Memory for AI](https://github.com/howware/long-term-memory-for-AI)
as their memory; install its `project-memory` skill too. Then tell your agent: *"I want to turn the way I
<do something> into a howware."*

Prefer to start by hand? The [template](template/) is a complete, working howware skeleton:

```bash
python skills/howware-builder/scripts/new_howware.py --name car-maintenance \
  --description "Car maintenance without an app." --out ~/dev
```

## Howwares

| Howware | Job |
|---|---|
| [finanzas-personales](https://github.com/howware/finanzas-personales) | Personal finances: bank statements, categories that learn, budgets, card payments, monthly close |
| [todo](https://github.com/howware/todo) | Getting Things Done without an app: capture, clarify, what to do now, weekly review — [how it was built](https://github.com/howware/todo/blob/main/docs/building.md) |

Built one? Open a pull request to add it here — see [CONTRIBUTING](CONTRIBUTING.md).

## Honest limits

- **There is still code** — less, and only where exactness matters.
- **Words are less precise than formulas**, so the agent proposes and you approve, and exact operations live in
  tested tools.
- **What the agent sees leaves your computer** for your AI provider. Each howware must say what stays local, what
  the agent sees and what it cannot guarantee.
- **Not everything should be howware.** Visual, real-time and high-frequency work still deserve an app.

## Roadmap

Howware starts with personal use. Next: teams (shared memory, roles, approvals, audit) and enterprise software
under the same principles — explored in the open. See the whitepaper,
[§11](docs/whitepaper.md#11-from-personal-to-teams-and-enterprise).

## Repository

```text
MANIFESTO.md · MANIFIESTO.md    the definition and principles
docs/whitepaper.md · docs/es/   the whitepaper (English, Spanish)
docs/spec.md · docs/es/         the specification
skills/                          howware-builder, howware-review
template/                        a working howware skeleton
```

## License

Code (skills' scripts, template, tools) under [Apache 2.0](LICENSE). Texts (manifesto, whitepaper,
specification; the site in [howware.github.io](https://github.com/howware/howware.github.io)) under [CC BY 4.0](LICENSE-docs.md): use them, translate them, build on them, and say where
they came from.
