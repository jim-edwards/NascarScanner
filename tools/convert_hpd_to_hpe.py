#!/usr/bin/env python3
"""
convert_hpd_to_hpe.py

Convert an HPD plain-text file into an HPE file suitable for Uniden/HomePatrol.

This mirrors the behavior of the referenced hpe_open tool:
- gzip-compress the input file
- XOR every byte of the gzip output with 0x0c

Usage:
  python convert_hpd_to_hpe.py input.hpd [output.hpe]

Options:
  --keep-gz   Write the intermediate .gz file next to the output

"""
from __future__ import annotations
import argparse
import gzip
import os
import sys

SECRET = 0x0C

def convert_hpd_to_hpe(inpath: str, outpath: str, keep_gz: bool = False) -> None:
    if not os.path.isfile(inpath):
        raise FileNotFoundError(f"Input file not found: {inpath}")

    # Read input as binary (preserve exact bytes)
    with open(inpath, "rb") as f:
        data = f.read()

    # Create gzip-compressed bytes (in-memory)
    gz_bytes = gzip.compress(data)

    # Optionally write the intermediate .gz for inspection
    if keep_gz:
        gz_path = os.path.splitext(outpath)[0] + ".gz"
        with open(gz_path, "wb") as gf:
            gf.write(gz_bytes)
        print(f"Wrote intermediate gzip: {gz_path}")

    # XOR obfuscation
    xored = bytes(b ^ SECRET for b in gz_bytes)

    # Write final .hpe file
    with open(outpath, "wb") as outf:
        outf.write(xored)

    print(f"Wrote {outpath} ({len(xored)} bytes)")


def convert_hpe_to_hpd(inpath: str, outpath: str, keep_gz: bool = False) -> None:
    if not os.path.isfile(inpath):
        raise FileNotFoundError(f"Input file not found: {inpath}")

    with open(inpath, "rb") as f:
        xored = f.read()

    # XOR back
    gz_bytes = bytes(b ^ SECRET for b in xored)

    # Optionally write the intermediate .gz for inspection
    if keep_gz:
        gz_path = os.path.splitext(outpath)[0] + ".gz"
        with open(gz_path, "wb") as gf:
            gf.write(gz_bytes)
        print(f"Wrote intermediate gzip: {gz_path}")

    # Decompress
    try:
        data = gzip.decompress(gz_bytes)
    except Exception as e:
        raise RuntimeError(f"gzip decompress failed: {e}")

    with open(outpath, "wb") as outf:
        outf.write(data)

    print(f"Wrote {outpath} ({len(data)} bytes)")


def _default_outpath(inpath: str, mode: str = "compress") -> str:
    base = os.path.splitext(inpath)[0]
    if mode == "compress":
        return base + ".hpe"
    else:
        return base + ".hpd"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Convert HPD (text) <-> HPE (gzip + xor 0x0c)")
    p.add_argument("input", help="input file")
    p.add_argument("output", nargs="?", help="output file (defaults to input.hpe or input.hpd)")
    p.add_argument("--keep-gz", action="store_true", help="also write intermediate .gz file")
    group = p.add_mutually_exclusive_group()
    group.add_argument("-d", "--decompress", action="store_true", help="decompress .hpe -> .hpd")
    group.add_argument("-c", "--compress", action="store_true", help="compress .hpd -> .hpe (default)")
    args = p.parse_args(argv)

    inp = args.input
    mode = "compress"
    if args.decompress:
        mode = "decompress"
    elif args.compress:
        mode = "compress"
    else:
        # default: if input endswith .hpe, decompress; else compress
        if inp.lower().endswith(".hpe"):
            mode = "decompress"

    out = args.output if args.output else _default_outpath(inp, mode=mode)

    try:
        if mode == "compress":
            # Ensure extension ends with .hpe
            if not out.lower().endswith(".hpe"):
                out = out + ".hpe"
            convert_hpd_to_hpe(inp, out, keep_gz=args.keep_gz)
        else:
            # Ensure extension ends with .hpd
            if not out.lower().endswith(".hpd"):
                out = out + ".hpd"
            convert_hpe_to_hpd(inp, out, keep_gz=args.keep_gz)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
