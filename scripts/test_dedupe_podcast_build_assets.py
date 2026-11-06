#!/usr/bin/env python3

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dedupe_podcast_build_assets import rewrite_build


class DedupePodcastBuildAssetsTest(unittest.TestCase):
    def test_rewrites_link_and_keeps_static_original(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            podcasts = repo / "static" / "podcasts"
            hashed_dir = repo / "build" / "assets" / "files"
            podcasts.mkdir(parents=True)
            hashed_dir.mkdir(parents=True)

            audio = b"valid m4a fixture"
            original = podcasts / "episodio.m4a"
            duplicate = hashed_dir / f"episodio-{'a' * 32}.m4a"
            original.write_bytes(audio)
            duplicate.write_bytes(audio)
            page = repo / "build" / "index.html"
            page.write_text(
                f'<a href="/osint-blog/assets/files/{duplicate.name}">audio</a>',
                encoding="utf-8",
            )

            result = rewrite_build(repo)

            self.assertEqual(result, (1, 1, 1))
            self.assertTrue(original.exists())
            self.assertFalse(duplicate.exists())
            self.assertIn(
                "/osint-blog/podcasts/episodio.m4a",
                page.read_text(encoding="utf-8"),
            )

    def test_refuses_to_delete_nonidentical_audio(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            podcasts = repo / "static" / "podcasts"
            hashed_dir = repo / "build" / "assets" / "files"
            podcasts.mkdir(parents=True)
            hashed_dir.mkdir(parents=True)

            original = podcasts / "episodio.m4a"
            duplicate = hashed_dir / f"episodio-{'b' * 32}.m4a"
            original.write_bytes(b"original")
            duplicate.write_bytes(b"different")

            with self.assertRaisesRegex(RuntimeError, "Tamaño distinto"):
                rewrite_build(repo)
            self.assertTrue(duplicate.exists())


if __name__ == "__main__":
    unittest.main()
