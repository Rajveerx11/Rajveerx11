"""Offline regression: only public repositories reach the generated card."""
import io
import json
import os
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).with_name("gen_projects.py")


class PublicProjectsTest(unittest.TestCase):
    def test_public_only_and_escaped(self):
        def fake_urlopen(request):
            if "/users/" in request.full_url:
                repos = [
                    {"full_name": "Rajveerx11/good", "name": "good", "private": False,
                     "fork": False, "language": "Python", "stargazers_count": 1, "pushed_at": "2026-01-01"},
                    {"full_name": "Rajveerx11/private-build", "name": "private-build", "private": True,
                     "fork": False, "language": "Python", "stargazers_count": 8, "pushed_at": "2026-01-01"},
                    {"full_name": "Rajveerx11/bad&name", "name": "bad&name", "private": False,
                     "fork": False, "language": "HTML", "stargazers_count": 0, "pushed_at": "2026-01-01"},
                    {"full_name": "Rajveerx11/unknown-privacy", "name": "unknown-privacy",
                     "fork": False, "language": "Python", "stargazers_count": 0, "pushed_at": "2026-01-01"},
                    {"full_name": "Rajveerx11/very-long-public-repository-name-that-needs-truncation",
                     "name": "very-long-public-repository-name-that-needs-truncation", "private": False,
                     "fork": False, "language": "Python", "stargazers_count": 2, "pushed_at": "2026-01-01"},
                ]
            else:
                repos = []
            return io.BytesIO(json.dumps(repos).encode())

        with tempfile.TemporaryDirectory() as folder, patch("urllib.request.urlopen", side_effect=fake_urlopen), patch.dict(os.environ, {"GITHUB_TOKEN": "test"}):
            previous = Path.cwd()
            try:
                os.chdir(folder)
                runpy.run_path(str(SCRIPT))
                svg = Path("assets/project-index.svg").read_text(encoding="utf-8")
            finally:
                os.chdir(previous)
        self.assertIn("good", svg)
        self.assertIn("bad&amp;name", svg)
        self.assertNotIn("private-build", svg)
        self.assertNotIn("unknown-privacy", svg)
        self.assertNotIn("very-long-public-repository-name-that-needs-truncation", svg)
        self.assertIn("very-long-public-repository-", svg)
        self.assertNotIn("PRIVATE", svg)
        self.assertIn("3 public repositories", svg)


if __name__ == "__main__":
    unittest.main()
