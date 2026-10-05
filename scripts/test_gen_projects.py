"""Offline regressions for public filtering, pagination, and both catalog outputs."""
import io
import json
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).with_name("gen_projects.py")
with patch.dict(os.environ, {"GITHUB_TOKEN": "test"}):
    MODULE = runpy.run_path(str(SCRIPT))


def repo(name="good", **changes):
    value = {"full_name": f"Rajveerx11/{name}", "name": name, "private": False,
             "fork": False, "language": "Python", "stargazers_count": 1,
             "pushed_at": "2026-01-01", "description": "A public description."}
    value.update(changes)
    return value


class PublicProjectsTest(unittest.TestCase):
    def test_public_only_forks_marked_and_escaped(self):
        repositories = [repo(), repo("private-build", private=True),
                        repo("bad&name"), repo("a-fork", fork=True),
                        repo("unknown-privacy", private=None), repo("Rajveerx11"),
                        repo("very-long-public-repository-name-that-needs-truncation")]

        def fake_urlopen(request, **kwargs):
            return io.BytesIO(json.dumps(repositories if "/users/" in request.full_url else []).encode())

        with tempfile.TemporaryDirectory() as folder, patch("urllib.request.urlopen", side_effect=fake_urlopen), patch.dict(os.environ, {"GITHUB_TOKEN": "test"}):
            previous = Path.cwd()
            try:
                os.chdir(folder)
                runpy.run_path(str(SCRIPT), run_name="__main__")
                svg = Path("assets/project-index.svg").read_text(encoding="utf-8")
                markdown = Path("docs/public-repositories.md").read_text(encoding="utf-8")
            finally:
                os.chdir(previous)
        ET.fromstring(svg)
        self.assertIn("bad&amp;name", svg)
        for name in ("private-build", "unknown-privacy"):
            self.assertNotIn(name, svg + markdown)
        self.assertNotIn("very-long-public-repository-name-that-needs-truncation", svg)
        self.assertIn("very-long-public-repository-…", svg)
        self.assertIn("4 public repositories", svg)
        self.assertIn("/ fork", svg)
        self.assertIn("| Fork |", markdown)
        self.assertIn("https://github.com/Rajveerx11/bad%26name", markdown)
        self.assertIn("very-long-public-repository-name-that-needs-truncation", markdown)
        self.assertNotIn("PRIVATE", svg)

    def test_deduplicates_and_fails_closed_on_missing_privacy(self):
        unknown = repo("unknown")
        del unknown["private"]
        items = MODULE["public_projects"]([repo(), repo(full_name="RAJVEERX11/GOOD"), unknown])
        self.assertEqual([item["name"] for item in items], ["good"])

    def test_organization_namespace_preserved(self):
        items = MODULE["public_projects"]([repo("same"), repo("same", full_name="neuratile/same")])
        markdown = MODULE["render_markdown"](items, "2026-01-01")
        self.assertIn("https://github.com/Rajveerx11/same", markdown)
        self.assertIn("https://github.com/neuratile/same", markdown)
        self.assertEqual(len(items), 2)

    def test_markdown_metadata_cannot_add_rows_or_active_html(self):
        value = "A | [link](javascript:alert(1)) <script>bad</script>\n# injected"
        items = MODULE["public_projects"]([repo(description=value)])
        markdown = MODULE["render_markdown"](items, "2026-01-01")
        self.assertNotIn("<script>", markdown)
        self.assertNotIn("\n# injected", markdown)
        self.assertIn("\\|", markdown)
        self.assertIn("\\[link\\]", markdown)
        self.assertEqual(len([line for line in markdown.splitlines() if line.startswith("| ")]), 3)

    def test_missing_metadata_and_empty_catalog(self):
        items = MODULE["public_projects"]([repo(language=None, description=None)])
        markdown = MODULE["render_markdown"](items, "2026-01-01")
        self.assertIn("Not reported", markdown)
        self.assertIn("No public description supplied.", markdown)
        self.assertIn("No public repositories returned.", MODULE["render_svg"]([], "2026-01-01"))
        self.assertIn("No public repositories returned.", MODULE["render_markdown"]([], "2026-01-01"))

    def test_pagination(self):
        calls = []
        chunks = [[repo(str(i)) for i in range(100)], [repo("last")]]

        def fake_urlopen(request, **kwargs):
            calls.append(request.full_url)
            return io.BytesIO(json.dumps(chunks[len(calls) - 1]).encode())

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            result = MODULE["collect"]("/users/Rajveerx11/repos", "&type=owner")
        self.assertEqual(len(result), 101)
        self.assertIn("page=1", calls[0])
        self.assertIn("page=2", calls[1])
        self.assertIn("type=owner", calls[1])


if __name__ == "__main__":
    unittest.main()
