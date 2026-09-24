"""Generate assets/project-index.svg from live public GitHub data.

Only public repositories from the user and associated orgs are displayed.
"""
import json
import os
import subprocess
import urllib.request
from pathlib import Path

USER = "Rajveerx11"
ORGS = ["neuratile", "Government-Polytechnic-Solapur"]


def token():
    for key in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(key):
            return os.environ[key]
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return ""


TOK = token()


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-index-generator"}
    if TOK:
        headers["Authorization"] = f"bearer {TOK}"
    request = urllib.request.Request("https://api.github.com" + path, headers=headers)
    return json.load(urllib.request.urlopen(request))


def collect(path, extra=""):
    output, page = [], 1
    while True:
        separator = "&" if "?" in path else "?"
        chunk = api(f"{path}{separator}per_page=100&page={page}{extra}")
        if not chunk:
            break
        output += chunk
        if len(chunk) < 100:
            break
        page += 1
    return output


repositories = collect(f"/users/{USER}/repos", "&type=owner&sort=updated")
for org in ORGS:
    repositories += collect(f"/orgs/{org}/repos", "&type=public&sort=updated")

public = []
seen = set()
for repo in repositories:
    full_name = repo["full_name"].lower()
    if full_name in seen:
        continue
    seen.add(full_name)
    if repo.get("private") is not False or repo.get("fork") or repo["name"].lower() == USER.lower():
        continue
    public.append({
        "name": repo["name"],
        "language": repo.get("language") or "Other",
        "stars": repo.get("stargazers_count", 0),
        "pushed": repo.get("pushed_at") or "",
    })

# Strong public proof first: stars descending, then most recent push
public.sort(key=lambda item: (item["stars"], item["pushed"]), reverse=True)

LANG = {
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "Python": "#3572A5",
    "Rust": "#dea584",
    "Kotlin": "#A97BFF",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Jupyter Notebook": "#DA5B0B",
    "PLpgSQL": "#336790",
    "Go": "#00ADD8",
    "Shell": "#89e051",
    "C++": "#f34b7d",
    "Java": "#b07219",
    "Vue": "#41b883",
}

W = 860
ROW_H = 27
TOP = 78

# Split public repos evenly into 2 columns
n_rows = max((len(public) + 1) // 2, 1)
col0 = public[:n_rows]
col1 = public[n_rows:]

H = TOP + n_rows * ROW_H + 54


def esc(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def row_svg(item, x, y):
    color = LANG.get(item["language"], "#8b949e")
    # Leave room for the star count and the right-aligned language label.
    limit = 28 if item["stars"] else 34
    display_name = item["name"][:limit] + ("…" if len(item["name"]) > limit else "")
    name = esc(display_name)

    parts = ["<g>"]
    parts.append(f'<circle cx="{x+6}" cy="{y-4}" r="3.5" fill="{color}"/>')
    parts.append(f'<text x="{x+18}" y="{y}" fill="#e6edf3" font-size="12">{name}</text>')

    star_x = x + 18 + len(display_name) * 7.3 + 8
    if item["stars"]:
        parts.append(f'<text x="{star_x:.0f}" y="{y}" fill="#e3b341" font-size="10.5">&#9733; {item["stars"]}</text>')

    # Language tag right aligned in this column
    col_end = x + 380
    parts.append(f'<text x="{col_end}" y="{y}" text-anchor="end" fill="#6e7681" font-size="10">{esc(item["language"])}</text>')
    parts.append("</g>")
    return "".join(parts)


rows = []
for idx in range(n_rows):
    y = TOP + idx * ROW_H
    if idx < len(col0):
        rows.append(row_svg(col0[idx], 34, y))
    if idx < len(col1):
        rows.append(row_svg(col1[idx], 446, y))

present = []
seen_languages = set()
for item in public:
    lang = item["language"]
    if lang in LANG and lang not in seen_languages:
        seen_languages.add(lang)
        present.append(lang)

legend = []
legend_x = 34
for language in present[:5]:
    legend.append(
        f'<circle cx="{legend_x}" cy="{H-22}" r="3.5" fill="{LANG[language]}"/>'
        f'<text x="{legend_x+8}" y="{H-19}" fill="#8b949e" font-size="10">{language}</text>'
    )
    legend_x += 16 + len(language) * 6.5 + 12

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Index of public open source repositories" font-family="'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="#0d1117" stroke="#26334a" stroke-width="1.5"/>
  <line x1="18" y1="1.5" x2="{W-18}" y2="1.5" stroke="#38bdf8" stroke-width="2" opacity="0.6"/>
  <circle cx="26" cy="22" r="5" fill="#ff5f57"/>
  <circle cx="44" cy="22" r="5" fill="#febc2e"/>
  <circle cx="62" cy="22" r="5" fill="#28c840"/>
  <text x="{W//2}" y="26" text-anchor="middle" fill="#8b949e" font-size="11.5">rajveer@github: ~/projects</text>
  <line x1="1.5" y1="40" x2="{W-1.5}" y2="40" stroke="#26334a" stroke-width="1"/>

  <text x="34" y="60" fill="#3fb950" font-size="11.5">$ <tspan fill="#e6edf3">portfolio</tspan> <tspan fill="#8b949e">--public</tspan></text>
  <text x="{W-34}" y="60" text-anchor="end" fill="#8b949e" font-size="10.5" font-weight="600" letter-spacing="0.8">PUBLIC REPOSITORIES</text>

  <!-- Subtle column divider -->
  <line x1="430" y1="52" x2="430" y2="{TOP + n_rows * ROW_H - 4}" stroke="#21262d" stroke-width="1" stroke-dasharray="3 3"/>

  {"".join(rows)}

  <line x1="34" y1="{H-36}" x2="{W-34}" y2="{H-36}" stroke="#161b22" stroke-width="1"/>
  {"".join(legend)}
  <text x="{W-34}" y="{H-19}" text-anchor="end" fill="#8b949e" font-size="10.5">{len(public)} public repositories · indexed daily</text>
</svg>'''

import xml.dom.minidom
xml.dom.minidom.parseString(svg)
Path("assets").mkdir(exist_ok=True)
Path("assets/project-index.svg").write_text(svg + "\n", encoding="utf-8", newline="\n")
print(f"ok: {len(public)} public projects; langs={present[:5]}")
