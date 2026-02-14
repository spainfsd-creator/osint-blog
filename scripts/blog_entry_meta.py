#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


def _read_frontmatter(md_text: str) -> dict:
    # Minimal frontmatter parser for simple Docusaurus posts.
    if not md_text.startswith("---"):
        return {}
    parts = md_text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    fm_block = parts[0].strip()
    fm_block = fm_block.removeprefix("---").strip()
    fm = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def _read_docusaurus_url_baseurl(config_text: str) -> tuple[str, str]:
    # Best-effort extraction of `url: '...'` and `baseUrl: '...'` from docusaurus.config.ts
    m_url = re.search(r"\burl:\s*['\"]([^'\"]+)['\"]", config_text)
    m_base = re.search(r"\bbaseUrl:\s*['\"]([^'\"]+)['\"]", config_text)
    url = m_url.group(1) if m_url else ""
    base_url = m_base.group(1) if m_base else "/"
    return url, base_url


def _join_url(url: str, base_url: str, slug: str) -> str:
    url = url.rstrip("/")
    if not base_url.startswith("/"):
        base_url = "/" + base_url
    if not base_url.endswith("/"):
        base_url += "/"
    slug = slug.lstrip("/")
    return f"{url}{base_url}{slug}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--post", required=True)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    post = Path(args.post).resolve()
    cfg = repo / "docusaurus.config.ts"

    md_text = post.read_text(encoding="utf-8")
    fm = _read_frontmatter(md_text)

    title = fm.get("title", "").strip()
    slug = fm.get("slug", "").strip()
    date = fm.get("date", "").strip()

    cfg_text = cfg.read_text(encoding="utf-8") if cfg.exists() else ""
    url, base_url = _read_docusaurus_url_baseurl(cfg_text)
    public_url = _join_url(url, base_url, slug) if (url and slug) else ""

    out = {
        "title": title,
        "slug": slug,
        "date": date,
        "base_url": base_url,
        "public_url": public_url,
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

