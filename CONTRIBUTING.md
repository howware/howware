# Contributing

Howware is an open idea. Contributions in English or Spanish are welcome.

## Ways to contribute

- **Add a howware to the list.** Open a pull request adding a row to the "Howwares" table in both READMEs. It
  should have a `howware.json`, state its privacy limits honestly, and pass a `howware-review`.
- **Add an adapter.** A shared program that connects howwares to a kind of document, store or service
  (specification §7). It lives in its own repository; open a pull request adding it to the "Adapters" table.
- **Counter-examples.** Jobs where howware failed or an app was clearly better make the whitepaper's "when not to"
  section stronger. Open an issue.
- **Patterns.** Found a pattern or anti-pattern while building a howware? Propose it with the failure it solved.
- **Translations** of the manifesto and the whitepaper, under `docs/<language>/`.
- **The template and skills.** Improvements must keep the template standard-library only and its tests passing.

## Rules

- **No real personal data**, ever: not in code, fixtures, issues or examples. CI runs a guard over every file.
- Keep the texts precise about limits: no absolute claims about privacy or capability.
- Code is Apache 2.0; texts are CC BY 4.0 (see [LICENSE-docs.md](LICENSE-docs.md)). By contributing you agree to
  license your contribution the same way.

## Development

```bash
git clone https://github.com/howware/long-term-memory-for-AI ../long-term-memory-for-AI
python -m unittest discover -s tests -v
git ls-files -z | xargs -0 python tools/check_private_data.py
```
