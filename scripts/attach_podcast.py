#!/usr/bin/env python3

import argparse
import shutil
from pathlib import Path


PODCAST_LINE_PREFIX = "**Descargar el podcast!**:"


def _ensure_podcast_line(md_text: str, podcast_filename: str) -> str:
    line = f"**Descargar el podcast!**: [Descargar el podcast](/podcasts/{podcast_filename})"
    if line in md_text:
        return md_text

    # Insert after the first image block (featured image), or after frontmatter.
    lines = md_text.splitlines()

    # Find end of frontmatter.
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        if i < len(lines) and lines[i].strip() == "---":
            i += 1

    # Find first markdown image after frontmatter.
    insert_at = None
    for j in range(i, len(lines)):
        if lines[j].lstrip().startswith("![") and "](" in lines[j]:
            insert_at = j + 1
            break

    if insert_at is None:
        insert_at = i

    # Keep a blank line separation.
    to_insert = ["", line, ""]
    new_lines = lines[:insert_at] + to_insert + lines[insert_at:]
    return "\n".join(new_lines) + ("\n" if md_text.endswith("\n") else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--post", required=True)
    ap.add_argument("--audio_path", required=True)
    ap.add_argument("--podcast_filename", required=True)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    post_path = Path(args.post).resolve()
    audio_path = Path(args.audio_path).resolve()

    podcasts_dir = repo / "static" / "podcasts"
    podcasts_dir.mkdir(parents=True, exist_ok=True)

    dst = podcasts_dir / args.podcast_filename
    shutil.copy2(audio_path, dst)

    md_text = post_path.read_text(encoding="utf-8")
    md_text2 = _ensure_podcast_line(md_text, args.podcast_filename)
    if md_text2 != md_text:
        post_path.write_text(md_text2, encoding="utf-8")

    print(str(dst))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

