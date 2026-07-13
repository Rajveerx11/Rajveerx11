"""Generate the three flagship project cards as themed terminal-panel SVGs.

Star counts are pulled live from the GitHub API so they never go stale.
Runs in CI (GITHUB_TOKEN) or locally (gh auth token).
"""
import json, os, subprocess, urllib.request

def token():
    for k in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(k):
            return os.environ[k]
    return subprocess.check_output(["gh", "auth", "token"], text=True).strip()

TOK = token()

def stars(full):
    req = urllib.request.Request(f"https://api.github.com/repos/{full}",
                                 headers={"Authorization": f"bearer {TOK}"})
    return json.load(urllib.request.urlopen(req))["stargazerCount" if False else "stargazers_count"]

LANG = {"TypeScript":"#3178c6","JavaScript":"#f1e05a","React":"#61dafb","Rust":"#dea584",
        "Transformers.js":"#ff6f00","MCP":"#8b949e","React Flow":"#ff0072","Tree-sitter":"#a9b1d6",
        "Tauri":"#24c8db","Ollama":"#c9d1d9"}

# (slug, monogram, accent, repo_url, star_repo, title, desc_lines, tags, note)
CARDS = [
    ("obsidian", "O", "#a371f7", "https://github.com/Rajveerx11/obsidian-graph-intelligence",
     "Rajveerx11/obsidian-graph-intelligence", "Obsidian Graph Intelligence",
     [[("An Obsidian plugin that treats your knowledge vault as a ", 0), ("graph", 1),
       (". Detects orphan notes, discovers", 0)],
      [("topic clusters, and suggests missing links using offline ", 0), ("Transformers.js", 1),
       (" embeddings. Ships with an", 0)],
      [('adaptive learning system, a batch ', 0), ('"Fix My Vault"', 1),
       (" repair engine, and LLM integration via Ollama/OpenAI.", 0)]],
     ["TypeScript", "React", "Transformers.js", "MCP"], None),

    ("repograph", "R", "#36bcf7", "https://github.com/Rajveerx11/repograph-intelligence",
     "Rajveerx11/repograph-intelligence", "RepoGraph Intelligence",
     [[("An AI-native structural intelligence engine that analyzes codebases as ", 0), ("dependency graphs", 1),
       (". Extracts", 0)],
      [("imports, exports and symbols across JS/TS/Python, computes coupling metrics, estimates ", 0),
       ("blast radius", 1)],
      [("for changes, and audits supply-chain deps against OSV.dev. React Flow live explorer + MCP server.", 0)]],
     ["JavaScript", "Rust", "React Flow", "Tree-sitter", "MCP"], "Rust core in active development"),

    ("tessera", "T", "#3fb950", "https://github.com/neuratile/Tessera",
     "neuratile/Tessera", "Tessera",
     [[("A ", 0), ("local-first", 1), (" AI testing IDE that turns any codebase into a full QA dossier without sending source", 0)],
      [("to the cloud. Parses with Tree-sitter, embeds via Ollama, generates test plans, cases and defect", 0)],
      [("reports through versioned prompts with JSON-Schema tool calling, each validated by a ", 0), ("Zod contract", 1), (".", 0)]],
     ["TypeScript", "Rust", "Tauri", "React", "Ollama"], None)
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def chip(x, y, label, color):
    w = round(len(label) * 6.9 + 20)
    svg = (f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="6" fill="{color}" opacity="0.14"/>'
           f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="6" fill="none" stroke="{color}" stroke-width="1" opacity="0.5"/>'
           f'<text x="{x + w/2:.0f}" y="{y+14}" text-anchor="middle" fill="{color}" font-size="10.5" font-weight="600">{esc(label)}</text>')
    return svg, w

def desc_line(x, y, segs):
    out = [f'<text x="{x}" y="{y}" font-size="12.5" fill="#8b949e">']
    for txt, hl in segs:
        if hl:
            out.append(f'<tspan fill="#e6edf3" font-weight="600">{esc(txt)}</tspan>')
        else:
            out.append(esc(txt))
    out.append('</text>')
    return "".join(out)

os.makedirs("assets", exist_ok=True)
import xml.dom.minidom
W = 860
for slug, mono, accent, url, starrepo, title, lines, tags, note in CARDS:
    sc = stars(starrepo)
    body_top = 92
    line_h = 22
    tags_y = body_top + len(lines) * line_h + (18 if note else 6)
    H = tags_y + 40

    parts = []
    # panel + animated border sweep
    parts.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="#0d1117" stroke="#26334a" stroke-width="1.5"/>')
    peri = 2 * (W + H)
    parts.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="none" stroke="{accent}" stroke-width="1.5" '
                 f'stroke-dasharray="80 {peri-80}" stroke-linecap="round" opacity="0.85">'
                 f'<animate attributeName="stroke-dashoffset" values="0;-{peri}" dur="9s" repeatCount="indefinite"/></rect>')
    # monogram tile — everything in the header row is centred on the tile's
    # vertical centre (cy) so the box never looks dropped next to the title
    tile = 44
    ty = 30
    cy = ty + tile / 2                       # 52
    parts.append(f'<rect x="30" y="{ty}" width="{tile}" height="{tile}" rx="11" fill="{accent}" opacity="0.14"/>'
                 f'<rect x="30" y="{ty}" width="{tile}" height="{tile}" rx="11" fill="none" stroke="{accent}" stroke-width="1.5"/>'
                 f'<text x="52" y="{cy}" text-anchor="middle" dominant-baseline="central" fill="{accent}" font-size="23" font-weight="700">{mono}</text>')
    # pulsing status dot + title, baseline-aligned to the tile centre
    parts.append(f'<circle cx="90" cy="{cy}" r="3.5" fill="{accent}"><animate attributeName="opacity" values="1;0.3;1" dur="2.4s" repeatCount="indefinite"/></circle>')
    parts.append(f'<text x="102" y="{cy}" dominant-baseline="central" fill="#e6edf3" font-size="18" font-weight="700">{esc(title)}</text>')
    bx = round(102 + len(title) * 10.4 + 14)
    chip_y = round(cy - 10)                   # 20px-tall chip centred on cy
    # org pill (Tessera only)
    if slug == "tessera":
        s, w = chip(bx, chip_y, "neuratile", "#a371f7"); parts.append(s); bx += w + 6
        s, w = chip(bx, chip_y, "founder", "#a371f7"); parts.append(s); bx += w + 6
    # star chip (skip when zero — a live "0" is negative signal)
    if sc > 0:
        s, w = chip(bx, chip_y, f"★ {sc}", "#e3b341"); parts.append(s)
    # description
    for i, segs in enumerate(lines):
        parts.append(desc_line(34, body_top + i * line_h, segs))
    if note:
        parts.append(f'<text x="34" y="{body_top + len(lines)*line_h + 4}" font-size="11" fill="{accent}" font-style="italic">◆ {esc(note)}</text>')
    # tag chips
    tx = 34
    for t in tags:
        s, w = chip(tx, tags_y, t, LANG.get(t, "#8b949e")); parts.append(s); tx += w + 8
    # click-through arrow
    parts.append(f'<text x="{W-30}" y="{cy}" text-anchor="end" dominant-baseline="central" fill="{accent}" font-size="16" font-weight="700">↗</text>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'font-family="\'JetBrains Mono\', ui-monospace, SFMono-Regular, monospace">\n  '
           + "\n  ".join(parts) + "\n</svg>\n")
    xml.dom.minidom.parseString(svg)
    with open(f"assets/built-{slug}.svg", "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"built-{slug}.svg  stars={sc}  {H}px")
