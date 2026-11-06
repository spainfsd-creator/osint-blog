#!/usr/bin/env python3
"""Remove Docusaurus' hashed duplicates of podcasts from a production build.

Podcast files live in ``static/podcasts`` and therefore already appear in the
build as ``podcasts/<name>.m4a``. Docusaurus also treats Markdown download links
as imported assets, emits a second hashed copy in ``assets/files`` and rewrites
the rendered link to that copy. On this blog the duplicate set is several GB
and can push the GitHub Pages artifact over its hard size limit.

This postprocessor verifies every hashed M4A against its static original,
rewrites generated text assets to the static URL, and removes only the verified
duplicate from the generated build directory.
"""

from __future__ import annotations

import argparse
import filecmp
import re
from pathlib import Path


HASHED_M4A = re.compile(r"^(?P<stem>.+)-[0-9a-f]{32}\.m4a$")
TEXT_SUFFIXES = {".html", ".js", ".json", ".xml", ".txt", ".map"}


def rewrite_build(repo: Path) -> tuple[int, int, int]:
    build = repo / "build"
    hashed_dir = build / "assets" / "files"
    podcasts = repo / "static" / "podcasts"

    if not build.is_dir():
        raise RuntimeError(f"No existe el directorio de build: {build}")
    if not podcasts.is_dir():
        return (0, 0, 0)
    if not hashed_dir.is_dir():
        return (0, 0, 0)

    duplicates: list[tuple[Path, Path, bytes, bytes]] = []
    for hashed in sorted(hashed_dir.glob("*.m4a")):
        match = HASHED_M4A.match(hashed.name)
        if not match:
            raise RuntimeError(f"M4A generado con nombre inesperado: {hashed}")

        original = podcasts / f"{match.group('stem')}.m4a"
        if not original.is_file():
            raise RuntimeError(
                f"No se encuentra el podcast estático correspondiente a {hashed.name}: "
                f"{original}"
            )
        if hashed.stat().st_size != original.stat().st_size:
            raise RuntimeError(f"Tamaño distinto entre duplicado y original: {hashed}")
        if not filecmp.cmp(hashed, original, shallow=False):
            raise RuntimeError(f"Contenido distinto entre duplicado y original: {hashed}")

        old = f"assets/files/{hashed.name}".encode()
        new = f"podcasts/{original.name}".encode()
        duplicates.append((hashed, original, old, new))

    replacements = 0
    touched_files = 0
    referenced: set[Path] = set()
    for output in build.rglob("*"):
        if not output.is_file() or output.suffix.lower() not in TEXT_SUFFIXES:
            continue
        content = output.read_bytes()
        updated = content
        for hashed, _original, old, new in duplicates:
            count = updated.count(old)
            if count:
                updated = updated.replace(old, new)
                replacements += count
                referenced.add(hashed)
        if updated != content:
            output.write_bytes(updated)
            touched_files += 1

    unreferenced = [path for path, *_rest in duplicates if path not in referenced]
    if unreferenced:
        names = ", ".join(path.name for path in unreferenced[:5])
        raise RuntimeError(
            f"Hay {len(unreferenced)} duplicados sin referencia reescrita; "
            f"no se elimina nada. Ejemplos: {names}"
        )

    for hashed, _original, _old, _new in duplicates:
        hashed.unlink()

    return (len(duplicates), replacements, touched_files)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()

    duplicates, replacements, touched = rewrite_build(args.repo.resolve())
    print(
        "[OK  ] Podcasts del build deduplicados: "
        f"{duplicates} copias, {replacements} referencias, {touched} ficheros"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
