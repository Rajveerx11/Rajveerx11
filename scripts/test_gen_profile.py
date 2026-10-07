"""Offline reference-layout, portrait safety, and contribution-card regressions."""
from datetime import date, timedelta
import json
import unittest
import xml.etree.ElementTree as ET

from gen_profile import LINK_BUTTONS, PORTRAIT_DATA, ROOT, activity_markdown, card, graph, link_button, metrics, monthly, portrait, static_svg, validate_rows

NS = "{http://www.w3.org/2000/svg}"


class ProfileTest(unittest.TestCase):
    def setUp(self):
        self.snapshot = {"observed": "2026-10-06", "days": [
            {"date": (date(2026, 9, 30) + timedelta(days=i)).isoformat(), "count": count, "level": level}
            for i, (count, level) in enumerate([(2, 1), (0, 0), (4, 2), (4, 2), (0, 0), (1, 1), (0, 0)])],
            "merged": 1, "repos": 2, "stars": 3, "followers": 4}

    def test_portrait_reproduces_frozen_rows_without_raw_photo(self):
        data = json.loads(PORTRAIT_DATA.read_text(encoding="utf-8"))
        self.assertEqual(set(data), {"columns", "rows"})
        self.assertEqual(data["columns"], 180)
        self.assertEqual(len(validate_rows(data)), 96)
        output = portrait(data)
        self.assertEqual(output, (ROOT / "assets/rajveer-ascii.svg").read_text(encoding="utf-8"))
        root = ET.fromstring(output)
        self.assertEqual(root.attrib["viewBox"], "0 0 840 880")
        rows = [node for node in root.iter(NS + "text") if node.attrib.get("class") == "ascii-row"]
        self.assertEqual([node.text for node in rows], data["rows"])
        self.assertEqual(output.count('class="scan-cursor"'), 96)
        self.assertIn("prefers-reduced-motion", output)
        self.assertIn("then remain visible", output)
        self.assertNotIn("Portfolio Photo", output)
        self.assertNotIn("<image", output)
        self.assertNotIn("base64", output)
        self.assertNotIn("<script", output)
        self.assertNotIn("<foreignObject", output)
        self.assertNotIn("avi@", output)

    def test_static_sources_are_frozen_equivalents(self):
        data = json.loads(PORTRAIT_DATA.read_text(encoding="utf-8"))
        pairs = [("rajveer-ascii-static.svg", portrait(data)),
                 (None, graph(self.snapshot)), (None, card(self.snapshot))]
        for filename, animated in pairs:
            frozen = static_svg(animated)
            self.assertNotIn("<style>", frozen)
            self.assertNotIn("<animate", frozen)
            self.assertNotIn("<script", frozen)
            root = ET.fromstring(frozen)
            self.assertEqual(len(list(root.iter(NS + "text"))), len(list(ET.fromstring(animated).iter(NS + "text"))))
            if filename:
                self.assertEqual(frozen, (ROOT / "assets" / filename).read_text(encoding="utf-8"))

    def test_terminal_links_are_equal_sized_local_and_reproducible(self):
        self.assertEqual(len(LINK_BUTTONS), 4)
        self.assertEqual(sum(primary for _, _, _, primary in LINK_BUTTONS), 1)
        for name, label, description, primary in LINK_BUTTONS:
            output = link_button(label, description, primary)
            self.assertEqual(output, (ROOT / f"assets/link-{name}.svg").read_text(encoding="utf-8"))
            root = ET.fromstring(output)
            self.assertEqual(root.attrib["viewBox"], "0 0 132 44")
            self.assertEqual(root.find(NS + "title").text, label)
            self.assertEqual(root.find(NS + "desc").text, description)
            self.assertNotIn("<style>", output)
            self.assertNotIn("<script", output)
            self.assertNotIn("href=", output)
            self.assertNotIn("<image", output)

    def test_unsafe_or_malformed_rows_fail_closed(self):
        for data in ({"columns": 39, "rows": [" " * 39] * 96},
                     {"columns": 40, "rows": [" " * 39] * 96},
                     {"columns": 40, "rows": ["\n" + " " * 39] * 96},
                     {"columns": 40, "rows": []}):
            with self.subTest(data=data["columns"]), self.assertRaises(ValueError):
                validate_rows(data)
        data = {"columns": 40, "rows": ["<>&" + " " * 37] * 20}
        output = portrait(data)
        self.assertIn("&lt;&gt;&amp;", output)
        ET.fromstring(output)

    def test_card_metrics_months_and_static_fallback(self):
        values = metrics(self.snapshot)
        self.assertEqual([item[1] for item in values[:5]], [1, 2, 11, 4, 4])
        self.assertEqual(values[4][3], "2026-10-02")
        self.assertEqual(values[5][1], 2.75)
        self.assertEqual(monthly(self.snapshot["days"]), [("2026-09", 2), ("2026-10", 9)])
        output = card(self.snapshot)
        root = ET.fromstring(output)
        self.assertEqual(root.attrib["viewBox"], "0 0 840 880")
        self.assertEqual(output.count('class="counter-final"'), 6)
        self.assertEqual(output.count('class="bar"'), 2)
        self.assertIn("prefers-reduced-motion", output)
        self.assertIn(".counter-step { display: none; }", output)
        finals = [node for node in root.iter(NS + "text") if node.attrib.get("class") == "counter-final"]
        self.assertTrue(all(node.attrib.get("opacity") == "1" for node in finals))
        self.assertIn("snapshot 2026-10-06 UTC", output)
        self.assertIn("2.8", output)

    def test_graph_uses_actual_levels_and_dates(self):
        output = graph(self.snapshot)
        root = ET.fromstring(output)
        cells = [node for node in root.iter(NS + "rect") if node.attrib.get("class") == "cell"]
        self.assertEqual(len(cells), 7)
        self.assertEqual([node.attrib["fill"] for node in cells], ["#0e4429", "#161b22", "#006d32", "#006d32", "#161b22", "#0e4429", "#161b22"])
        self.assertEqual(cells[0].attrib["y"], "72")  # Wednesday, Sunday-first calendar.
        self.assertIn("2026-09-30: 2 contributions", output)
        self.assertIn("11 contributions", output)
        self.assertIn('fill="#24292f"', graph(self.snapshot, light=True))
        self.assertIn("prefers-reduced-motion", output)

    def test_zero_activity_has_zero_average_and_no_invented_bar(self):
        for day in self.snapshot["days"]:
            day.update(count=0, level=0)
        self.assertEqual(metrics(self.snapshot)[5][1], 0)
        output = card(self.snapshot)
        self.assertIn('height="0.000"', output)
        self.assertIn("| avg / active day | 0 |", activity_markdown(self.snapshot))
        ET.fromstring(output)


if __name__ == "__main__":
    unittest.main()
