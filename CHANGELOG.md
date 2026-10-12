# Changelog

## Unreleased

- New howware listed: [repaso](https://github.com/howware/repaso).
- New howware listed: [arrendamiento](https://github.com/howware/arrendamiento).
- **Shared memory.** Specification 0.2 §8: several howwares may share one memory; records from an adapter are
  written in the form the adapter documents, keyed by its stable ids and without interpretation; each howware
  stores its own reading beside them and never changes them; no howware requires another only to get shared
  records. Whitepaper §4.3 explains it. Backed by project-memory 0.4.0 (a resent record gains the links it
  lacks) and mxbank 0.3.0 (`mxbank records`).
- **Adapters.** Specification 0.2: the term *adapter* (a shared program that connects howwares to documents,
  stores and services, with no rules of any job), an Architecture section (core, tools, adapters, after ports and
  adapters / clean architecture) with three rules, a new §7 for adapters, and the manifest field `adapters`
  (0.1 manifests used `requires`; both are accepted). Whitepaper 0.2 (§4.3 "Adapters: the edge"), manifesto,
  READMEs, skills and template updated to match. New adapter listed:
  [mxsat](https://github.com/howware/mx-sat-documents) for SAT documents.
- New howware listed: [facturacion](https://github.com/howware/facturacion).
- Template guard: in English like the rest of the template; blocks invoice XMLs and the `mxsat-private/`
  store; allows the SAT's public generic RFCs (found while building the `facturacion` howware).
- Whitepaper case study: hosts now say Claude Code only (Codex not yet tested), matching the manifest.
- Template: adds `LICENSE`, `SECURITY.md` and `.gitattributes`, which the specification lists and the template
  lacked (found while building the `todo` howware).
- New howware listed: [todo](https://github.com/howware/todo).

## 0.1.0 — first public version

- The term: **howware** — your know-how, put to work by AI. Manifesto in English and Spanish.
- Whitepaper "Howware: From Know-How to Done" (English, Spanish): the handoff problem, the next step after the
  spreadsheet, anatomy, principles, twelve patterns, anti-patterns, privacy model, when not to use it, comparison,
  the path to teams and enterprise, and the personal-finance case study.
- Specification 0.1: repository layout, `howware.json` manifest, protocol sections, tool contract, memory
  conventions, privacy requirements, testing and a conformance checklist.
- Skills: `howware-builder` (interview, design, scaffold, build, verify) and `howware-review` (conformance and
  privacy claims).
- Template: a working howware skeleton with an example tool, seed, tests, conversation scenarios, installer,
  private-data guard and CI.
- Site: howware.org (English and Spanish).
