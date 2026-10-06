"""Refresh terminal calendar and activity cards from GitHub GraphQL.

GITHUB_TOKEN / GH_TOKEN / existing gh authentication. No third-party image API.
All fetching and SVG validation complete before any existing artwork is replaced.
"""
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import subprocess
import urllib.request

from gen_terminal import USER, activity_markdown, calendar_days, heatmap, stats, variants


def token():
    for key in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(key):
            return os.environ[key]
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise RuntimeError("GitHub authentication required; use gh auth login or GITHUB_TOKEN") from None


def gql(query, variables, auth):
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {auth}", "Content-Type": "application/json",
                 "User-Agent": "rajveer-profile-generator"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors") or not result.get("data"):
        raise RuntimeError("GitHub GraphQL returned errors; keeping the previous artwork")
    return result["data"]


def collect(auth, now):
    end = now.astimezone(timezone.utc)
    # A single calendar window avoids overlapping yearly queries and leap-day bugs.
    start = (end - timedelta(days=365)).replace(hour=0, minute=0, second=0, microsecond=0)
    profile = gql('''
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}''', {"login": USER, "from": start.isoformat(), "to": end.isoformat()}, auth)["user"]
    days = calendar_days(profile["contributionsCollection"]["contributionCalendar"])
    if days[0]["date"] != start.date().isoformat() or days[-1]["date"] != end.date().isoformat():
        raise ValueError("GitHub returned an unexpected calendar window")
    merged = gql('''query($query: String!) {
  search(query: $query, type: ISSUE) { issueCount }
}''', {"query": f"author:{USER} is:pr is:merged is:public"}, auth)["search"]["issueCount"]
    # Paginate every owned public non-fork: do not silently truncate at 100 repos.
    cursor = None
    repos = stars = 0
    while True:
        connection = gql('''query($login: String!, $cursor: String) {
  user(login: $login) {
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      nodes { stargazerCount }
      pageInfo { hasNextPage endCursor }
    }
  }
}''', {"login": USER, "cursor": cursor}, auth)["user"]["repositories"]
        repos += len(connection["nodes"])
        stars += sum(item["stargazerCount"] for item in connection["nodes"])
        page = connection["pageInfo"]
        if not page["hasNextPage"]:
            break
        if not page["endCursor"] or page["endCursor"] == cursor:
            raise RuntimeError("GitHub returned a non-advancing repository cursor")
        cursor = page["endCursor"]
    return {"observed": end.date().isoformat(), "days": days, "merged": merged,
            "repos": repos, "stars": stars, "followers": profile["followers"]["totalCount"]}


def main():
    snapshot = collect(token(), datetime.now(timezone.utc))
    outputs = dict(variants("contrib-heatmap", lambda theme, mobile: heatmap(snapshot["days"], snapshot["observed"], theme, mobile)))
    outputs.update(variants("github-stats", lambda theme, mobile: stats(snapshot, theme, mobile)))
    # Render the accessible text from the identical snapshot before replacing anything.
    documents = {Path("assets", filename): svg for filename, svg in outputs.items()}
    documents[Path("docs/activity.md")] = activity_markdown(snapshot)
    # API/render failures leave the last dated snapshot intact.
    for path, content in documents.items():
        path.parent.mkdir(exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"ok: {sum(item['count'] for item in snapshot['days']):,} calendar contributions; {snapshot['repos']} public non-forks")


if __name__ == "__main__":
    main()
