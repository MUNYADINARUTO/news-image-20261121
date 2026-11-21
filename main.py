#!/usr/bin/env python3
"""news-image-20261121 entrypoint.

Reads the finished front-page image bundled next to this script
(entry.png), validates it thoroughly as a PNG, and publishes the
validated bytes to /output/entry.png.

The entry is fully deterministic: the program performs no generation
of its own, calls no network, and writes exactly the bytes it read,
so two runs produce byte-identical output. The write is atomic: the
bytes go to a temporary file in the destination directory first and
are then renamed into place, so a failed run can never leave a
partial /output/entry.png behind.
"""

import hashlib
import os
import struct
import sys
import tempfile
import zlib

# The eight-byte magic every PNG file starts with.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# Chunk type names the validator understands.
CHUNK_IHDR = b"IHDR"
CHUNK_PLTE = b"PLTE"
CHUNK_IDAT = b"IDAT"
CHUNK_IEND = b"IEND"

# Valid (colour type, bit depth) pairs from the PNG specification.
# Colour type 0: greyscale; 2: truecolour; 3: indexed colour;
# 4: greyscale with alpha; 6: truecolour with alpha.
VALID_BIT_DEPTHS = {
    0: (1, 2, 4, 8, 16),
    2: (8, 16),
    3: (1, 2, 4, 8),
    4: (8, 16),
    6: (8, 16),
}

# Interlace method must be 0 (none) or 1 (Adam7).
VALID_INTERLACE_METHODS = (0, 1)


class PngError(Exception):
    """Raised when the bundled image fails PNG validation."""


def fail(message):
    """Abort the run with a clear error on stderr and a non-zero exit."""
    print("main.py: invalid PNG: {0}".format(message), file=sys.stderr)
    sys.exit(1)


