"""Generate assets/github-stats.svg from the GitHub GraphQL API.

Runs in CI (GITHUB_TOKEN) or locally (GH_TOKEN / gh auth token).
"""
import json, os, subprocess, urllib.request

USER = "Rajveerx11"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    pullRequests(states: MERGED) { totalCount }
    contributionsCollection {
      contributionCalendar { totalContributions }
      totalCommitContributions
      totalPullRequestReviewContributions
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10) { edges { size node { name color } } }
      }
    }
  }
}
"""

def token():
    for k in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(k):
            return os.environ[k]
    return subprocess.check_output(["gh", "auth", "token"], text=True).strip()

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"},
)
u = json.load(urllib.request.urlopen(req))["data"]["user"]

contribs = u["contributionsCollection"]["contributionCalendar"]["totalContributions"]
commits = u["contributionsCollection"]["totalCommitContributions"]
merged = u["pullRequests"]["totalCount"]
followers = u["followers"]["totalCount"]
repos = u["repositories"]["totalCount"]
stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])

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
    ("contributions", f"{contribs:,}", "past year", "#36bcf7"),
    ("commits", f"{commits:,}", "past year", "#3fb950"),
    ("merged PRs", f"{merged}", "all time", "#a371f7"),
    ("stars earned", f"{stars}", "all time", "#e3b341"),
    ("followers", f"{followers}", "", "#ff6b9d"),
    ("repos", f"{repos}", "original only", "#36bcf7"),
]

rows = []
for i, (label, val, note, color) in enumerate(STATS):
    y = 92 + (i % 3) * 44
    x = 34 + (i // 3) * 200
    note_svg = f'<text x="{x+20}" y="{y+16}" fill="#4d5866" font-size="9.5">{note}</text>' if note else ""
    rows.append(f'''<g>
    <circle cx="{x+6}" cy="{y-14}" r="3.5" fill="{color}"><animate attributeName="opacity" values="1;0.3;1" dur="3s" begin="{i*0.4}s" repeatCount="indefinite"/></circle>
    <text x="{x+20}" y="{y-8}" fill="{color}" font-size="20" font-weight="700">{val}</text>
    <text x="{x+20}" y="{y+4}" fill="#8b949e" font-size="10.5" letter-spacing="1">{label.upper()}</text>
    {note_svg}</g>''')

bars = []
bx, bw = 470, 356
for i, (name, v) in enumerate(top):
    y = 78 + i * 26
    frac = v["size"] / total_size
    w = max(round(bw * frac), 4)
    pct = f"{frac*100:.1f}%"
    bars.append(f'''<g>
    <text x="{bx}" y="{y+9}" fill="#e6edf3" font-size="11">{name}</text>
    <rect x="{bx+96}" y="{y}" width="{bw-96-52}" height="11" rx="5.5" fill="#161e2c"/>
    <rect x="{bx+96}" y="{y}" width="{max(round((bw-96-52)*frac),4)}" height="11" rx="5.5" fill="{v['color']}">
      <animate attributeName="opacity" values="1;0.65;1" dur="4s" begin="{i*0.3}s" repeatCount="indefinite"/>
    </rect>
    <text x="{bx+bw}" y="{y+9}" text-anchor="end" fill="#8b949e" font-size="10.5">{pct}</text></g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="'JetBrains Mono', ui-monospace, SFMono-Regular, monospace">
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="#0d1117" stroke="#26334a" stroke-width="1.5"/>
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="none" stroke="#36bcf7" stroke-width="1.5" stroke-dasharray="90 {2*(W+H)-90}" stroke-linecap="round" opacity="0.85">
    <animate attributeName="stroke-dashoffset" values="0;-{2*(W+H)}" dur="10s" repeatCount="indefinite"/>
  </rect>
  <circle cx="26" cy="24" r="5.5" fill="#ff5f57"/><circle cx="46" cy="24" r="5.5" fill="#febc2e"/><circle cx="66" cy="24" r="5.5" fill="#28c840"/>
  <text x="{W//2}" y="28" text-anchor="middle" fill="#8b949e" font-size="12">rajveer@github: ~/stats</text>
  <line x1="1.5" y1="44" x2="{W-1.5}" y2="44" stroke="#26334a" stroke-width="1"/>
  <text x="34" y="64" fill="#3fb950" font-size="12.5">$ <tspan fill="#e6edf3">git</tspan> <tspan fill="#8b949e">stats --live</tspan></text>
  <text x="{bx}" y="64" fill="#6e7681" font-size="11" letter-spacing="1">TOP LANGUAGES BY CODE</text>
  {"".join(rows)}
  {"".join(bars)}
  <text x="{W-34}" y="{H-16}" text-anchor="end" fill="#4d5866" font-size="10">auto-generated daily from the GitHub API</text>
</svg>'''

import xml.dom.minidom
xml.dom.minidom.parseString(svg)
os.makedirs("assets", exist_ok=True)
with open("assets/github-stats.svg", "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
print(f"ok: contribs={contribs} commits={commits} merged={merged} stars={stars} followers={followers} repos={repos} langs={[n for n,_ in top]}")
