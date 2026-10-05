"""Render the approved profile design as GitHub-safe, self-contained SVGs.

These are editorial project roles, not runtime telemetry or repository wiring.
Run with --check to verify checked-in assets without modifying them.
"""
from html import escape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
THEMES = {
    "dark": {"bg": "#131514", "surface": "#191c1a", "text": "#eeeae1",
             "muted": "#adb3a9", "line": "#363c35", "accent": "#ef9773", "tint": "#37251e"},
    "light": {"bg": "#f1f2eb", "surface": "#e9ece4", "text": "#20261f",
              "muted": "#515e4e", "line": "#bac4b3", "accent": "#a83e1b", "tint": "#f5e3d9"},
}
ROLES = [
    ("Human input", ("AgentWisper",), "input"),
    ("Context", ("GFI Scout / RepoGraph",), "context"),
    ("Orchestration", ("Neura",), "orchestration"),
    ("Testing", ("Tessera",), "testing"),
    ("Verification", ("Proof-of-Work",), "verification"),
    ("Memory", ("Obsidian Graph", "Intelligence"), "memory"),
]
GLYPHS = {
    "input": '<path d="M10 20v8m6-14v20m8-27v34m8-27v20m6-14v8"/>',
    "context": '<circle cx="21" cy="21" r="13"/><circle cx="21" cy="21" r="6"/><path d="m30 30 11 11M21 5v7M5 21h7M21 30v7M30 21h7"/>',
    "orchestration": '<rect x="4" y="19" width="10" height="10"/><rect x="34" y="5" width="10" height="10"/><rect x="34" y="33" width="10" height="10"/><path d="M14 24h10V10h10M24 24v14h10"/>',
    "testing": '<path d="m24 5 15 7v13c0 8-7 14-15 18C16 39 9 33 9 25V12Z"/><path d="M17 18h14M17 24h14M17 30h8"/>',
    "verification": '<path d="m24 4 17 10v20L24 44 7 34V14Z"/><path d="m14 24 7 7 14-15m-10 15 10-11"/>',
    "memory": '<path d="m24 5 19 10-19 10L5 15Zm-19 19 19 10 19-10M5 33l19 10 19-10"/>',
}


def text(x, y, value, color, size=16, anchor="start", mono=False):
    family = "ui-monospace, Consolas, monospace" if mono else "Segoe UI, Arial, sans-serif"
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'text-anchor="{anchor}" font-family="{family}">{escape(value)}</text>')


def frame(width, height, title, description, body, colors):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            'role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title>\n'
            f'<desc id="desc">{escape(description)}</desc>\n'
            f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="5" '
            f'fill="{colors["bg"]}" stroke="{colors["line"]}"/>\n'
            + "\n".join(body) + "\n</svg>\n")


def header(colors):
    c = colors
    body = [
        text(32, 41, "Rajveer Vadnal / Agentic systems engineer", c["muted"], 17, mono=True),
        text(29, 121, "Systems that can", c["text"], 64),
        text(29, 195, "prove themselves.", c["accent"], 64),
        f'<path d="M32 222H828" stroke="{c["line"]}"/>',
        text(32, 255, "Coding tools · Local-first AI · Verification", c["muted"], 17),
        text(828, 255, "RV", c["accent"], 18, anchor="end", mono=True),
    ]
    return frame(860, 280, "Rajveer Vadnal: systems that can prove themselves",
                 "Agentic systems engineer building coding tools and local-first AI products.", body, c)


def atlas(colors, mobile=False):
    c = colors
    width, height = (430, 790) if mobile else (860, 545)
    positions = [(110, 140), (320, 140), (320, 360), (110, 360), (110, 600), (320, 600)] if mobile else [
        (135, 155), (425, 155), (720, 155), (720, 350), (425, 350), (135, 350)]
    path = "M110 140H320V360H110V600" if mobile else "M135 155H425H720V350H425"
    memory = "M110 600H320M320 600H415V140H320" if mobile else "M425 350H135M135 350H58V98H425V155"
    body = [
        text(25, 36, "Execution atlas", c["text"], 20),
        text(25, 61, "Intent / context / evidence", c["muted"], 12, mono=True),
        f'<path d="M1 77H{width - 1}" stroke="{c["line"]}"/>',
        f'<path d="{path}" fill="none" stroke="{c["line"]}" stroke-width="1.5"/>',
        f'<path d="{memory}" fill="none" stroke="{c["line"]}" stroke-width="1.5" stroke-dasharray="5 7"/>',
    ]
    for index, ((role, projects, glyph), (x, y)) in enumerate(zip(ROLES, positions), 1):
        selected = glyph == "verification"
        color = c["accent"] if selected else c["muted"]
        body += [
            f'<circle cx="{x}" cy="{y}" r="41" fill="{c["tint"] if selected else c["surface"]}" stroke="{color if selected else c["line"]}"/>',
            f'<circle cx="{x}" cy="{y}" r="34" fill="none" stroke="{color if selected else c["line"]}" opacity="0.6"/>',
            f'<g transform="translate({x - 24} {y - 24})" fill="none" stroke="{color}" stroke-width="1.5">{GLYPHS[glyph]}</g>',
            text(x + 38, y - 43, f"{index:02}", color, 12, mono=True),
            text(x, y + 68, role, color if selected else c["text"], 18, anchor="middle"),
        ]
        for row, project in enumerate(projects):
            body.append(text(x, y + 93 + row * 19, project, c["muted"], 13 if mobile else 15, anchor="middle", mono=True))
        if selected:
            body.append(f'<circle cx="{x}" cy="{y}" r="48" fill="none" stroke="{c["accent"]}"/>')
    # A physical break in the path marks human approval; it is not a status signal.
    if mobile:
        body += [f'<rect x="44" y="465" width="133" height="35" rx="3" fill="{c["bg"]}" stroke="{c["line"]}"/>',
                 text(110, 488, "Human approval", c["accent"], 12, anchor="middle", mono=True)]
    else:
        body += [f'<rect x="560" y="334" width="25" height="32" fill="{c["bg"]}"/>',
                 f'<path d="M565 337v26m15-26v26M572 290v34" stroke="{c["muted"]}"/>',
                 text(572, 278, "Human approval", c["muted"], 13, anchor="middle", mono=True)]
    footer = height - 50
    body += [f'<path d="M25 {footer - 15}H{width - 25}" stroke="{c["line"]}"/>',
             text(25, footer + 9, "Roles, not repository integrations.", c["muted"], 14),
             text(25, footer + 31, "Explore the linked projects below.", c["muted"], 12, mono=True)]
    return frame(width, height, "Execution atlas of Rajveer Vadnal's projects",
                 "Human input: AgentWisper. Context: GFI Scout and RepoGraph. Orchestration: Neura. "
                 "Testing: Tessera. Verification: Proof-of-Work. Memory: Obsidian Graph Intelligence. "
                 "Paths describe conceptual roles, not implemented integrations.", body, c)


