"""Offline smoke regression for the activity snapshot presentation."""
import io
import json
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).with_name("gen_stats.py")


class StatsTest(unittest.TestCase):
    def test_snapshot_labels_and_public_query(self):
        queries = []

        def fake_urlopen(request):
            query = json.loads(request.data)["query"]
            queries.append(query)
            if "createdAt" in query:
                data = {"user": {"createdAt": "2025-01-01T00:00:00Z", "followers": {"totalCount": 2},
                                  "repositories": {"totalCount": 1, "nodes": [{"stargazerCount": 3,
                                  "languages": {"edges": [{"size": 100, "node": {"name": "Python", "color": "#3572A5"}}]}}]}}}
            elif "search(" in query:
                self.assertIn("is:public", json.loads(request.data)["variables"]["query"])
                data = {"search": {"issueCount": 4}}
            else:
                data = {"user": {"contributionsCollection": {"contributionCalendar": {"totalContributions": 5}, "totalCommitContributions": 6}}}
            return io.BytesIO(json.dumps({"data": data}).encode())

        with tempfile.TemporaryDirectory() as folder, patch("urllib.request.urlopen", side_effect=fake_urlopen), patch.dict(os.environ, {"GITHUB_TOKEN": "test"}):
            previous = Path.cwd()
            try:
                os.chdir(folder)
                runpy.run_path(str(SCRIPT))
                svg = Path("assets/github-stats.svg").read_text(encoding="utf-8")
            finally:
                os.chdir(previous)
        ET.fromstring(svg)
        self.assertIn("GitHub activity snapshot", svg)
        self.assertIn("Snapshot ", svg)
        self.assertIn("Byte share within displayed top languages", svg)
        self.assertIn("privacy: PUBLIC", queries[0])
        self.assertIn("isFork: false", queries[0])
        self.assertNotIn("LIVE STATS", svg)
        self.assertNotIn("stats --live", svg)
        self.assertNotIn("#ff5f57", svg)


if __name__ == "__main__":
    unittest.main()
