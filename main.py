#!/usr/bin/env python3
"""news-image-20261123: copy the bundled front-page poster to the output.

The entry image (entry.png, drawn for Monday 23 November 2026) sits
beside this file in the repository. It sums up the day: Wall Street's
record rebound after Nvidia reinstated Jensen Huang, Ukraine sinking
a Russian warship off Libya, the Democrats' historic House majority,
an Indonesian factory fire, and the Ebola response in DR Congo.

This program copies the image, byte for byte, to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). It uses only the
Python standard library and touches no network.
"""
import hashlib
import os
import shutil
import sys


def output_path():
    """Return the destination path for the entry image.

    The grader sets MAKEFUN_OUTPUT_DIR; fall back to /output so a
    plain local run behaves the same way.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.png")


def source_path():
    """Return the path of the bundled image next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def main():
    src = source_path()
    dst = output_path()
    if not os.path.isfile(src):
        print("missing bundled image: %s" % src, file=sys.stderr)
        return 1
    parent = os.path.dirname(dst)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, dst)
    # Confirm the copy landed intact before reporting success: same
    # size and same sha256, so repeated runs write identical bytes.
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy size mismatch: %s" % dst, file=sys.stderr)
        return 1
    with open(src, "rb") as fh:
        src_hash = hashlib.sha256(fh.read()).hexdigest()
    with open(dst, "rb") as fh:
        dst_hash = hashlib.sha256(fh.read()).hexdigest()
    if src_hash != dst_hash:
        print("copy hash mismatch: %s" % dst, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
