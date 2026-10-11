# Howware Specification

*Version 0.1 · [Leer en español](es/especificacion.md)*

What a howware is made of, so that anyone can build one, review one, or tell whether something is one. The key
words **MUST**, **SHOULD** and **MAY** are used as in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## 1. Terms

| Term | Meaning |
|---|---|
| **Howware** | Know-how put to work by an AI agent: a protocol, tools and a memory convention, with the conversation as the interface |
| **Owner** | The person whose know-how and data the howware serves |
| **Host** | The agent runtime that loads the protocol and runs the tools (Claude Code, Codex, …). Not part of the howware |
| **Protocol** | The know-how in natural language (a skill file) |
| **Tool** | A small program that performs an exact operation |
| **Memory** | Where the owner's state, rules and history are stored |

## 2. Repository layout

A howware SHOULD be a repository with this layout (the [template](../template/) implements it):

```text
<name>/
  howware.json                 manifest (§3)
  README.md                    what it does, install, privacy (§7), limits
  skill/<name>/SKILL.md        protocol (§4)
  skill/<name>/scripts/        tools (§5) and seed data for the memory
  tests/                       tool tests with synthetic data; conversation scenarios
  tools/install_skill.py       installs the skill into a host
  tools/check_private_data.py  CI guard against real data (§7)
  .github/workflows/ci.yml     runs the guard and the tests
  AGENTS.md · CLAUDE.md        rules for whoever develops the howware with AI
  SECURITY.md · LICENSE
```

## 3. Manifest: `howware.json`

Every howware MUST include a manifest at the repository root:

```json
{
  "howware": "0.1",
  "name": "finanzas-personales",
  "version": "0.1.0",
  "description": "Personal finances without an app: statements, categories, budgets, card payments.",
  "license": "Apache-2.0",
  "languages": ["es"],
  "hosts": ["claude-code", "codex"],
  "skill": "skill/finanzas-personales",
  "requires": [
    {"name": "mxbank", "version": ">=0.2.0", "url": "https://github.com/proteo5/mx-bank-statement-reader"},
    {"name": "project-memory", "version": ">=0.3.0", "url": "https://github.com/proteo5/long-term-memory-for-AI"}
  ],
  "tools": [{"name": "fin.py", "network": false, "dependencies": []}],
  "memory": {"kind": "local-sqlite", "append_only": true, "seed_version": "2"},
  "privacy": {
    "stays_local": ["statement PDFs", "names, tax ids, card and account numbers", "the memory file"],
    "agent_sees": ["merchant, amount and date of transactions", "pseudonyms", "what the owner types"],
    "cannot_guarantee": ["automatic anonymization is not infallible", "the no-PDF rule is an instruction to the agent"]
  }
}
```

