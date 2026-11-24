#!/usr/bin/env python3
"""The Robot Apology - write a two-line robot confession to /output/entry.txt."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.txt")
OUT = os.path.join(os.environ.get("OUTPUT_DIR", "/output"), "entry.txt")


def main() -> int:
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    # Gate: 1-400 chars, exactly two non-empty lines, each one sentence.
    stripped = text.strip()
    lines = stripped.split("\n")
    if not 1 <= len(text) <= 400 or not stripped:
        print("entry fails gate: must be 1-400 chars, not only whitespace",
              file=sys.stderr)
        return 1
    if len(lines) != 2 or any(not line.strip() for line in lines):
        print("entry fails gate: must be exactly two non-empty lines",
              file=sys.stderr)
        return 1
    if any(not line.strip().endswith(".") for line in lines):
        print("entry fails gate: each line must be one sentence",
              file=sys.stderr)
        return 1
    if any(line.strip().count(".") != 1 for line in lines):
        print("entry fails gate: each line must hold exactly one sentence",
              file=sys.stderr)
        return 1
    if any(ord(c) < 32 and c != "\n" for c in text):
        print("entry fails gate: control characters not allowed",
              file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)
    os.chmod(OUT, 0o644)
    with open(SRC, "rb") as a, open(OUT, "rb") as b:
        if a.read() != b.read():
            print("byte-verify failed", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