def recorder(colors, mobile=False):
    c = colors
    width, height = (430, 700) if mobile else (860, 390)
    body = [text(25, 37, "Flight recorder / Tessera", c["text"], 20),
            text(25, 63, "Public commit 48266fa · 18 Jun 2026", c["muted"], 12, mono=True),
            f'<path d="M1 80H{width - 1}" stroke="{c["line"]}"/>']
    steps = [
        ("Build the engine", ("Mutate covered source.", "Rerun the test suite.")),
        ("Catch the gap", ("A Stop request could be lost", "at the baseline handoff.")),
        ("Keep the regression", ("Stopping during the baseline", "prevents mutant runs.")),
        ("Guard the side effect", ("The internal baseline must", "not post a tracker comment.")),
    ]
    if mobile:
        body.append(f'<path d="M40 124V451" stroke="{c["line"]}"/>')
        for i, (heading, lines) in enumerate(steps):
            y = 123 + i * 102
            body += [f'<rect x="30" y="{y - 11}" width="20" height="20" fill="{c["bg"]}" stroke="{c["accent"] if i == 1 else c["line"]}"/>',
                     text(66, y + 5, heading, c["accent"] if i == 1 else c["text"], 19)]
            body += [text(66, y + 33 + j * 20, line, c["muted"], 15) for j, line in enumerate(lines)]
        body += [f'<rect x="25" y="535" width="380" height="96" rx="3" fill="{c["surface"]}" stroke="{c["line"]}"/>',
                 text(45, 563, "One registered cancellation token", c["accent"], 16),
                 text(45, 593, "Baseline run → mutant sweep", c["text"], 16),
                 text(25, 664, "A commit reading, not simulated agent logs.", c["muted"], 12)]
    else:
        for i, (heading, lines) in enumerate(steps):
            x = 30 + i * 210
            body += [text(x, 112, f"{i + 1:02}", c["accent"] if i == 1 else c["muted"], 12, mono=True),
                     text(x, 142, heading, c["accent"] if i == 1 else c["text"], 18)]
            body += [text(x, 172 + j * 20, line, c["muted"], 14) for j, line in enumerate(lines)]
        body += [f'<rect x="25" y="220" width="810" height="100" rx="3" fill="{c["surface"]}" stroke="{c["line"]}"/>',
                 text(45, 249, "One registered cancellation token across both phases", c["accent"], 16),
                 text(45, 287, "Baseline run", c["text"], 22),
                 f'<path d="M260 281H520m-8-6 8 6-8 6" fill="none" stroke="{c["accent"]}"/>',
                 text(550, 287, "Mutant sweep", c["text"], 22),
                 text(25, 354, "A reading of a public commit, not a replay of an agent session.", c["muted"], 14)]
    return frame(width, height, "Tessera mutation-testing change and review corrections",
                 "The public commit records the mutation engine, a shared cancellation token fixing a Stop gap, "
                 "a regression test, and suppression of tracker comments for the internal baseline.", body, c)


def build_assets():
    assets = {}
    for theme, colors in THEMES.items():
        suffix = "" if theme == "dark" else "-light"
        assets[f"profile-header{suffix}.svg"] = header(colors)
        for mobile in (False, True):
            variant = "-mobile" if mobile else ""
            assets[f"execution-atlas{variant}{suffix}.svg"] = atlas(colors, mobile)
            assets[f"flight-recorder{variant}{suffix}.svg"] = recorder(colors, mobile)
    return assets


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for name, svg in build_assets().items():
        path = ROOT / "assets" / name
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != svg:
                stale.append(name)
        else:
            path.parent.mkdir(exist_ok=True)
            path.write_text(svg, encoding="utf-8", newline="\n")
    if stale:
        raise SystemExit("Stale atlas assets: " + ", ".join(stale))
    print("ok: atlas assets " + ("match their generator" if check else "generated"))


if __name__ == "__main__":
    main()