| Field | Required | Meaning |
|---|---|---|
| `howware` | MUST | Version of this specification |
| `name`, `version`, `description`, `license` | MUST | Identity; `version` follows semantic versioning |
| `languages` | SHOULD | Languages the protocol is written for (the agent answers in the owner's language either way) |
| `hosts` | MUST | Hosts it has been tested on |
| `skill` | MUST | Path to the protocol folder |
| `requires` | MUST if any | Other tools or skills, with minimum versions |
| `tools` | MUST | Each tool, whether it uses the network, and its third-party dependencies |
| `memory` | MUST | Where state lives and whether history is kept |
| `privacy` | MUST | The three lists of §7, in plain language |

## 4. Protocol

The protocol MUST be a skill file (`SKILL.md`) with front matter (`name`, `description`) that the host uses to
decide when to load it. The `description` MUST say what jobs it handles in words the owner would use.

The protocol MUST include:

1. **Rules (non-negotiable).** What the agent must always and never do, starting with privacy and outward-facing
   actions.
2. **Cold start.** What to run at the beginning of a session and what to surface first (pending items).
3. **Workflows.** One section per job: when it applies, which tools to run, what to show, what to ask.
4. **The exactness boundary.** Which operations the agent MUST delegate to tools (arithmetic, parsing, writing
   state) and never do itself.
5. **Approval.** Which decisions the owner approves, and how proposals are presented (in batch, with the owner's
   words stored as evidence).
6. **Presenting results.** Format, language, what is data and what is estimate.

The protocol SHOULD be readable by the owner: plain sentences, examples in their words, no code beyond the
commands to run. Rules of the job live in the protocol; rules the owner teaches live in the memory (§6).

## 5. Tools

Each tool:

- MUST be a command-line program the host can run, with `--help` and `--version`.
- MUST write its result as JSON on standard output and diagnostics on standard error.
- MUST report errors as JSON (`{"ok": false, "error": {...}}`) with a non-zero, documented exit code. It MUST NOT
  prompt interactively.
- MUST be deterministic for the same input and state.
- MUST NOT use the network unless the manifest declares it, and SHOULD have no third-party dependencies.
- MUST take secrets only from environment variables, never from arguments or files in the repository.
- MUST make writes idempotent: repeating the same operation does not duplicate state.
- MUST refuse input that would corrupt state or leak personal data, and say why.
- SHOULD verify the versions of the tools and memory it depends on.
- SHOULD do bulk work in one call, so the agent never transcribes records.

## 6. Memory

- State MUST live where the owner decides, outside the howware's repository.
- History SHOULD be kept: changes close, correct or void records with a reason; they don't silently overwrite.
- Money MUST be stored in minor units (integer cents) with a declared unit. Other exact quantities likewise.
- Records SHOULD have stable keys derived from their source, so imports are idempotent.
- Calendar dates SHOULD be stored at noon local time.
- Rules the owner teaches (categories, budgets, names) MUST be stored as data in the memory, with the owner's
  words as evidence, not as edits to code.
- High-volume records SHOULD be kept out of the session brief.
- Repeated questions SHOULD be saved as named, parameterized queries.

## 7. Privacy

A howware MUST:

- Publish the three lists of its manifest in its README: **what is designed to stay local**, **what the agent
  sees**, **what it cannot guarantee**. Claims MUST be accurate; absolute claims ("never", "100 %") MUST be
  avoided unless strictly true for the whole system, including the AI provider.
- Process sensitive documents with local tools before the agent sees anything, when the job involves them.
- Run a guard in CI that rejects documents, databases and personal identifiers in versioned files.
- Use only synthetic data in tests and fixtures.

A howware SHOULD recommend host permissions that back its rules (for example, denying file reads of sensitive
document types) and state their limits.

## 8. Testing

- Tools MUST have automated tests with synthetic data, run in CI.
- A howware SHOULD include conversation scenarios (`tests/conversations.md`): what the owner says, what the agent
  must do (which tools, what it must ask, what it must refuse). Until automated, they are checked by hand before
  each release.
- CI SHOULD install the skill into a temporary host folder and run its tools end to end.

## 9. Versioning

- `version` follows [semantic versioning](https://semver.org). Changing seed data that affects existing memories
  SHOULD bump its own seed version.
- A `CHANGELOG.md` SHOULD record user-visible changes, including changes to the protocol's behavior.

## 10. Conformance checklist

A project is a conforming howware when:

- [ ] It has a valid `howware.json`.
- [ ] Its protocol has rules, cold start, workflows, exactness boundary, approval and presentation sections.
- [ ] Every exact operation is done by a tool; the agent is told never to transcribe or calculate.
- [ ] Its tools follow §5 (JSON output, exit codes, no prompts, no undeclared network, idempotent).
- [ ] The owner's rules live in the memory, not in code.
- [ ] Its README states what stays local, what the agent sees and what it cannot guarantee, without absolute
      claims.
- [ ] CI runs a private-data guard and the tool tests on synthetic data.

The [`howware-review`](../skills/howware-review/SKILL.md) skill checks this list.

---

*Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*
