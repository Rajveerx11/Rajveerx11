"""Generate assets/project-index.svg from live public data and an explicit private allowlist.

Public repositories come from GitHub's public user/org APIs. Private repository names are
read only from data/private-projects.json, so CI needs no broad personal token and a newly
created private repository can never be disclosed accidentally.
"""
import json
import os
import subprocess
import urllib.request
from pathlib import Path

USER = "Rajveerx11"
ORGS = ["neuratile"]
PRIVATE_MANIFEST = Path("data/private-projects.json")


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
    if repo["fork"] or repo["name"].lower() == USER.lower() or repo["size"] == 0 or not repo["language"]:
        continue
    public.append({
        "name": repo["name"],
        "language": repo["language"],
        "stars": repo["stargazers_count"],
        "private": False,
        "pushed": repo.get("pushed_at") or "",
    })

# Strong public proof first; among equal-star projects, show recent work first.
public.sort(key=lambda item: (item["stars"], item["pushed"]), reverse=True)

with PRIVATE_MANIFEST.open(encoding="utf-8") as manifest_file:
    private = [
        {"name": item["name"], "language": item["language"], "stars": 0, "private": True, "pushed": ""}
        for item in json.load(manifest_file)
        if item.get("name") and item.get("language")
    ]

LANG = {
    "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Python": "#3572A5",
    "Kotlin": "#A97BFF", "HTML": "#e34c26", "CSS": "#563d7c", "Rust": "#dea584",
    "Go": "#00ADD8", "Shell": "#89e051", "C++": "#f34b7d", "Java": "#b07219",
    "Vue": "#41b883",
}

W, ROW_H, TOP = 860, 26, 78
n_rows = max(len(public), len(private))
H = TOP + n_rows * ROW_H + 58


def esc(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def row_svg(item, x, y, delay):
    color = LANG.get(item["language"], "#8b949e")
    parts = [f'<g><animate attributeName="opacity" values="0;1" dur="0.5s" begin="{delay}s" fill="freeze"/>']
    parts.append(f'<circle cx="{x+6}" cy="{y-4}" r="4" fill="{color}"/>')
    parts.append(f'<text x="{x+20}" y="{y}" fill="#e6edf3" font-size="12.5">{esc(item["name"])}</text>')
    tag_x = x + 20 + len(item["name"]) * 7.6 + 10
    if item["stars"]:
        parts.append(f'<text x="{tag_x:.0f}" y="{y}" fill="#e3b341" font-size="11">&#9733; {item["stars"]}<animate attributeName="opacity" values="1;0.45;1" dur="3s" begin="{delay}s" repeatCount="indefinite"/></text>')
    if item["private"]:
        parts.append(f'<text x="{x+390}" y="{y}" text-anchor="end" fill="#6e7681" font-size="10">&#128274;</text>')
    parts.append("</g>")
    return "".join(parts)


rows, delay = [], 0.5
for index in range(n_rows):
    for column, items in ((0, public), (1, private)):
        if index < len(items):
            rows.append(row_svg(items[index], 34 + column * 415, TOP + index * ROW_H, round(delay, 2)))
            delay += 0.07

present, seen_languages = [], set()
for item in public + private:
    language = item["language"]
    if language in LANG and language not in seen_languages:
        seen_languages.add(language)
        present.append(language)

legend, legend_x = [], 34
for language in present[:6]:
    legend.append(f'<circle cx="{legend_x}" cy="{H-30}" r="4" fill="{LANG[language]}"/><text x="{legend_x+10}" y="{H-26}" fill="#8b949e" font-size="10.5">{language}</text>')
    legend_x += 20 + len(language) * 7.2 + 14

total = len(public) + len(private)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="'JetBrains Mono', ui-monospace, SFMono-Regular, monospace">
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="#0d1117" stroke="#26334a" stroke-width="1.5"/>
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="none" stroke="#36bcf7" stroke-width="1.5" stroke-dasharray="90 {2*(W+H)-90}" stroke-linecap="round" opacity="0.85">
    <animate attributeName="stroke-dashoffset" values="0;-{2*(W+H)}" dur="10s" repeatCount="indefinite"/>
  </rect>
  <circle cx="26" cy="24" r="5.5" fill="#ff5f57"/><circle cx="46" cy="24" r="5.5" fill="#febc2e"/><circle cx="66" cy="24" r="5.5" fill="#28c840"/>
  <text x="{W//2}" y="28" text-anchor="middle" fill="#8b949e" font-size="12">rajveer@github: ~/projects</text>
  <line x1="1.5" y1="44" x2="{W-1.5}" y2="44" stroke="#26334a" stroke-width="1"/>
  <text x="34" y="64" fill="#3fb950" font-size="12.5">$ <tspan fill="#e6edf3">portfolio</tspan> <tspan fill="#8b949e">--public</tspan></text>
  <text x="449" y="64" fill="#6e7681" font-size="11" letter-spacing="1">&#128274; SELECTED PRIVATE BUILDS</text>
  {"".join(rows)}
  {"".join(legend)}
  <text x="{W-34}" y="{H-26}" text-anchor="end" fill="#8b949e" font-size="11.5">{total} projects &#183; {len(public)} public &#183; {len(private)} selected private</text>
  <rect x="{W-26}" y="{H-36}" width="7" height="13" fill="#36bcf7"><animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></rect>
</svg>'''

import xml.dom.minidom
xml.dom.minidom.parseString(svg)
Path("assets").mkdir(exist_ok=True)
Path("assets/project-index.svg").write_text(svg + "\n", encoding="utf-8", newline="\n")
print(f"ok: {total} projects, {len(public)} public, {len(private)} selected private; langs={present[:6]}")
