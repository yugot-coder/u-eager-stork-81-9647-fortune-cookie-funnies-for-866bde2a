#!/usr/bin/env python3
"""Fortune Cookie Funnies for Engineers — make.fun entry.

Writes one fortune cookie message for a software engineer, a single line
of at most 120 characters, to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt) and prints it to stdout.

Standard library only. Deterministic: the same bytes every run.
"""

import hashlib
import os
import sys
from pathlib import Path

FORTUNE = "Your code will work on the first try, and that will worry you more than any bug."


def output_path() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.txt"


def check() -> int:
    """Re-read entry.txt and verify SHA-256, character count and one line."""
    path = output_path()
    data = path.read_bytes()
    text = data.decode("utf-8")
    lines = text.splitlines()
    sha = hashlib.sha256(data).hexdigest()
    expected = hashlib.sha256((FORTUNE + "\n").encode("utf-8")).hexdigest()
    ok = True
    if sha != expected:
        print(f"FAIL: sha256 {sha} != expected {expected}")
        ok = False
    if len(FORTUNE) > 120 or len(FORTUNE) < 1:
        print(f"FAIL: fortune is {len(FORTUNE)} characters (must be 1-120)")
        ok = False
    if len(lines) != 1 or lines[0] != FORTUNE:
        print(f"FAIL: entry.txt is not exactly one line matching the fortune")
        ok = False
    if FORTUNE.strip() == "":
        print("FAIL: fortune is only whitespace")
        ok = False
    if ok:
        print(f"OK: {len(FORTUNE)} characters, 1 line, sha256 {sha}")
        return 0
    return 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return check()
    text = FORTUNE
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
