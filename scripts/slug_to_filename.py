#!/usr/bin/env python3

import argparse
import re


def slug_to_stem(slug: str) -> str:
    s = slug.strip().strip("/")
    s = s.replace("/", "-")
    s = s.lower()
    s = re.sub(r"[^a-z0-9._-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "podcast"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--ext", required=True)
    args = ap.parse_args()

    stem = slug_to_stem(args.slug)
    ext = args.ext.lstrip(".")
    print(f"{stem}.{ext}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

