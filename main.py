#!/usr/bin/env python3
"""Deliver the front page for make.fun's news-image-20261121 bounty.

The finished page lives in this repository as entry.png — in fact
JPEG bytes under a .png name, which the bounty allows because it
tells PNG from JPEG by the file's first bytes. This program copies
the page to the grader's output path ($MAKEFUN_OUTPUT_DIR/entry.png,
or /output/entry.png when the variable is unset). Before and after
the copy it checks the page's length and SHA-256 digest against the
values pinned below, so a damaged or swapped file fails loudly
instead of being graded. Nothing here touches the network, the
clock or a random source: the same repository always yields the
same bytes, run after run.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGE = HERE / "entry.png"
EXPECTED_BYTES = 556273
EXPECTED_SHA256 = "2d8cc2db19ff57fc1aba4ae7478331a275048f3b5603492221fad538a3e8365b"


def digest_of(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def checked_page():
    size = PAGE.stat().st_size
    if size != EXPECTED_BYTES:
        sys.exit(f"entry.png has {size} bytes; expected {EXPECTED_BYTES}")
    actual = digest_of(PAGE)
    if actual != EXPECTED_SHA256:
        sys.exit(f"entry.png digests to {actual}; expected {EXPECTED_SHA256}")
    return PAGE


def destination():
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(folder or "/output") / "entry.png"


def run():
    source = checked_page()
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    found = digest_of(target)
    if found != EXPECTED_SHA256:
        print(f"copy verification failed for {target}: "
              f"delivered digest {found}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
