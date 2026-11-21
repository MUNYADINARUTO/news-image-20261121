#!/usr/bin/env python3
"""Copy the bundled front-page image to /output/entry.png.

The picture itself was drawn and checked while the entry was built,
so this program has nothing to generate: it moves the finished
bytes into place. It reads entry.png from the same directory as
this script, confirms the bytes open with the PNG signature, writes
them to /output/entry.png through a temporary file, and prints the
size and SHA-256 of what it wrote. Two runs write identical bytes.
"""

import hashlib
import os
import struct
import sys
import tempfile

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
OUTPUT_PATH = os.path.join(os.sep, "output", "entry.png")


def die(message):
    print("main.py: {0}".format(message), file=sys.stderr)
    sys.exit(1)


def read_bundled_image():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as error:
        die("cannot read {0}: {1}".format(path, error))


def png_dimensions(data):
    if len(data) < 24 or data[:8] != PNG_MAGIC:
        die("bundled file is not a PNG image")
    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0:
        die("PNG header declares a zero dimension")
    return width, height


def write_output(destination, data):
    folder = os.path.dirname(destination)
    os.makedirs(folder, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=folder, delete=False) as handle:
            tmp = handle.name
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, destination)
        tmp = None
    except OSError as error:
        if tmp is not None:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        die("cannot write {0}: {1}".format(destination, error))


def main(destination=OUTPUT_PATH):
    data = read_bundled_image()
    width, height = png_dimensions(data)
    write_output(destination, data)
    print("wrote {0}".format(destination))
    print("dimensions: {0}x{1}".format(width, height))
    print("size: {0} bytes".format(len(data)))
    print("sha256: {0}".format(hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
