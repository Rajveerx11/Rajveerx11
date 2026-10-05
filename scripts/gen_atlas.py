"""Render the approved profile design as GitHub-safe, self-contained SVGs.

These are editorial project roles, not runtime telemetry or repository wiring.
Run with --check to verify checked-in assets without modifying them.
"""
from html import escape
from pathlib import Path
import sys
from textwrap import wrap

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


def header(colors, mobile=False):
    c = colors
    if mobile:
        body = [
            text(25, 37, "Rajveer Vadnal", c["text"], 21),
            text(25, 65, "Agentic systems engineer", c["muted"], 14, mono=True),
            text(23, 130, "Systems that", c["text"], 46),
            text(23, 194, "can prove", c["text"], 46),
            text(23, 258, "themselves.", c["accent"], 46),
            f'<path d="M25 287H405" stroke="{c["line"]}"/>',
            text(25, 320, "Coding tools / Local-first AI", c["muted"], 16),
            text(25, 346, "Verification", c["accent"], 16),
        ]
        return frame(430, 370, "Rajveer Vadnal: systems that can prove themselves",
                     "Agentic systems engineer building coding tools and local-first AI products.", body, c)
    body = [
        text(32, 41, "Rajveer Vadnal / Agentic systems engineer", c["muted"], 17, mono=True),
        text(29, 121, "Systems that can", c["text"], 64),
        text(29, 210, "prove themselves.", c["accent"], 64),
        f'<path d="M32 240H828" stroke="{c["line"]}"/>',
        text(32, 277, "Coding tools · Local-first AI · Verification", c["muted"], 17),
        text(828, 277, "RV", c["accent"], 18, anchor="end", mono=True),
    ]
    return frame(860, 302, "Rajveer Vadnal: systems that can prove themselves",
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


def paragraph(x, y, value, colors, columns=48, size=16, leading=24):
    return [text(x, y + i * leading, line, colors["muted"], size)
            for i, line in enumerate(wrap(value, columns))]


def panel_heading(width, title, label, colors):
    return [text(25, 37, title, colors["text"], 23),
            text(25, 64, label, colors["muted"], 12, mono=True),
            f'<path d="M1 82H{width - 1}" stroke="{colors["line"]}"/>']


def overview(colors, mobile=False):
    c = colors
    width, height = (430, 470) if mobile else (860, 280)
    body = panel_heading(width, "The builder behind the map", "CONTEXT / EXECUTION / VERIFICATION", c)
    body += paragraph(25, 119,
                      "I build coding tools and local-first AI products. My work focuses on context, controlled execution, and verification.",
                      c, columns=42 if mobile else 93)
    y = 220 if mobile else 183
    body += [f'<path d="M25 {y - 18}H{width - 25}" stroke="{c["line"]}"/>',
             text(25, y + 8, "Founder / neuratile + Visage AI", c["accent"], 17)]
    body += paragraph(25, y + 36, "Developer tools including Tessera; aesthetic outcome previews at Visage AI.",
                      c, columns=42 if mobile else 93, size=15, leading=22)
    if mobile:
        body += [text(25, 338, "Python / TypeScript / Rust", c["text"], 17),
                 text(25, 379, "EDUCATION", c["accent"], 12, mono=True),
                 text(25, 406, "Diploma / Computer Science Engineering", c["muted"], 15),
                 text(25, 432, "B.Tech / AI & Machine Learning", c["muted"], 15)]
    else:
        body += [text(25, 254, "Python / TypeScript / Rust", c["text"], 15),
                 text(345, 254, "Diploma: CSE · B.Tech: AI & ML", c["muted"], 15)]
    return frame(width, height, "About Rajveer Vadnal", "Founder at neuratile and Visage AI. "
                 "Python, TypeScript and Rust. Diploma in Computer Science Engineering; B.Tech in AI and Machine Learning.", body, c)


FLAGSHIPS = [
    ("01", "Proof-of-Work", "verification",
     "Rerun checks. Detect deleted or weakened tests. Record hash-chained, Ed25519-signed verdicts.",
     ("Python / FastMCP / SQLite", "Ed25519 / GitHub Actions")),
    ("02", "GFI Scout", "context",
     "Find contribution opportunities using repository health, maintainer responsiveness, freshness, and setup friction.",
     ("Python / FastMCP / asyncio", "Rich / Textual / GitHub API")),
    ("03", "Tessera", "testing",
     "Local-first testing IDE at neuratile. Code context, structured QA artifacts, and optional isolated Docker test execution.",
     ("Rust / Tauri / React / Tree-sitter", "Ollama / Docker")),
    ("04", "Obsidian Graph Intelligence", "memory",
     "Analyze and repair local knowledge graphs. Offline embeddings; queries opt in. External providers have separate data boundaries.",
     ("TypeScript / Obsidian API", "Transformers.js")),
]


def flagships(colors, mobile=False):
    c = colors
    width, height = (430, 1095) if mobile else (860, 615)
    body = panel_heading(width, "Selected systems", "FOUR PROJECTS / INSPECTABLE SOURCE", c)
    for i, (number, name, glyph, description, stack) in enumerate(FLAGSHIPS):
        x, y = (25, 103 + i * 242) if mobile else (25 + (i % 2) * 417, 103 + (i // 2) * 244)
        w = 380 if mobile else 393
        body += [f'<rect x="{x}" y="{y}" width="{w}" height="226" rx="3" fill="{c["surface"]}" stroke="{c["line"]}"/>',
                 text(x + 18, y + 31, number, c["accent"], 13, mono=True),
                 f'<g transform="translate({x + w - 42} {y + 13}) scale(.55)" fill="none" stroke="{c["accent"]}" stroke-width="2">{GLYPHS[glyph]}</g>',
                 text(x + 18, y + 63, name, c["text"], 20)]
        body += paragraph(x + 18, y + 94, description, c, columns=40 if mobile else 43, size=16, leading=23)
        body += [f'<path d="M{x + 18} {y + 169}H{x + w - 18}" stroke="{c["line"]}"/>']
        body += [text(x + 18, y + 192 + j * 19, line, c["muted"], 13, mono=True)
                 for j, line in enumerate(stack)]
    body.append(text(25, height - 19, "Source links and contribution evidence below.", c["muted"], 13))
    return frame(width, height, "Selected engineering projects", "Proof-of-Work, GFI Scout, Tessera "
                 "and Obsidian Graph Intelligence. Descriptions and technology stacks; linked evidence is in the README.", body, c)


EVALUATION = [
    ("Codex CLI 0.146.0", "gpt-5.6-sol", 20, 0),
    ("Copilot CLI 1.0.79", "auto router", 20, 0),
    ("OpenCode CLI 1.4.0", "Nemotron 3 Nano", 17, 3),
]


def evaluation(colors, mobile=False):
    c = colors
    width, height = (430, 875) if mobile else (860, 590)
    body = panel_heading(width, "An evaluation you can inspect", "PROOF-OF-WORK / AUGUST 2026 COHORT", c)
    body += [text(25, 142, "60", c["accent"], 48),
             text(101, 123, "recorded runs", c["text"], 18),
             text(101, 149, "20 tasks / 3 configurations", c["muted"], 15)]
    body += paragraph(25, 188, "One attempt per task and configuration. All outcomes retained.",
                      c, columns=42 if mobile else 93, size=15, leading=22)
    for i, (name, model, passed, failed) in enumerate(EVALUATION):
        y = (258 + i * 125) if mobile else (241 + i * 66)
        body += [text(25, y, name, c["text"], 16),
                 text(25, y + 22, model, c["muted"], 13, mono=True)]
        bx, by, bw = (25, y + 38, 270) if mobile else (335, y - 9, 340)
        body += [f'<rect x="{bx}" y="{by}" width="{bw}" height="12" rx="2" fill="{c["line"]}"/>',
                 f'<rect x="{bx}" y="{by}" width="{bw * passed / 20}" height="12" rx="2" fill="{c["accent"]}"/>',
                 text(315 if mobile else 698, by + 12, f"{passed} / 20 passed", c["text"], 14),
                 text(315 if mobile else 698, by + 34, f"{failed} failed", c["muted"], 13)]
    y = 636 if mobile else 430
    body += [f'<path d="M25 {y - 19}H{width - 25}" stroke="{c["line"]}"/>',
             text(25, y + 4, "RECORDED RESULTS, NOT AN AGENT RANKING", c["accent"], 12, mono=True)]
    caveats = [
        "Pass = successful exit + protected outcome verifier + deterministic anti-tampering gate.",
        "Three failures: outcome verification, not tampering. Codex rows imported unchanged from eight days earlier.",
        "Token usage and exact cost are unknown. Read the linked methodology and limitations.",
    ]
    cy = y + 34
    for caveat in caveats:
        lines = paragraph(25, cy, caveat, c, columns=44 if mobile else 100, size=14, leading=21)
        body += lines
        cy += len(lines) * 21 + 9
    return frame(width, height, "Published Proof-of-Work evaluation, with limitations",
                 "60 runs on 20 tasks, one attempt per configuration. Codex and Copilot: 20 passed, 0 failed each. "
                 "OpenCode: 17 passed, 3 failed. August 2026 recorded cohort, not a general agent ranking. "
                 "Codex rows imported from eight days earlier. Token usage and exact cost unknown.", body, c)


PRINCIPLES = [
    ("01", "Evidence before claims", "Tests and inspectable outputs beat a claim that the task is complete."),
    ("02", "Local-first when privacy matters", "Keep sensitive context on-device by default. Make external boundaries explicit."),
    ("03", "Agents as systems", "Build state and recovery around the model. Keep human approval points explicit."),
]
TOOLS = [
    ("AGENT SYSTEMS", "MCP / FastMCP / RAG", "Zod / JSON Schema / eval gates"),
    ("LANGUAGES", "Python / TypeScript / JavaScript", "Rust / Kotlin"),
    ("LOCAL AI + CODE", "Ollama / Transformers.js", "Tree-sitter / PyTorch / graphs"),
    ("SYSTEMS + DELIVERY", "Tauri / SQLite / Docker / Node.js", "React / Next.js / Flask / CI", "Mutation tests / Ed25519 / PyPI"),
]


def working_set(colors, mobile=False):
    c = colors
    width, height = (430, 1090) if mobile else (860, 660)
    body = panel_heading(width, "Working principles + toolkit", "HOW I BUILD / WHAT I REACH FOR", c)
    for i, (number, name, description) in enumerate(PRINCIPLES):
        y = 118 + i * (130 if mobile else 93)
        body += [text(25, y, number, c["accent"], 13, mono=True),
                 text(60, y, name, c["text"], 19)]
        body += paragraph(60, y + 29, description, c, columns=38 if mobile else 86, size=16, leading=23)
    y = 510 if mobile else 397
    body.append(f'<path d="M25 {y - 28}H{width - 25}" stroke="{c["line"]}"/>')
    for i, (label, *lines) in enumerate(TOOLS):
        x, ty = (25, y + i * 138) if mobile else (25 + (i % 2) * 417, y + (i // 2) * 119)
        body.append(text(x, ty, label, c["accent"], 12, mono=True))
        body += [text(x, ty + 29 + j * 24, line, c["muted"], 16) for j, line in enumerate(lines)]
    return frame(width, height, "Working principles and technical working set",
                 "Evidence before claims. Local-first when privacy matters. Agents as systems with human approval. "
                 "Tools span agent systems, languages, local AI, desktop systems, delivery and verification.", body, c)


def contact(colors, mobile=False):
    c = colors
    width, height = (430, 215) if mobile else (860, 155)
    body = [text(25, 43, "Build something inspectable.", c["text"], 26),
            text(25, 78, "Developer tools / Agentic systems", c["muted"], 17)]
    body += paragraph(25, 116, "Contact and collaboration: email, LinkedIn, or portfolio. Open a link below to get in touch.",
                      c, columns=43 if mobile else 97, size=15, leading=23)
    return frame(width, height, "Contact and collaboration", "Building tools for developers or agentic systems? "
                 "Email Rajveer, connect on LinkedIn or explore the portfolio using the links below.", body, c)


PANELS = {
    "profile-header": header,
    "profile-overview": overview,
    "execution-atlas": atlas,
    "selected-systems": flagships,
    "flight-recorder": recorder,
    "evaluation": evaluation,
    "working-set": working_set,
    "contact": contact,
}


def build_assets():
    assets = {}
    for theme, colors in THEMES.items():
        suffix = "" if theme == "dark" else "-light"
        for mobile in (False, True):
            variant = "-mobile" if mobile else ""
            for name, render in PANELS.items():
                assets[f"{name}{variant}{suffix}.svg"] = render(colors, mobile)
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
