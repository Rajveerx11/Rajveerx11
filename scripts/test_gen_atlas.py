"""Offline checks for GitHub-safe assets and the README's image fallbacks."""
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

from gen_atlas import ROOT, build_assets


class PictureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "img":
            self.images.append(attrs)
        elif tag == "source":
            self.sources.append(attrs)


class AtlasTest(unittest.TestCase):
    def test_generated_variants_match_checked_in_files(self):
        assets = build_assets()
        self.assertEqual(len(assets), 10)
        for name, svg in assets.items():
            with self.subTest(name=name):
                self.assertEqual((ROOT / "assets" / name).read_text(encoding="utf-8"), svg)
                root = ET.fromstring(svg)
                self.assertEqual(root.attrib["role"], "img")
                self.assertIn("aria-labelledby", root.attrib)
                for element in root.iter():
                    self.assertNotIn(element.tag.split("}")[-1], ("script", "foreignObject", "animate"))
                    for attribute in element.attrib:
                        self.assertFalse(attribute.startswith("on"))
                        self.assertNotIn(attribute.split("}")[-1], ("href", "src"))

    def test_atlas_preserves_roles_and_conceptual_boundary(self):
        for name, svg in build_assets().items():
            if name.startswith("execution-atlas"):
                with self.subTest(name=name):
                    for title in ("Human input", "Context", "Orchestration", "Testing", "Verification", "Memory"):
                        self.assertIn(title, svg)
                    self.assertIn("not repository integrations", svg)
                    if "mobile" in name:
                        self.assertIn('viewBox="0 0 430 790"', svg)

    def test_atlas_footer_stays_below_project_labels(self):
        for name, svg in build_assets().items():
            if not name.startswith("execution-atlas"):
                continue
            labels = list(ET.fromstring(svg).iter("{http://www.w3.org/2000/svg}text"))
            last_project = max(float(label.attrib["y"]) for label in labels
                               if label.text in ("Tessera", "Proof-of-Work", "Intelligence"))
            footer = next(float(label.attrib["y"]) for label in labels
                          if label.text == "Roles, not repository integrations.")
            self.assertGreater(footer - last_project, 20, name)

    def test_recorder_is_pinned_and_not_live_telemetry(self):
        for name, svg in build_assets().items():
            if name.startswith("flight-recorder"):
                self.assertIn("48266fa", svg)
                self.assertIn("18 Jun 2026", svg)
                self.assertNotIn("LIVE", svg)
                self.assertIn("cancellation token", svg)

    def test_readme_images_have_existing_sources_and_alt_text(self):
        parser = PictureParser()
        parser.feed((ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(len(parser.sources), 7)
        self.assertGreaterEqual(len(parser.images), 5)
        for image in parser.images:
            self.assertTrue(image.get("alt"))
            self.assertTrue((ROOT / image["src"]).is_file())
        for source in parser.sources:
            if source["srcset"].endswith("-light.svg"):
                self.assertIn("prefers-color-scheme", source["media"])
            else:
                self.assertIn("max-width", source["media"])
            self.assertTrue((ROOT / source["srcset"]).is_file())

    def test_workflow_tracks_index_and_avoids_generated_commit_loop(self):
        workflow = (ROOT / ".github/workflows/stats.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request:", workflow)
        self.assertIn("python -m unittest discover -s scripts -v", workflow)
        self.assertIn("if: github.event_name != 'pull_request'", workflow)
        ignored = workflow.split("paths-ignore:", 1)[1].split("pull_request:", 1)[0]
        for path in ("assets/github-stats.svg", "assets/project-index.svg", "docs/public-repositories.md"):
            self.assertIn(path, ignored)
        self.assertIn("git add assets/github-stats.svg assets/project-index.svg docs/public-repositories.md", workflow)


if __name__ == "__main__":
    unittest.main()
