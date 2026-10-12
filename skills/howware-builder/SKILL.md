---
name: howware-builder
description: Turn someone's know-how into a howware — a protocol, small exact tools, shared adapters and a memory, with the conversation as the interface, instead of an app. Use it when the person wants to automate a job, "make an app" for something they do, put their rules or process to work with AI, or create a new howware.
---

# Building a howware

A howware puts the owner's know-how to work through an AI agent: the rules in their words (protocol), only the
exact operations as code (tools), shared adapters that connect it to documents and stores, their state in a memory
they own, and the conversation as the interface. You
help the **owner** become the author. You don't take their know-how away into code.

Read the [manifesto](https://github.com/howware/howware/blob/main/MANIFESTO.md) and the
[specification](https://github.com/howware/howware/blob/main/docs/spec.md) if you haven't. `NEW` means
`python "<this skill's folder>/scripts/new_howware.py"`.

## Rules

1. **The owner is the author.** Ask, don't invent. Every rule of the job comes from them, in their words. When
   you propose wording, they approve it.
2. **Code only what must be exact.** If a wrong answer would be silent (parsing, money, dates, ids, storage), it
   goes in a tool with tests. If it's judgment, it goes in the protocol or the memory. Never move the owner's
   rules into code, and never into an adapter.
3. **No real data in the repository.** Fixtures and tests are synthetic. Never open the owner's sensitive
   documents to "see the format": read them through an adapter, or ask for a description or a made-up sample.
   When building an adapter, debug real documents only with masked shapes (`9` per digit, `X` per letter).
4. **Say when not to.** If the job is visual, real-time, high-frequency, has no judgment in it, or must be
   certified software, tell the owner a howware is not the right tool and why.
5. **Be honest about privacy.** Write the three privacy lists accurately; no absolute claims.
6. **Plan before building.** Show the plan (step 3) and wait for approval before creating files.

## 1. Interview

Ask in one or two messages, in the owner's language; skip what is already clear:

- **The job.** What do you do, how often, and what result do you need? Tell me the last time you did it.
- **The rules.** What decisions do you make? What are the exceptions? What do you check before trusting a result?
- **The inputs.** What comes in (documents, exports, things you'd just say)? Are any sensitive? Is there an
  adapter for them already?
- **The questions.** What would you ask if this worked perfectly? What should it remind you about?
- **The exact parts.** Money, dates, counts, identifiers, deadlines — where would a mistake hurt?
- **The host.** Claude Code, Codex or both? Which language?

## 2. Decide whether it fits

Apply the test: *if you removed the screens from the app you have in mind, would most of its value remain?*
Check the "when not to" list (rule 4). If it fits only partly, say which part fits.

## 3. Propose the design (wait for approval)

Present, in plain language:

| Part | Proposal |
|---|---|
| Protocol | The jobs (one workflow each), the non-negotiable rules, what to surface at the start |
| Tools | Each exact operation of this job, with its inputs and outputs |
| Adapters | The existing adapters it uses (project-memory, a statement reader, SAT documents…) and any new one it needs, as its own repository with no rules of the job |
| Memory | What is stored: records, the owner's rules as data, money in cents, high-volume record types, saved questions |
| Exactness boundary | A two-column table: what the tools do / what the agent decides |
| Privacy | What stays local, what the agent sees, what cannot be guaranteed |
| Not included | What is out of scope for the first version |

## 4. Scaffold

```bash
NEW --name <kebab-case> --description "<one sentence>" --out <folder the owner chose>
```

It creates the repository from the template: manifest, protocol skeleton, an example tool that follows the
contract, seed data, tests, conversation scenarios, installer, private-data guard and CI.

## 5. Write the protocol with the owner

Fill `skill/<name>/SKILL.md` section by section (Rules, Cold start, Workflows, Exactness boundary, Approval,
Presenting results). Use the owner's words and examples. Read each section back to them; they approve it.

## 6. Build the tools

Replace the example commands with the exact operations from the design:

- JSON on stdout; errors as JSON with documented exit codes; `--version`; no prompts; no network.
- Integer cents for money; dates at noon; stable keys for idempotent writes.
- Bulk work in one call, so the agent never transcribes records.
- Refuse unsafe input with a clear message.
- Tests with synthetic data for every command, including refusals.

### New adapters

If the job needs an adapter that doesn't exist, build it as a separate repository (specification §7): it reads
or writes one kind of document, store or service; holds no rules of the job (decisions come from the owner's data,
for example a template taken from a real document); pseudonymizes identifiers with a key the owner keeps in an
environment variable; withholds its output if a personal value would get through; has a guide for agents, a
private-data guard and synthetic tests. Check it with the owner's real documents only through its own output.

## 7. Seed the memory

Edit `seed.json`: predicates (with units), starting entities, high-volume event types and saved questions the
owner will ask often.

## 8. Privacy and manifest

Fill `howware.json` (adapters, tools, memory, the three privacy lists) and the README's privacy section with the
same content. Recommend host permissions that back the protocol's rules (for example, deny reading sensitive documents and
adapters' private stores), with their limits.

## 9. Verify

- Run the tests and the guard (commands in the generated `AGENTS.md`).
- Walk through `tests/conversations.md` with the owner: add one scenario per workflow and per refusal.
- Install the skill and try one real conversation **in the owner's own folder**, with their data, outside the
  repository.
- Review against the specification with the `howware-review` skill.

## 10. Hand over

Tell the owner, briefly: how to install, what to say first, where their data lives, how to change a rule
(say it in conversation, or edit `SKILL.md` for rules of the job), and what the howware cannot guarantee.
