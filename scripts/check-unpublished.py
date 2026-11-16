#!/usr/bin/env python3
"""Fail if AGENTS.md or CLAUDE.md would ship with the site."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("AGENTS.md", "CLAUDE.md")


def excluded_paths(config: str) -> list[str]:
    match = re.search(r"^exclude:\s*\[(.*)\]\s*$", config, re.M)
    if match is None:
        raise SystemExit("_config.yml has no exclude list")
    return [
        part.strip().strip("'\"") for part in match.group(1).split(",") if part.strip()
    ]


def main() -> int:
    excluded = excluded_paths((ROOT / "_config.yml").read_text())
    missing = [name for name in NAMES if name not in excluded]
    if missing:
        print("exclude lacks " + ", ".join(missing), file=sys.stderr)
        return 1
    site = ROOT / "_site"
    if site.is_dir():
        published = [name for name in NAMES if (site / name).is_file()]
        if published:
            print("_site contains " + ", ".join(published), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