def check_signature(data):
    """Require the eight-byte PNG signature at the very start."""
    if len(data) < len(PNG_SIGNATURE):
        raise PngError(
            "file is only {0} bytes, shorter than the PNG signature".format(
                len(data)
            )
        )
    if data[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        raise PngError("missing PNG signature at the start of the file")


def check_ihdr_fields(chunk_data, offset):
    """Validate the thirteen bytes of the IHDR chunk."""
    if len(chunk_data) != 13:
        raise PngError(
            "IHDR chunk at byte {0} holds {1} bytes, expected 13".format(
                offset, len(chunk_data)
            )
        )
    width, height, bit_depth, colour_type, compression, filtering, interlace = (
        struct.unpack(">IIBBBBB", chunk_data)
    )
    if width == 0 or height == 0:
        raise PngError(
            "IHDR declares an image of {0}x{1}, both dimensions must be "
            "positive".format(width, height)
        )
    allowed_depths = VALID_BIT_DEPTHS.get(colour_type)
    if allowed_depths is None:
        raise PngError(
            "IHDR colour type {0} is not a defined PNG colour type".format(
                colour_type
            )
        )
    if bit_depth not in allowed_depths:
        raise PngError(
            "IHDR bit depth {0} is not valid for colour type {1} "
            "(allowed: {2})".format(
                bit_depth, colour_type, ", ".join(map(str, allowed_depths))
            )
        )
    if compression != 0:
        raise PngError(
            "IHDR compression method {0} is not 0".format(compression)
        )
    if filtering != 0:
        raise PngError(
            "IHDR filter method {0} is not 0".format(filtering)
        )
    if interlace not in VALID_INTERLACE_METHODS:
        raise PngError(
            "IHDR interlace method {0} is not 0 or 1".format(interlace)
        )
    return width, height


def walk_chunks(data):
    """Walk the chunk list after the signature, validating each chunk.

    Returns a tuple of (width, height) for the caller. Raises PngError
    on the first problem found, naming the byte offset involved.
    """
    offset = len(PNG_SIGNATURE)
    first = True
    saw_idat = False
    saw_plte = False
    colour_type = None
    width = 0
    height = 0
    chunk_index = 0

    while True:
        chunk_start = offset
        if offset + 8 > len(data):
            raise PngError(
                "chunk {0} starts at byte {1} but the file ends at byte "
                "{2} before its header completes".format(
                    chunk_index, chunk_start, len(data)
                )
            )
        length, chunk_type = struct.unpack(">I4s", data[offset : offset + 8])
        offset += 8

        if first and chunk_type != CHUNK_IHDR:
            raise PngError(
                "first chunk is {0!r}, expected IHDR".format(
                    chunk_type.decode("latin-1")
                )
            )
        first = False

        data_end = offset + length
        if data_end + 4 > len(data):
            raise PngError(
                "chunk {0} at byte {1} claims {2} data bytes but the "
                "file ends at byte {3}".format(
                    chunk_type.decode("latin-1"),
                    chunk_start,
                    length,
                    len(data),
                )
            )
        chunk_data = data[offset:data_end]
        stored_crc = struct.unpack(
            ">I", data[data_end : data_end + 4]
        )[0]
        computed_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if stored_crc != computed_crc:
            raise PngError(
                "chunk {0} at byte {1} fails its CRC check "
                "(stored {2:08x}, computed {3:08x})".format(
                    chunk_type.decode("latin-1"),
                    chunk_start,
                    stored_crc,
                    computed_crc,
                )
            )

        if chunk_type == CHUNK_IHDR:
            width, height = check_ihdr_fields(chunk_data, chunk_start)
            colour_type = chunk_data[9]
        elif chunk_type == CHUNK_PLTE:
            if saw_idat:
                raise PngError(
                    "PLTE chunk at byte {0} appears after IDAT".format(
                        chunk_start
                    )
                )
            if len(chunk_data) == 0 or len(chunk_data) % 3 != 0:
                raise PngError(
                    "PLTE chunk at byte {0} holds {1} bytes, not a whole "
                    "number of RGB entries".format(chunk_start, len(chunk_data))
                )
            saw_plte = True
        elif chunk_type == CHUNK_IDAT:
            saw_idat = True
        elif chunk_type == CHUNK_IEND:
            if length != 0:
                raise PngError(
                    "IEND chunk at byte {0} holds {1} bytes, expected "
                    "0".format(chunk_start, length)
                )
            if data_end + 4 != len(data):
                raise PngError(
                    "IEND chunk ends at byte {0} but the file has {1} "
                    "trailing bytes after it".format(
                        data_end + 4, len(data) - (data_end + 4)
                    )
                )
            break

        offset = data_end + 4
        chunk_index += 1

    if not saw_idat:
        raise PngError("no IDAT chunk found in the file")
    if colour_type == 3 and not saw_plte:
        raise PngError(
            "indexed-colour image (colour type 3) has no PLTE chunk"
        )
    return width, height


def validate_png(data):
    """Validate the whole file as a PNG. Returns (width, height)."""
    check_signature(data)
    return walk_chunks(data)


def read_source(path):
    """Read the bundled image, failing clearly when it cannot be read."""
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError as error:
        fail("cannot read {0}: {1}".format(path, error))


def write_atomically(destination, data):
    """Write data to destination via a temp file plus rename."""
    directory = os.path.dirname(destination)
    os.makedirs(directory, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=directory, delete=False
        ) as handle:
            temp_path = handle.name
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, destination)
        temp_path = None
    except OSError as error:
        if temp_path is not None:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        fail("cannot write {0}: {1}".format(destination, error))


def main():
    """Copy the validated bundled image to /output/entry.png."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, "entry.png")
    destination = os.path.join(os.sep, "output", "entry.png")

    data = read_source(source_path)
    try:
        width, height = validate_png(data)
    except PngError as error:
        fail(str(error))

    write_atomically(destination, data)

    digest = hashlib.sha256(data).hexdigest()
    print("wrote {0}".format(destination))
    print("dimensions: {0}x{1}".format(width, height))
    print("size: {0} bytes".format(len(data)))
    print("sha256: {0}".format(digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
