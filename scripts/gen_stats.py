"""Generate assets/github-stats.svg from the GitHub GraphQL API.

Runs in CI (GITHUB_TOKEN) or locally (GH_TOKEN / gh auth token).
"""
import json, os, subprocess, urllib.request
from datetime import datetime, timezone

USER = "Rajveerx11"

def token():
    for k in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(k):
            return os.environ[k]
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception:
        return ""

TOK = token()

def gql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOK}", "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req))["data"]

# base profile numbers
u = gql("""
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10) { edges { size node { name color } } }
      }
    }
  }
}""", {"login": USER})["user"]

# Explicit public filter keeps local owner tokens and CI scoped tokens consistent.
merged = gql("""
query($query: String!) {
  search(query: $query, type: ISSUE) { issueCount }
}
""", {"query": f"author:{USER} is:pr is:merged is:public"})["search"]["issueCount"]
followers = u["followers"]["totalCount"]
repos = u["repositories"]["totalCount"]
stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])

# All-time contributions
created = datetime.strptime(u["createdAt"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
now = datetime.now(timezone.utc)
contribs = commits = 0
start = created
while start < now:
    end = min(start.replace(year=start.year + 1), now)
    c = gql("""
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar { totalContributions }
          totalCommitContributions
        }
      }
    }""", {"login": USER, "from": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
           "to": end.strftime("%Y-%m-%dT%H:%M:%SZ")})["user"]["contributionsCollection"]
    contribs += c["contributionCalendar"]["totalContributions"]
    commits += c["totalCommitContributions"]
    start = end

langs = {}
for n in u["repositories"]["nodes"]:
    for e in n["languages"]["edges"]:
        name = e["node"]["name"]
        langs.setdefault(name, {"size": 0, "color": e["node"]["color"] or "#8b949e"})
        langs[name]["size"] += e["size"]
top = sorted(langs.items(), key=lambda kv: -kv[1]["size"])[:6]
total_size = sum(v["size"] for _, v in top) or 1

W, H = 860, 260
STATS = [
    ("Contributions", f"{contribs:,}", "all time", "#ef9773"),
    ("Commits", f"{commits:,}", "all time", "#ef9773"),
    ("Merged PRs", f"{merged}", "public, all time", "#ef9773"),
    ("Stars Earned", f"{stars}", "at refresh", "#ef9773"),
    ("Followers", f"{followers}", "at refresh", "#ef9773"),
    ("Public Repos", f"{repos}", "non-forks", "#ef9773"),
]

# Left grid: 2 columns x 3 rows of clean metric cards
stat_cards = []
for i, (label, val, note, color) in enumerate(STATS):
    col = i // 3
    row = i % 3
    x = 34 + col * 196
    y = 78 + row * 49

    stat_cards.append(f'''<g transform="translate({x}, {y})">
    <rect width="186" height="43" rx="3" fill="#191c1a" stroke="#363c35" stroke-width="1"/>
    <text x="12" y="19" fill="{color}" font-size="16">{val}</text>
    <text x="12" y="33" fill="#adb3a9" font-size="9.5">{label}</text>
    <text x="176" y="33" text-anchor="end" fill="#adb3a9" font-size="8.5">{note}</text>
  </g>''')

# Right grid: Top languages with clear labels, full-width background tracks, and accurate fill bars
bars = []
lx = 462
bar_x = 598
bar_w = 172
end_x = 826

for i, (name, v) in enumerate(top):
    y = 80 + i * 25
    frac = v["size"] / total_size
    fill_w = max(round(bar_w * frac), 4)
    pct = f"{frac*100:.1f}%"
    color = v["color"]

    bars.append(f'''<g>
    <text x="{lx}" y="{y+8}" fill="#eeeae1" font-size="10.5">{name}</text>
    <rect x="{bar_x}" y="{y}" width="{bar_w}" height="8" rx="3" fill="#363c35"/>
    <rect x="{bar_x}" y="{y}" width="{fill_w}" height="8" rx="3" fill="{color}"/>
    <text x="{end_x}" y="{y+8}" text-anchor="end" fill="#adb3a9" font-size="10">{pct}</text>
  </g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc" font-family="ui-monospace, Consolas, monospace">
  <title id="title">GitHub activity snapshot</title>
  <desc id="desc">GitHub API activity totals and language byte shares within the displayed top languages. Refreshed daily, not live telemetry.</desc>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="5" fill="#131514" stroke="#363c35"/>
  <text x="34" y="32" fill="#eeeae1" font-size="20" font-family="Segoe UI, Arial, sans-serif">GitHub activity snapshot</text>
  <line x1="1" y1="44" x2="{W-1}" y2="44" stroke="#363c35"/>
  <text x="34" y="62" fill="#adb3a9" font-size="11">Recorded GitHub API totals</text>
  <text x="{lx}" y="62" fill="#adb3a9" font-size="10.5">Byte share within displayed top languages</text>
  <line x1="438" y1="52" x2="438" y2="230" stroke="#363c35" stroke-dasharray="3 3"/>
  {"".join(stat_cards)}
  {"".join(bars)}
  <line x1="34" y1="236" x2="{W-34}" y2="236" stroke="#363c35"/>
  <text x="34" y="249" fill="#adb3a9" font-size="9">Snapshot {now.strftime('%Y-%m-%d')} UTC</text>
  <text x="{W-34}" y="249" text-anchor="end" fill="#adb3a9" font-size="9">GitHub API · refreshed daily</text>
</svg>'''

import xml.dom.minidom
xml.dom.minidom.parseString(svg)
os.makedirs("assets", exist_ok=True)
with open("assets/github-stats.svg", "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
print(f"ok: contribs={contribs} commits={commits} merged={merged} stars={stars} followers={followers} repos={repos} langs={[n for n,_ in top]}")
