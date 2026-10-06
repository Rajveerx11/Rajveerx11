"""Offline regressions for fetching, presentation, and failure preservation."""
from datetime import datetime, timedelta, timezone
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import gen_stats
from gen_terminal import calendar_days, heatmap, hero, stats, streaks, variants
from gen_profile import activity_markdown, card, graph, metrics, monthly, number


class StatsTest(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 6, 12, tzinfo=timezone.utc)
        start = self.now.date() - timedelta(days=365)
        self.days = [{"date": (start + timedelta(days=i)).isoformat(), "count": int(i % 3 != 0)} for i in range(366)]
        self.calendar = {"totalContributions": sum(item["count"] for item in self.days),
                         "weeks": [{"contributionDays": [{"date": item["date"], "contributionCount": item["count"]} for item in self.days]}]}
        self.snapshot = {"observed": "2026-10-06", "days": self.days, "merged": 4, "repos": 2, "stars": 8, "followers": 2}

    def fake_urlopen(self, request, timeout):
        self.assertEqual(timeout, 30)
        payload = json.loads(request.data)
        query = payload["query"]
        if "contributionsCollection" in query:
            data = {"user": {"followers": {"totalCount": 2}, "contributionsCollection": {"contributionCalendar": self.calendar}}}
        elif "search(" in query:
            self.assertIn("is:public", payload["variables"]["query"])
            data = {"search": {"issueCount": 4}}
        else:
            self.assertIn("privacy: PUBLIC", query)
            self.assertIn("isFork: false", query)
            self.assertIn("ownerAffiliations: OWNER", query)
            cursor = payload["variables"]["cursor"]
            data = {"user": {"repositories": {"nodes": [{"stargazerCount": 3 if cursor is None else 5}],
                                               "pageInfo": {"hasNextPage": cursor is None, "endCursor": "next"}}}}
        return io.BytesIO(json.dumps({"data": data}).encode())

    def test_public_filters_pagination_and_window(self):
        with patch("urllib.request.urlopen", side_effect=self.fake_urlopen):
            snapshot = gen_stats.collect("test", self.now)
        self.assertEqual(snapshot, self.snapshot)

    def test_variants_valid_and_accessible(self):
        for name, render in [("profile", hero),
                             ("calendar", lambda theme, mobile: heatmap(self.days, "2026-10-06", theme, mobile)),
                             ("stats", lambda theme, mobile: stats(self.snapshot, theme, mobile))]:
            outputs = list(variants(name, render))
            self.assertEqual(len(outputs), 4)
            for filename, svg in outputs:
                with self.subTest(filename=filename):
                    root = ET.fromstring(svg)
                    self.assertEqual(root.attrib["role"], "img")
                    self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}title"))
                    self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}desc"))
                    self.assertNotIn("<script", svg)
                    self.assertNotIn("http://", svg.replace("http://www.w3.org/2000/svg", ""))
                    if name != "profile":
                        self.assertIn("snapshot 2026-10-06 UTC", svg)
                    if name == "calendar":
                        self.assertEqual(svg.count('class="cell"'), 366)
                        self.assertIn("prefers-reduced-motion", svg)
                        self.assertNotIn("opacity:0", svg)

    def test_accessible_text_matches_every_metric_and_calendar_day(self):
        markdown = activity_markdown(self.snapshot)
        svg = card(self.snapshot)
        self.assertIn("2026-10-06 UTC", markdown)
        self.assertIn("**244**", markdown)
        self.assertIn("2025-10-06 through 2026-10-06", markdown)
        for label, value, suffix, caption, _ in metrics(self.snapshot):
            formatted = number(value, value)
            self.assertIn(f"| {label} | {formatted}{suffix} | {caption} |", markdown)
            self.assertIn(formatted, svg)
        for month, total in monthly(self.days):
            self.assertIn(f"| {month} | {total} |", markdown)
            self.assertIn(f"{month}: {total} contributions", svg)
        for day in self.days:
            self.assertIn(f"| {day['date']} | {day['count']} |", markdown)

    def test_calendar_partial_week_is_aligned_to_sunday(self):
        days = [{"date": "2026-10-06", "count": 1}, {"date": "2026-10-07", "count": 2}]
        svg = graph({"days": days, "observed": "2026-10-07"})
        root = ET.fromstring(svg)
        cells = [node for node in root.iter() if node.attrib.get("class") == "cell"]
        self.assertEqual([node.attrib["y"] for node in cells], ["56", "72"])

    def test_github_levels_preserved_and_invalid_levels_rejected(self):
        calendar = {"totalContributions": 1, "weeks": [{"contributionDays": [
            {"date": "2026-10-06", "contributionCount": 1, "contributionLevel": "FIRST_QUARTILE"}]}]}
        self.assertEqual(calendar_days(calendar)[0]["level"], 1)
        for level in ("INVALID", "NONE"):
            calendar["weeks"][0]["contributionDays"][0]["contributionLevel"] = level
            with self.assertRaises(ValueError):
                calendar_days(calendar)

    def test_streak_grace_only_for_today_and_stale_snapshots(self):
        days = [{"date": f"2026-10-0{i}", "count": count} for i, count in enumerate([1, 1, 0], 1)]
        self.assertEqual(streaks(days, "2026-10-03"), (2, 2))
        self.assertEqual(streaks(days, "2026-10-04"), (0, 2))
        self.assertEqual(streaks(days[:2], "2026-10-06"), (0, 2))
        self.assertEqual(streaks([], "2026-10-06"), (0, 0))

    def test_invalid_calendar_rejected(self):
        for calendar in [{"totalContributions": 0, "weeks": []},
                         {"totalContributions": 0, "weeks": [{"contributionDays": [{"date": "2026-10-06", "contributionCount": -1}]}]},
                         {"totalContributions": 1, "weeks": [{"contributionDays": [{"date": "2026-10-06", "contributionCount": 0}]}]},
                         {"totalContributions": 0, "weeks": [{"contributionDays": [{"date": "2026-10-06", "contributionCount": 0}, {"date": "2026-10-08", "contributionCount": 0}]}]}]:
            with self.subTest(calendar=calendar), self.assertRaises(ValueError):
                calendar_days(calendar)

    def test_graphql_error_fetch_and_render_failures_preserve_all_active_outputs(self):
        with patch("urllib.request.urlopen", return_value=io.BytesIO(b'{"errors":[{"message":"test"}]}')):
            with self.assertRaises(RuntimeError):
                gen_stats.gql("query", {}, "test")
        with tempfile.TemporaryDirectory() as folder:
            previous = Path.cwd()
            try:
                os.chdir(folder)
                outputs = [Path("assets", filename) for filename in (
                    "contrib-heatmap.svg", "contrib-heatmap-static.svg", "contrib-heatmap-light.svg",
                    "contrib-heatmap-static-light.svg", "stats.svg", "stats-static.svg")]
                outputs.append(Path("docs/activity.md"))
                for output in outputs:
                    output.parent.mkdir(exist_ok=True)
                    output.write_text("previous dated output", encoding="utf-8")
                for phase in ("fetch", "render"):
                    with self.subTest(phase=phase), patch("gen_stats.token", return_value="test"), \
                         patch("gen_stats.collect", return_value=self.snapshot, side_effect=RuntimeError("offline") if phase == "fetch" else None), \
                         patch("gen_stats.card", side_effect=RuntimeError("render failed") if phase == "render" else card):
                        with self.assertRaises(RuntimeError):
                            gen_stats.main()
                    for output in outputs:
                        self.assertEqual(output.read_text(encoding="utf-8"), "previous dated output")
            finally:
                os.chdir(previous)

    def test_main_writes_reference_graph_card_and_equivalent_text(self):
        with tempfile.TemporaryDirectory() as folder:
            previous = Path.cwd()
            try:
                os.chdir(folder)
                with patch("gen_stats.token", return_value="test"), patch("gen_stats.collect", return_value=self.snapshot):
                    gen_stats.main()
                self.assertEqual({path.name for path in Path("assets").glob("*.svg")}, {"stats.svg", "stats-static.svg", "contrib-heatmap.svg", "contrib-heatmap-static.svg", "contrib-heatmap-light.svg", "contrib-heatmap-static-light.svg"})
                self.assertEqual(Path("docs/activity.md").read_text(encoding="utf-8"), activity_markdown(self.snapshot))
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
