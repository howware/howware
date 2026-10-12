---
name: howware-review
description: Review a howware (or a project that wants to be one) against the howware specification and principles — manifest, protocol sections, exactness boundary, tool contract, memory conventions, privacy claims and tests. Use it when asked to review, audit or check a howware, its SKILL.md, its privacy statements, or whether a project qualifies as a howware.
---

# Reviewing a howware

You check a howware against the [specification](https://github.com/howware/howware/blob/main/docs/spec.md) and
report findings. You **don't change files** unless the person asks you to apply fixes.

## Rules

1. **Read everything before judging:** `howware.json`, `README.md`, the protocol (`skill/*/SKILL.md`), every tool,
   `seed.json`, tests, CI, `AGENTS.md`.
2. **Never open the owner's real data** (documents, `.memory/`, exports) during a review. If you find real data in
   the repository, report it as the first finding, by file and type only, never by value.
3. **Verify, don't assume.** Run the tools' `--version` and `--help`, run the tests and the guard when possible,
   and try one invalid input to see the error contract.
4. **Report evidence.** Every finding names the file and line, quotes what is wrong (briefly) and proposes the
   fix.

## Checklist

### Manifest (spec §3)
- `howware.json` exists, parses, and has `howware`, `name`, `version`, `description`, `license`, `hosts`, `skill`,
  `tools`, `memory`, `privacy`.
- `requires` lists every other tool or skill the protocol calls, with minimum versions.
- `tools[].network` matches the code (search for network calls); dependencies match imports.

### Protocol (spec §4)
- Front matter `description` says which jobs it handles, in the owner's words.
- Sections present: Rules, Cold start, Workflows, Exactness boundary, Approval, Presenting results.
- **Exactness violations:** any instruction for the agent to add, convert, count, transcribe or parse by itself.
- **Rules in the wrong place:** owner-specific rules hard-coded in the protocol or the tools instead of stored in
  the memory.
- Outward-facing actions (payments, messages, publishing) require an explicit request.
- It is readable by a non-programmer.

### Tools (spec §5)
- JSON on stdout, diagnostics on stderr, errors as JSON with non-zero documented exit codes.
- No interactive prompts; no undeclared network; secrets only from environment variables.
- Idempotent writes (stable keys); refuses unsafe input; checks versions of what it depends on.
- Money in integer minor units; no floats for money; dates timezone-safe.

### Memory (spec §6)
- State lives outside the repository; history is kept (no silent overwrites).
- The owner's rules are stored as data with their words as evidence.
- High-volume record types are kept out of the session brief.

### Privacy (spec §7)
- README publishes the three lists and they match the manifest.
- **Overclaims:** flag absolute language ("never", "100 %", "nothing leaves", "no data", "completely private")
  unless strictly true for the whole system, including the AI provider. Propose precise wording.
- Sensitive documents are processed locally before the agent sees anything.
- A private-data guard runs in CI; fixtures are synthetic.

### Tests (spec §8)
- Tool tests with synthetic data, including refusals; CI runs them.
- `tests/conversations.md` covers each workflow and each refusal.

## Report

1. **Verdict:** conforming howware / conforming with findings / not yet a howware — one sentence why.
2. **Findings**, most severe first: real data or privacy overclaims, then exactness violations, then contract and
   memory issues, then documentation. Each with file:line, evidence and fix.
3. **What is done well** — briefly, so it is kept.
4. **Next steps** in order.
