# AGENTS.md

Rules for AI agents (and people) developing this repository.

- **No real personal data**, ever. Fixtures are synthetic; valid-looking identifiers in tests are built in code.
- Texts must be precise about limits: no absolute claims about privacy or capability.
- English is canonical; every change to `MANIFESTO.md`, `docs/whitepaper.md` or `docs/spec.md` is mirrored in
  `MANIFIESTO.md`, `docs/es/whitepaper.md` or `docs/es/especificacion.md` in the same change, and in the site
  ([howware/howware.github.io](https://github.com/howware/howware.github.io)) when it affects it.
- The template stays standard-library only and must pass its own tests after scaffolding (`tests/test_repo.py`).

```bash
git clone https://github.com/howware/long-term-memory-for-AI ../long-term-memory-for-AI
python -m unittest discover -s tests -v
git ls-files -z | xargs -0 python tools/check_private_data.py
```
