# __NAME__

> A [howware](https://howware.org): __DESCRIPTION__

<!-- Write this README for the owner first: what they can ask, what it needs, how to install, what happens with
     their data. Keep the three privacy lists accurate; avoid absolute claims. -->

## What you can ask

| You want | Say |
|---|---|
| <job 1> | «...» |
| <job 2> | «...» |

## How it works

- **Protocol:** [`skill/__NAME__/SKILL.md`](skill/__NAME__/SKILL.md) — the know-how, in plain words. Read it; change it.
- **Tools:** [`__NAME__.py`](skill/__NAME__/scripts/__NAME__.py) — only the operations that must be exact.
- **Memory:** [Long-Term Memory for AI](https://github.com/proteo5/long-term-memory-for-AI) — your data and the
  rules you teach, in a local file.

## Install

```bash
python tools/install_skill.py                                       # Claude Code
python tools/install_skill.py --target ~/.codex/skills/__NAME__      # Codex
```

Requires the `project-memory` skill (>= 0.3.0). Then open your agent in a folder of your choice and say what you
need.

## Privacy

| Designed to stay on your computer | What the AI agent sees |
|---|---|
| <...> | <...> |

**What we cannot guarantee:** <state the limits honestly>.

## Development

```bash
python -m unittest discover -s tests -v
git ls-files -z | xargs -0 python tools/check_private_data.py
```

Tests use synthetic data only. See [AGENTS.md](AGENTS.md).

## License

Apache 2.0.
