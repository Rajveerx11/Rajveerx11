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
    ("Contributions", f"{contribs:,}", "all time", "#38bdf8"),
    ("Commits", f"{commits:,}", "all time", "#3fb950"),
    ("Merged PRs", f"{merged}", "public, all time", "#a371f7"),
    ("Stars Earned", f"{stars}", "current", "#e3b341"),
    ("Followers", f"{followers}", "on GitHub", "#ff6b9d"),
    ("Public Repos", f"{repos}", "original", "#38bdf8"),
]

# Left grid: 2 columns x 3 rows of clean metric cards
stat_cards = []
for i, (label, val, note, color) in enumerate(STATS):
    col = i // 3
    row = i % 3
    x = 34 + col * 196
    y = 78 + row * 49

    stat_cards.append(f'''<g transform="translate({x}, {y})">
    <rect width="186" height="43" rx="6" fill="#161b22" stroke="#21262d" stroke-width="1"/>
    <circle cx="12" cy="15" r="3.5" fill="{color}"/>
    <text x="22" y="19" fill="{color}" font-size="16" font-weight="700">{val}</text>
    <text x="22" y="33" fill="#8b949e" font-size="9.5" font-weight="600" letter-spacing="0.6">{label.upper()}</text>
    <text x="176" y="33" text-anchor="end" fill="#4d5866" font-size="8.5">{note}</text>
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
    <text x="{lx}" y="{y+8}" fill="#e6edf3" font-size="10.5">{name}</text>
    <rect x="{bar_x}" y="{y}" width="{bar_w}" height="8" rx="4" fill="#21262d"/>
    <rect x="{bar_x}" y="{y}" width="{fill_w}" height="8" rx="4" fill="{color}"/>
    <text x="{end_x}" y="{y+8}" text-anchor="end" fill="#8b949e" font-size="10">{pct}</text>
  </g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Live GitHub statistics and top languages" font-family="'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="#0d1117" stroke="#26334a" stroke-width="1.5"/>
  <line x1="18" y1="1.5" x2="{W-18}" y2="1.5" stroke="#38bdf8" stroke-width="2" opacity="0.6"/>
  <circle cx="26" cy="22" r="5" fill="#ff5f57"/>
  <circle cx="44" cy="22" r="5" fill="#febc2e"/>
  <circle cx="62" cy="22" r="5" fill="#28c840"/>
  <text x="{W//2}" y="26" text-anchor="middle" fill="#8b949e" font-size="11.5">rajveer@github: ~/stats</text>
  <line x1="1.5" y1="40" x2="{W-1.5}" y2="40" stroke="#26334a" stroke-width="1"/>

  <text x="34" y="60" fill="#3fb950" font-size="11.5">$ <tspan fill="#e6edf3">git</tspan> <tspan fill="#8b949e">stats --live</tspan></text>
  <text x="{lx}" y="60" fill="#8b949e" font-size="10.5" font-weight="600" letter-spacing="0.8">TOP LANGUAGES BY CODE</text>

  <!-- Subtle column divider -->
  <line x1="438" y1="52" x2="438" y2="230" stroke="#21262d" stroke-width="1" stroke-dasharray="3 3"/>

  {"".join(stat_cards)}
  {"".join(bars)}

  <line x1="34" y1="236" x2="{W-34}" y2="236" stroke="#161b22" stroke-width="1"/>
  <text x="34" y="249" fill="#3fb950" font-size="9" letter-spacing="0.5">● <tspan fill="#8b949e">LIVE STATS</tspan></text>
  <text x="{W-34}" y="249" text-anchor="end" fill="#4d5866" font-size="9">auto-generated via GitHub API · refreshed daily</text>
</svg>'''

import xml.dom.minidom
xml.dom.minidom.parseString(svg)
os.makedirs("assets", exist_ok=True)
with open("assets/github-stats.svg", "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
print(f"ok: contribs={contribs} commits={commits} merged={merged} stars={stars} followers={followers} repos={repos} langs={[n for n,_ in top]}")
