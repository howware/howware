---
name: __NAME__
description: __DESCRIPTION__ Use it when the person asks to <list the jobs, in the words they would use>.
---

# __NAME__

<!-- A howware protocol: the know-how, in plain words. Write it so the owner can read and change it.
     Rules of the job go here. Rules the owner teaches (categories, limits, names) go in the memory as data.
     Sections marked REQUIRED follow the howware specification §5. -->

`TOOL` = `python "<this skill's folder>/scripts/__NAME__.py"`; `MEM` = the project-memory helper.
Run both from the owner's folder. All output is JSON.

## Rules (non-negotiable) — REQUIRED

1. <Privacy rule: what the agent must never open, read or send. Example: never open the original documents;
   only the extraction tool reads them.>
2. Never transcribe records by hand and never do arithmetic yourself: use `TOOL`. Report the totals it returns.
3. Never invent what you don't know (a merchant, a person, a rule): ask.
4. Rules and decisions are the owner's: propose, wait for approval, store their literal words with `--source`.
5. Nothing outward-facing (payments, messages, publishing) without an explicit request.
6. You inform and organize; you are not a licensed advisor.

## Cold start — REQUIRED

1. `MEM brief --format text` (or the one the session hook injected).
2. If there is no memory: follow "Start the memory" of project-memory, then `TOOL setup --by person:<id>`.
3. Surface what is pending first.

## Workflows — REQUIRED

### <Job 1, in the owner's words>

- When: <what the owner says>.
- Run: `TOOL record --amount 180 --description "..." --by person:<id> --source "<their words>"`.
- Show: <what to present>. Ask: <what to confirm>.

### <Job 2>

- ...

## Exactness boundary — REQUIRED

| The tool does | You do |
|---|---|
| Parsing, amounts, dates, identifiers, writing and querying the memory | Choosing the tool, explaining results, asking when unsure |

Exit codes of `TOOL`: 0 ok · 2 invalid input (explain and ask) · 3 memory problem (say what to install or fix).

## Approval — REQUIRED

- Group everything new into one proposal; one message, grouped, with an "unknown" group for what you can't tell.
- On approval, store the rule in the memory with the owner's literal words as evidence.

## Presenting results — REQUIRED

- Lead with the key figures. Amounts with thousands separators and two decimals.
- Use the owner's language. Mark clearly what is data and what is estimate. If something doesn't add up, say so.
