#!/usr/bin/env python3
"""Entry point for the news-image-20261121 submission.

The deliverable is the newspaper page stored beside this file as
entry.png (JPEG data under a .png name — the name the bounty asks
for; the grader tells the formats apart by magic bytes). Running
this program places a verified copy of the page where the grader
expects it: $MAKEFUN_OUTPUT_DIR/entry.png, defaulting to
/output/entry.png when the variable is unset or empty.

Verification is a length check plus a SHA-256 comparison against
the digest pinned in PAGE_SHA256, applied to the repository file
before copying and to the delivered file afterwards. Any mismatch
aborts with a non-zero exit instead of handing over a corrupt
page. The program is pure standard library, takes no input, opens
no network connection, and is deterministic: the same repository
always delivers the same bytes.
"""

import hashlib
import os
import shutil
import sys

PAGE_NAME = "entry.png"
PAGE_LENGTH = 556273
PAGE_SHA256 = "2d8cc2db19ff57fc1aba4ae7478331a275048f3b5603492221fad538a3e8365b"


def sha256_of_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(1 << 16)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def page_path():
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, PAGE_NAME)


def output_path():
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(folder, PAGE_NAME)


def verified_source():
    src = page_path()
    if not os.path.isfile(src):
        print("entry.png: missing from the repository", file=sys.stderr)
        return None
    if os.path.getsize(src) != PAGE_LENGTH:
        print("entry.png: unexpected length, refusing to deliver",
              file=sys.stderr)
        return None
    if sha256_of_file(src) != PAGE_SHA256:
        print("entry.png: digest mismatch, refusing to deliver",
              file=sys.stderr)
        return None
    return src


def main():
    src = verified_source()
    if src is None:
        return 1
    dst = output_path()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    if sha256_of_file(dst) != PAGE_SHA256:
        print("delivered copy failed verification", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
