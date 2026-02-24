#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER_KEYS = {"title", "slug", "authors", "tags", "date", "image"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_frontmatter(md_text: str):
    if not md_text.startswith("---\n"):
        return None, md_text
    end = md_text.find("\n---\n", 4)
    if end == -1:
        return None, md_text
    return md_text[4:end], md_text[end + 5 :]


def parse_frontmatter(fm_block: str) -> dict:
    fm = {}
    for raw in fm_block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def infer_post(repo: Path) -> Path:
    blog_dir = repo / "blog"
    posts = sorted(blog_dir.glob("20*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not posts:
        raise FileNotFoundError("No se han encontrado posts en blog/")
    return posts[0]


def image_path_from_frontmatter(repo: Path, image_value: str) -> Path:
    if not image_value.startswith("/img/"):
        raise ValueError(f"`image` no apunta a /img/...: {image_value}")
    return repo / "static" / image_value.lstrip("/")


def check_post(repo: Path, post_path: Path) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []

    if not post_path.exists():
        return [f"Post no existe: {post_path}"]

    md_text = read_text(post_path)
    fm_block, body = split_frontmatter(md_text)
    if fm_block is None:
        return [f"Frontmatter inválido o ausente en {post_path.name}"]

    fm = parse_frontmatter(fm_block)
    missing = REQUIRED_FRONTMATTER_KEYS - set(fm.keys())
    if missing:
        errors.append(f"Faltan claves de frontmatter: {', '.join(sorted(missing))}")

    image_value = fm.get("image", "")
    if image_value:
        try:
            image_path = image_path_from_frontmatter(repo, image_value)
            if not image_path.exists():
                errors.append(f"Imagen referenciada no existe: {image_path}")
            else:
                if image_path.stat().st_size < 50_000:
                    warnings.append(f"Imagen muy pequeña ({image_path.stat().st_size} bytes): {image_path.name}")
        except Exception as exc:
            errors.append(str(exc))
    else:
        errors.append("Frontmatter `image` vacío")

    if "<!-- truncate -->" not in body:
        errors.append("Falta `<!-- truncate -->` en el cuerpo del post")

    if image_value and image_value not in body:
        warnings.append("La imagen del frontmatter no aparece insertada en el cuerpo (recomendado antes de truncate)")

    # Comprobación ligera de slug vs nombre de archivo
    slug = fm.get("slug", "").strip().lstrip("/")
    if slug and slug not in post_path.name:
        warnings.append(f"El slug `{slug}` no coincide con el nombre de archivo `{post_path.name}`")

    # Autor esperado en este blog
    authors_raw = fm.get("authors", "")
    if "osint-writter" not in authors_raw:
        warnings.append("El autor no incluye `osint-writter` (revisar frontmatter)")

    for w in warnings:
        print(f"[WARN] {w}")
    for e in errors:
        print(f"[ERR ] {e}")
    if not errors:
        print(f"[OK  ] Preflight post assets correcto: {post_path}")

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Preflight de post Docusaurus (frontmatter + imagen + truncate)")
    ap.add_argument("--repo", default=".", help="Ruta del repo osint-blog")
    ap.add_argument("--post", help="Ruta al post .md; por defecto el más reciente en blog/")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    post_path = Path(args.post).resolve() if args.post else infer_post(repo)

    errors = check_post(repo, post_path)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
