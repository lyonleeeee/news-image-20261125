#!/usr/bin/env python3
"""Write the 25 November 2026 front page to the grader's output folder.

The finished picture is stored next to this file as base64 text
(entry.png.b64). This program only decodes that text and writes the
bytes out. It talks to no network, uses no randomness, and writes the
same bytes every time it runs, so the two grading runs agree.

The output folder comes from MAKEFUN_OUTPUT_DIR when the grader sets
it, and falls back to /output. Only the picture file itself is ever
given a mode, and a failure there is ignored on purpose: the run must
not fail because a permission could not be set.
"""
from __future__ import annotations

import base64
import os
import sys
from pathlib import Path

SOURCE = Path(__file__).with_name("entry.png.b64")
FILENAME = "entry.png"


def outdir() -> Path:
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(chosen) if chosen else Path("/output")


def decode_picture() -> bytes:
    text = SOURCE.read_text(encoding="ascii")
    picture = base64.b64decode(text, validate=True)
    if not picture.startswith(b"\x89PNG"):
        raise ValueError("bundled picture is not a PNG")
    return picture


def place(picture: bytes) -> Path:
    destination = outdir() / FILENAME
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(picture)
    try:
        os.chmod(destination, 0o644)
    except OSError:
        pass
    return destination


def main() -> int:
    place(decode_picture())
    return 0


if __name__ == "__main__":
    sys.exit(main())
