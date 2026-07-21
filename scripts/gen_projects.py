"""Generate assets/project-index.svg from live GitHub data.

Lists all original (non-fork) repos owned by the user plus the neuratile org:
public repos sorted by stars on the left, private on the right with lock marks.
Runs in CI (GITHUB_TOKEN) or locally (gh auth token).
"""
import json, os, subprocess, urllib.request

USER = "Rajveerx11"
ORGS = ["neuratile"]

def token():
    for k in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(k):
            return os.environ[k]
    return subprocess.check_output(["gh", "auth", "token"], text=True).strip()

TOK = token()

def api(path):
    req = urllib.request.Request("https://api.github.com" + path,
                                 headers={"Authorization": f"bearer {TOK}",
                                          "Accept": "application/vnd.github+json"})
    return json.load(urllib.request.urlopen(req))

def collect(path, extra=""):
    out, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        chunk = api(f"{path}{sep}per_page=100&page={page}{extra}")
        if not chunk:
            break
        out += chunk
        if len(chunk) < 100:
            break
        page += 1
    return out

# /user/repos (authenticated) returns private repos; /users/{login}/repos does not.
# Requires a user token that can see them — run locally, not with the CI GITHUB_TOKEN.
repos = collect("/user/repos", "&affiliation=owner&visibility=all")
for org in ORGS:
    repos += collect(f"/orgs/{org}/repos")

LANG = {"TypeScript":"#3178c6","JavaScript":"#f1e05a","Python":"#3572A5","Kotlin":"#A97BFF",
        "HTML":"#e34c26","CSS":"#563d7c","Rust":"#dea584","Go":"#00ADD8","Shell":"#89e051",
        "C++":"#f34b7d","Java":"#b07219","Vue":"#41b883"}

pub, priv = [], []
for r in repos:
    # skip forks, the profile repo, empty repos, and language-less scratch repos
    if r["fork"] or r["name"].lower() == USER.lower() or r["size"] == 0 or not r["language"]:
        continue
    row = (r["name"], r["language"], r["stargazers_count"], r["private"])
    (priv if r["private"] else pub).append(row)

pub.sort(key=lambda x: (-x[2], x[0].lower()))
priv.sort(key=lambda x: x[0].lower())

W, ROW_H, TOP = 860, 26, 78
n_rows = max(len(pub), len(priv))
H = TOP + n_rows * ROW_H + 58

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def row_svg(name, lang, stars, priv_flag, x, y, delay):
    c = LANG.get(lang, "#8b949e")
    p = [f'<g><animate attributeName="opacity" values="0;1" dur="0.5s" begin="{delay}s" fill="freeze"/>']
    p.append(f'<circle cx="{x+6}" cy="{y-4}" r="4" fill="{c}"/>')
    p.append(f'<text x="{x+20}" y="{y}" fill="#e6edf3" font-size="12.5">{esc(name)}</text>')
    tag_x = x + 20 + len(name) * 7.6 + 10
    if stars:
        p.append(f'<text x="{tag_x:.0f}" y="{y}" fill="#e3b341" font-size="11">&#9733; {stars}<animate attributeName="opacity" values="1;0.45;1" dur="3s" begin="{delay}s" repeatCount="indefinite"/></text>')
    if priv_flag:
        p.append(f'<text x="{x+390}" y="{y}" text-anchor="end" fill="#6e7681" font-size="10">&#128274;</text>')
    p.append('</g>')
    return "".join(p)

rows, d = [], 0.5
for i in range(n_rows):
    for col, data in ((0, pub), (1, priv)):
        if i < len(data):
            name, lang, stars, pf = data[i]
            rows.append(row_svg(name, lang, stars, pf, 34 + col * 415, TOP + i * ROW_H, round(d, 2)))
            d += 0.07

# legend from languages actually present
present = []
seen = set()
for name, lang, _, _ in pub + priv:
    if lang in LANG and lang not in seen:
        seen.add(lang); present.append(lang)
lx = 34
legend = []
for lang in present[:6]:
    legend.append(f'<circle cx="{lx}" cy="{H-30}" r="4" fill="{LANG[lang]}"/><text x="{lx+10}" y="{H-26}" fill="#8b949e" font-size="10.5">{lang}</text>')
    lx += 20 + len(lang) * 7.2 + 14

total = len(pub) + len(priv)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="'JetBrains Mono', ui-monospace, SFMono-Regular, monospace">
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="#0d1117" stroke="#26334a" stroke-width="1.5"/>
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="none" stroke="#36bcf7" stroke-width="1.5" stroke-dasharray="90 {2*(W+H)-90}" stroke-linecap="round" opacity="0.85">
    <animate attributeName="stroke-dashoffset" values="0;-{2*(W+H)}" dur="10s" repeatCount="indefinite"/>
  </rect>
  <circle cx="26" cy="24" r="5.5" fill="#ff5f57"/><circle cx="46" cy="24" r="5.5" fill="#febc2e"/><circle cx="66" cy="24" r="5.5" fill="#28c840"/>
  <text x="{W//2}" y="28" text-anchor="middle" fill="#8b949e" font-size="12">rajveer@github: ~/projects</text>
  <line x1="1.5" y1="44" x2="{W-1.5}" y2="44" stroke="#26334a" stroke-width="1"/>
  <text x="34" y="64" fill="#3fb950" font-size="12.5">$ <tspan fill="#e6edf3">ls</tspan> <tspan fill="#8b949e">--all --sort=stars</tspan></text>
  <text x="449" y="64" fill="#6e7681" font-size="11" letter-spacing="1">&#128274; PRIVATE BUILDS</text>
  {"".join(rows)}
  {"".join(legend)}
  <text x="{W-34}" y="{H-26}" text-anchor="end" fill="#8b949e" font-size="11.5">{total} projects &#183; {len(pub)} public &#183; {len(priv)} private &#183; still counting</text>
  <rect x="{W-26}" y="{H-36}" width="7" height="13" fill="#36bcf7">
    <animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>
</svg>'''

import xml.dom.minidom
xml.dom.minidom.parseString(svg)
os.makedirs("assets", exist_ok=True)
with open("assets/project-index.svg", "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
print(f"ok: {total} projects, {len(pub)} public, {len(priv)} private; langs={present[:6]}")
