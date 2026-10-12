"""__NAME__ — tool of the __NAME__ howware.

Commands (JSON on stdout, diagnostics on stderr, documented exit codes):
  setup    load seed.json into the memory (predicates, starting entities, saved queries)
  record   record one item, idempotently (example of an exact write)
  report   totals for a period, computed by the memory (example of an exact read)

Contract (howware spec §6): no network, no interactive prompts, secrets only from environment variables,
idempotent writes, money in integer cents, refuse unsafe input with a clear error. Standard library only.

Replace the example commands with the exact operations your howware needs. Keep judgment out of this file:
rules of the job go in SKILL.md, rules the owner teaches go in the memory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path
from typing import Any

__version__ = "0.1.0"
HERE = Path(__file__).resolve().parent
SEED = HERE / "seed.json"
MIN_MEMORY = (0, 3, 0)

# Exit codes (document them in SKILL.md)
OK, BAD_INPUT, MEMORY_ERROR = 0, 2, 3


class ToolError(Exception):
    def __init__(self, message: str, code: int = BAD_INPUT):
        super().__init__(message)
        self.code = code


# -- memory (project-memory helper) -------------------------------------------------
def find_helper(explicit: str | None) -> Path:
    for c in (explicit, os.environ.get("HOWWARE_MEMORY_HELPER"),
              Path.home() / ".claude/skills/project-memory/scripts/memory.py",
              Path.home() / ".codex/skills/project-memory/scripts/memory.py"):
        if c and Path(c).is_file():
            return Path(c)
    raise ToolError("project-memory is not installed (or pass --mem / HOWWARE_MEMORY_HELPER).", MEMORY_ERROR)


class Memory:
    def __init__(self, helper: Path, db: str | None):
        self.helper, self.db = helper, db

    def run(self, *args: str, stdin: dict | None = None) -> Any:
        cmd = [sys.executable, str(self.helper)] + (["--db", self.db] if self.db else []) + list(args)
        proc = subprocess.run(cmd, input=json.dumps(stdin, ensure_ascii=False) if stdin is not None else None,
                              capture_output=True, text=True, encoding="utf-8")
        if proc.returncode != 0:
            raise ToolError(f"memory {args[0]} failed: {(proc.stderr or proc.stdout).strip()[-600:]}", MEMORY_ERROR)
        return json.loads(proc.stdout) if proc.stdout.strip() else None

    def check_version(self) -> None:
        out = subprocess.run([sys.executable, str(self.helper), "--version"], capture_output=True, text=True).stdout
        parts = [int(p) for p in out.split()[-1].split(".")[:3]] if out.strip() else [0]
        if tuple(parts) < MIN_MEMORY:
            raise ToolError(f"project-memory >= {'.'.join(map(str, MIN_MEMORY))} is required (found: {out.strip()}).",
                            MEMORY_ERROR)


# -- exact helpers ----------------------------------------------------------------
def cents(value: str) -> int:
    """Decimal text to integer cents. Never use floats for money."""
    try:
        return int((Decimal(str(value)) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError) as error:
        raise ToolError(f"Not an amount: {value!r}") from error


def money(c: int | None) -> str | None:
    if c is None:
        return None
    return f"{'-' if c < 0 else ''}${abs(c) // 100:,}.{abs(c) % 100:02d}"


def at_noon(day: str, tz: str) -> str:
    """Calendar dates are stored at noon local time so they never shift a day in another zone."""
    datetime.strptime(day, "%Y-%m-%d")
    return f"{day}T12:00:00{tz}"


def stable_key(prefix: str, *parts: str) -> str:
    """Same inputs, same key: repeating a write never duplicates it."""
    return f"{prefix}_" + hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:16]


def local_offset() -> str:
    z = datetime.now().astimezone().strftime("%z")
    return f"{z[:3]}:{z[3:]}"


def source(by: str, content: str, kind: str = "user_statement") -> dict:
    return {"type": kind, "content": content, "provided_by": by, "captured_at": "now"}


# -- commands -----------------------------------------------------------------------
def cmd_setup(mem: Memory, args) -> dict:
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    result = mem.run("write", stdin={"source": source(args.by, f"__NAME__ seed v{seed['seed_version']}", "helper_command"),
                                     "performed_by": args.by,
                                     "predicates": [{**p, "distinct_from_similar": True} for p in seed["predicates"]],
                                     "entities": seed.get("entities", [])})
    for event_type in seed.get("high_volume_event_types", []):
        mem.run("define-event-type", "--type", event_type, "--high-volume", "--by", args.by)
    return {"ok": True, "seed_version": seed["seed_version"], "warnings": result.get("warnings", [])}


def cmd_record(mem: Memory, args) -> dict:
    amount = cents(args.amount)
    day = args.date or date.today().isoformat()
    key = stable_key("ITEM", day, str(amount), args.description.strip().lower(), args.nonce or "")
    result = mem.run("write", stdin={
        "source": source(args.by, args.source or args.description), "performed_by": args.by,
        "events": [{"key": key, "type": "item", "occurred_at": at_noon(day, args.tz),
                    "summary": args.description[:160], "attributes": {"amount": amount}}]})
    created = bool(result.get("events", {}).get("created"))
    return {"ok": True, "key": key, "amount": money(amount), "created": created}


def cmd_report(mem: Memory, args) -> dict:
    agg = mem.run("aggregate", "--event-type", "item", "--measure", "sum:amount", "--by", "period:month",
                  "--since", args.since, "--until", args.until)
    return {"ok": True, "unit": agg.get("unit"),
            "months": [{"month": g["period:month"], "total": money(g["value"]), "items": g["rows"]}
                       for g in agg["groups"]]}


# -- CLI -----------------------------------------------------------------------------
def main() -> None:
    p = argparse.ArgumentParser(prog="__NAME__.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"__NAME__.py {__version__}")
    p.add_argument("--mem", help="Path to project-memory's memory.py")
    p.add_argument("--db", help="Path to the memory (default: the current project's)")
    p.add_argument("--tz", default=os.environ.get("HOWWARE_TZ") or local_offset(), help="UTC offset, e.g. --tz=-06:00")
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("setup")
    s.add_argument("--by", required=True, help="person:<id> of the owner")
    s = sub.add_parser("record")
    s.add_argument("--amount", required=True)
    s.add_argument("--description", required=True)
    s.add_argument("--date", help="YYYY-MM-DD (today by default)")
    s.add_argument("--nonce", help="Tells apart two identical records on the same day")
    s.add_argument("--by", required=True)
    s.add_argument("--source", help="The owner's literal words")
    s = sub.add_parser("report")
    s.add_argument("--since", required=True, help="YYYY-MM-DD")
    s.add_argument("--until", required=True, help="YYYY-MM-DD (excluded)")
    args = p.parse_args()
    commands = {"setup": cmd_setup, "record": cmd_record, "report": cmd_report}
    try:
        mem = Memory(find_helper(args.mem), args.db)
        mem.check_version()
        result, code = commands[args.command](mem, args), OK
    except ToolError as error:
        result, code = {"ok": False, "error": {"code": error.code, "message": str(error)}}, error.code
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(code)


if __name__ == "__main__":
    main()
