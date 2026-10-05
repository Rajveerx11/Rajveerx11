"""Generate a public-only SVG catalog and a readable, linked Markdown index."""
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import subprocess
from urllib.parse import quote
import urllib.request

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
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


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


def public_projects(repositories):
    public, seen = [], set()
    for repo in repositories:
        full_name = repo["full_name"].lower()
        if full_name in seen:
            continue
        seen.add(full_name)
        # Fail closed: authenticated owner responses must not expose private or unknown data.
        if repo.get("private") is not False or full_name == f"{USER}/{USER}".lower():
            continue
        public.append({
            "name": repo["name"], "full_name": repo["full_name"],
            "language": repo.get("language") or "Not reported",
            "description": repo.get("description") or "No public description supplied.",
            "stars": repo.get("stargazers_count", 0), "pushed": repo.get("pushed_at") or "",
            "fork": bool(repo.get("fork")),
        })
    public.sort(key=lambda item: (item["stars"], item["pushed"]), reverse=True)
    return public


def render_svg(public, observed):
    width, row_height, top = 860, 34, 105
    n_rows = max((len(public) + 1) // 2, 1)
    height = top + n_rows * row_height + 65
    rows = []
    for i, item in enumerate(public):
        column, row = divmod(i, n_rows)
        x, y = 32 + column * 412, top + row * row_height
        name = item["name"][:28] + ("…" if len(item["name"]) > 28 else "")
        meta = item["language"] + (" / fork" if item["fork"] else "")
        rows += [f'<text x="{x}" y="{y}" fill="#eeeae1" font-size="13">{escape(name)}</text>',
                 f'<text x="{x + 380}" y="{y}" text-anchor="end" fill="#adb3a9" font-size="10">{escape(meta)}</text>']
    if not public:
        rows.append('<text x="32" y="105" fill="#adb3a9" font-size="14">No public repositories returned.</text>')
    rendered_rows = "\n".join(rows)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" font-family="ui-monospace, Consolas, monospace">
<title id="title">Public repository catalog</title>
<desc id="desc">Public repositories from Rajveerx11 and associated organizations. Forks are marked. Full names, descriptions, and clickable source links are in docs/public-repositories.md.</desc>
<rect x="1" y="1" width="858" height="{height - 2}" rx="5" fill="#131514" stroke="#363c35"/>
<text x="32" y="37" fill="#eeeae1" font-size="20" font-family="Segoe UI, Arial, sans-serif">Public repository catalog</text>
<text x="32" y="64" fill="#adb3a9" font-size="12">Rajveerx11 / associated organizations</text>
<path d="M1 78H859" stroke="#363c35"/>
{rendered_rows}
<path d="M32 {height - 48}H828" stroke="#363c35"/>
<text x="32" y="{height - 25}" fill="#adb3a9" font-size="11">{len(public)} public repositories · forks marked · snapshot {observed}</text>
<text x="828" y="{height - 25}" text-anchor="end" fill="#ef9773" font-size="11">Full linked index ↗</text>
</svg>
'''


def markdown_cell(value):
    # Preserve source wording while preventing API text from adding rows, links, or raw HTML.
    value = escape(str(value), quote=False).replace("\\", "\\\\")
    for char in ("|", "[", "]", "*", "_", "`", "~"):
        value = value.replace(char, "\\" + char)
    return value.replace("\r", " ").replace("\n", " ")


def render_markdown(public, observed):
    lines = ["# Public repositories", "", f"GitHub API snapshot: {observed} (UTC).", "",
             "Public repositories from Rajveerx11, neuratile, and Government-Polytechnic-Solapur. "
             "Forks are identified; inclusion does not imply sole authorship. Private repositories and "
             "the profile repository are excluded. Descriptions are supplied by the repositories.", "",
             "[Back to the profile](../README.md)", "", "| Repository | Language | Kind | Description |",
             "| --- | --- | --- | --- |"]
    for item in public:
        url = "https://github.com/" + quote(item["full_name"], safe="/")
        kind = "Fork" if item["fork"] else "Non-fork"
        lines.append(f'| [{markdown_cell(item["full_name"])}]({url}) | {markdown_cell(item["language"])} | {kind} | {markdown_cell(item["description"])} |')
    if not public:
        lines += ["", "No public repositories returned."]
    return "\n".join(lines) + "\n"


def main():
    repositories = collect(f"/users/{USER}/repos", "&type=owner&sort=updated")
    for org in ORGS:
        repositories += collect(f"/orgs/{org}/repos", "&type=public&sort=updated")
    public = public_projects(repositories)
    observed = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    Path("assets").mkdir(exist_ok=True)
    Path("docs").mkdir(exist_ok=True)
    Path("assets/project-index.svg").write_text(render_svg(public, observed), encoding="utf-8", newline="\n")
    Path("docs/public-repositories.md").write_text(render_markdown(public, observed), encoding="utf-8", newline="\n")
    print(f"ok: {len(public)} public repositories; forks marked")


if __name__ == "__main__":
    main()
