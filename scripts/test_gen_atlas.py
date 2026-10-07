"""Offline checks for GitHub-safe assets and the README's image fallbacks."""
from fnmatch import fnmatch
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

from gen_atlas import PANELS, ROOT, build_assets


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
        self.assertEqual(len(assets), 32)
        for panel in PANELS:
            for variant in ("", "-light", "-mobile", "-mobile-light"):
                self.assertIn(f"{panel}{variant}.svg", assets)
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
        self.assertEqual(len(parser.sources), 5)
        self.assertEqual(len(parser.images), 3)
        self.assertEqual([image["src"] for image in parser.images],
                         [f"./assets/{name}.svg" for name in ("contrib-heatmap", "rajveer-ascii", "stats")])
        self.assertEqual([image["width"] for image in parser.images], ["860", "420", "420"])
        for name in ("rajveer-ascii", "stats"):
            self.assertEqual(ET.parse(ROOT / "assets" / f"{name}.svg").getroot().attrib["viewBox"], "0 0 840 880")
        for image in parser.images:
            self.assertTrue(image.get("alt"))
            self.assertTrue((ROOT / image["src"]).is_file())
        self.assertEqual([source["media"] for source in parser.sources[:3]],
                         ["(prefers-reduced-motion: reduce) and (prefers-color-scheme: light)",
                          "(prefers-reduced-motion: reduce)", "(prefers-color-scheme: light)"])
        for source in parser.sources:
            self.assertTrue("prefers-reduced-motion" in source["media"] or "prefers-color-scheme" in source["media"])
            self.assertTrue((ROOT / source["srcset"]).is_file())

    def test_evaluation_keeps_results_and_limitations_visible(self):
        for name, svg in build_assets().items():
            if not name.startswith("evaluation"):
                continue
            visible = " ".join(element.text or "" for element in
                               ET.fromstring(svg).iter("{http://www.w3.org/2000/svg}text"))
            for evidence in ("60", "20 tasks / 3 configurations", "20 / 20 passed", "17 / 20 passed",
                             "3 failed", "AUGUST 2026", "NOT AN AGENT RANKING",
                             "eight days earlier", "Token usage and exact cost are unknown",
                             "One attempt", "All outcomes retained", "not tampering",
                             "protected outcome verifier", "anti-tampering gate"):
                with self.subTest(asset=name, evidence=evidence):
                    self.assertIn(evidence, visible)

    def test_visual_profile_keeps_native_navigation_and_text_companion(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        companion = (ROOT / "docs/profile-evidence.md").read_text(encoding="utf-8")
        self.assertNotIn("| ---", readme)
        self.assertIn("[Project evidence](docs/profile-evidence.md)", readme)
        for source in ("https://github.com/Rajveerx11/AgentWisper",
                       "https://github.com/Rajveerx11/gfi-scout",
                       "https://github.com/Rajveerx11/repograph-intelligence",
                       "https://github.com/Rajveerx11/neura",
                       "https://github.com/neuratile/Tessera",
                       "https://github.com/Rajveerx11/proof-of-work",
                       "https://github.com/Rajveerx11/obsidian-graph-intelligence",
                       "https://github.com/Rajveerx11/unified-memory-mcp",
                       "https://github.com/Rajveerx11/pr-reliability-platform",
                       "https://github.com/Rajveerx11/Master-Models"):
            self.assertIn(f"]({source})", companion)
        self.assertIn('<div align="center">', readme)
        self.assertIn('<table>', readme)
        headings = ["./contributions.sh", "whoami", "./links.sh"]
        self.assertEqual(readme.count("<h3>"), 3)
        for heading in headings:
            self.assertIn(f"rajveer@github ~ $ {heading}", readme)
        self.assertLess(readme.index("./contributions.sh"), readme.index("whoami"))
        self.assertLess(readme.index("whoami"), readme.index("./links.sh"))
        self.assertIn("docs/activity.md", readme)
        self.assertNotIn("img.shields.io", readme)
        self.assertEqual(readme.count("![Portfolio]"), 1)
        for name in ("portfolio", "neuratile", "linkedin", "email"):
            self.assertIn(f"./assets/link-{name}.svg", readme)
            self.assertTrue((ROOT / f"assets/link-{name}.svg").is_file())
        for evidence in ("48266fa55f46fff88a966aecf88c0b437e1c5704",
                         "6cdbc5b3b0e0432f328451f949e5ab12c9d83fac",
                         "9ec127a71b818296b5ac201a2bfd7e926e69a206",
                         "stop_during_baseline_aborts_before_any_mutant_runs",
                         "arithmetic_operators_form_a_distinct_cycle",
                         "post_jira_comment = false", "not a general ranking",
                         "inclusion does not imply sole authorship"):
            self.assertIn(evidence, companion.lower() if evidence.startswith("inclusion") else companion)

    def test_personal_and_company_websites_preserve_repository_sources(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        companion = (ROOT / "docs/profile-evidence.md").read_text(encoding="utf-8")
        interactive = (ROOT / "docs/execution-atlas.html").read_text(encoding="utf-8")
        for content in (readme, companion, interactive):
            self.assertIn("https://rajveer.codes/", content)
            self.assertIn("https://neuratile.rajveer.codes/", content)
            self.assertNotIn("rajveervadnal.netlify.app", content)
        for content in (companion, interactive):
            self.assertIn("https://github.com/neuratile/Tessera", content)
        for content in (readme, companion):
            self.assertIn("https://rajveer.codes/Rajveer_Vadnal_Resume.pdf", content)

    def test_workflow_tracks_index_and_avoids_generated_commit_loop(self):
        workflow = (ROOT / ".github/workflows/stats.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request:", workflow)
        self.assertIn("python -m unittest discover -s scripts -v", workflow)
        self.assertIn("if: github.event_name != 'pull_request'", workflow)
        ignored = workflow.split("paths-ignore:", 1)[1].split("pull_request:", 1)[0]
        patterns = [line.strip().removeprefix('- "').removesuffix('"') for line in ignored.splitlines() if line.strip()]
        generated = ["assets/contrib-heatmap.svg", "assets/contrib-heatmap-static.svg", "assets/contrib-heatmap-light.svg",
                     "assets/contrib-heatmap-static-light.svg", "assets/stats.svg",
                     "assets/stats-static.svg", "assets/project-index.svg", "docs/public-repositories.md", "docs/activity.md"]
        for path in generated:
            self.assertTrue(any(fnmatch(path, pattern) for pattern in patterns), path)
        self.assertIn("git add assets/contrib-heatmap.svg assets/contrib-heatmap-static.svg assets/contrib-heatmap-light.svg assets/contrib-heatmap-static-light.svg assets/stats.svg assets/stats-static.svg assets/project-index.svg docs/public-repositories.md docs/activity.md", workflow)
        self.assertIn("python scripts/gen_terminal.py --check", workflow)
        self.assertIn("python scripts/gen_profile.py --check", workflow)
        self.assertNotIn("contents: write", workflow.split("  stats:", 1)[0])


if __name__ == "__main__":
    unittest.main()
