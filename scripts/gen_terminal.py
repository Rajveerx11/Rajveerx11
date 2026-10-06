"""Terminal profile artwork. Standard library only; no scripts or remote SVG assets."""
import argparse
from datetime import date, timedelta
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

USER = "Rajveerx11"
THEMES = {
    "dark": {"bg": "#101511", "fg": "#dfe7df", "muted": "#a3afa5", "line": "#334238",
             "accent": "#91c89a", "cells": ["#202c23", "#3d6447", "#56805f", "#73a580", "#91c89a"]},
    "light": {"bg": "#f3f6f0", "fg": "#26382b", "muted": "#536457", "line": "#bccbbe",
              "accent": "#28643b", "cells": ["#e0e8dc", "#afccaa", "#8fb58f", "#5b8b64", "#28643b"]},
}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace"
ROOT = Path(__file__).resolve().parent.parent


def text(x, y, value, color, size=16, **attrs):
    options = " ".join(f'{key.replace("_", "-")}="{escape(str(value), quote=True)}"' for key, value in attrs.items())
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" {options}>{escape(str(value))}</text>'


def frame(width, height, title, description, body, theme, style=""):
    p = THEMES[theme]
    body = "\n".join(body)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" font-family="{MONO}">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(description)}</desc>
{style}
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="4" fill="{p['bg']}" stroke="{p['line']}"/>
{body}
</svg>
'''
    ET.fromstring(svg)
    return svg


def hero(theme="dark", mobile=False):
    p = THEMES[theme]
    width, height = (440, 378) if mobile else (860, 298)
    body = [text(24, 31, "~/Rajveerx11", p["muted"], 14),
            f'<path d="M1 46H{width - 1}" stroke="{p["line"]}"/>',
            text(24, 82, "rajveer@github:~$ whoami", p["accent"], 17)]
    # Original ASCII initials, not an invented portrait or copied photograph.
    initials = ["RRRR   VV      VV", "RR RR   VV    VV ", "RRRR     VV  VV  ",
                "RR RR     VVVV   ", "RR  RR     VV    "]
    for i, line in enumerate(initials):
        body.append(text(24, 126 + i * 22, line, p["accent"], 18, **{"xml:space": "preserve"}))
    x, y = (24, 270) if mobile else (370, 132)
    body += [text(x, y, "Rajveer Vadnal", p["fg"], 24, font_weight="600"),
             text(x, y + 28, "Agentic systems engineer", p["muted"], 16)]
    if not mobile:
        body += [text(x, y + 61, "Coding tools. Local-first AI.", p["fg"], 16),
                 text(x, y + 86, "Checks you can rerun.", p["fg"], 16)]
    body += [f'<path d="M24 {height - 50}H{width - 24}" stroke="{p["line"]}"/>',
             text(24, height - 23, "Python / TypeScript / Rust", p["muted"], 15)]
    return frame(width, height, "Rajveer Vadnal: terminal profile",
                 "Agentic systems engineer. Coding tools, local-first AI, and verification. Python, TypeScript, Rust. ASCII initials: RV.",
                 body, theme)


def calendar_days(calendar):
    """Validate API dates/counts before they influence labels, geometry, or totals."""
    days = []
    for week in calendar["weeks"]:
        for item in week["contributionDays"]:
            day = date.fromisoformat(item["date"])
            count = item["contributionCount"]
            if type(count) is not int or count < 0:
                raise ValueError("Contribution counts must be nonnegative integers")
            record = {"date": day.isoformat(), "count": count}
            if "contributionLevel" in item:
                levels = ("NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE")
                if item["contributionLevel"] not in levels:
                    raise ValueError("Unknown GitHub contribution level")
                record["level"] = levels.index(item["contributionLevel"])
                if (record["level"] == 0) != (count == 0):
                    raise ValueError("Contribution level disagrees with count")
            days.append(record)
    days.sort(key=lambda item: item["date"])
    if not days:
        raise ValueError("Empty contribution calendar")
    for previous, current in zip(days, days[1:]):
        if date.fromisoformat(current["date"]) - date.fromisoformat(previous["date"]) != timedelta(days=1):
            raise ValueError("Calendar dates must be unique and consecutive")
    total = calendar["totalContributions"]
    if type(total) is not int or total != sum(item["count"] for item in days):
        raise ValueError("Contribution calendar total does not match its days")
    return days


def streaks(days, today):
    """Longest is window-scoped. Only an unfinished *today* gets a grace day."""
    today = date.fromisoformat(today)
    observed = [item for item in days if date.fromisoformat(item["date"]) <= today]
    if not observed:
        return 0, 0
    run = longest = 0
    for item in observed:
        run = run + 1 if item["count"] else 0
        longest = max(longest, run)
    end = len(observed) - 1
    if date.fromisoformat(observed[end]["date"]) == today and observed[end]["count"] == 0:
        end -= 1
    # A stale calendar must not report a historical streak as current.
    if end < 0 or today - date.fromisoformat(observed[end]["date"]) > timedelta(days=1):
        return 0, longest
    current = 0
    while end >= 0 and observed[end]["count"]:
        current += 1
        end -= 1
    return current, longest


def heatmap(days, observed, theme="dark", mobile=False):
    p = THEMES[theme]
    first, last = date.fromisoformat(days[0]["date"]), date.fromisoformat(days[-1]["date"])
    # GitHub calendars begin on Sunday; partial opening weeks need empty slots.
    offset = (first.weekday() + 1) % 7
    weeks = (offset + len(days) + 6) // 7
    panels = [range(0, weeks)] if not mobile else [range(0, min(27, weeks)), range(27, weeks)]
    panels = [panel for panel in panels if panel]
    width = 440 if mobile else 860
    height = 122 + len(panels) * 170 if mobile else 272
    step, cell, left = (13, 10, 57) if mobile else (14, 11, 61)
    body = [text(24, 33, "contributions / GitHub calendar", p["fg"], 16),
            text(24, 61, f"{sum(d['count'] for d in days):,} contributions", p["accent"], 17)]
    if not mobile:
        body.append(text(width - 24, 61, f"{first} .. {last}", p["muted"], 13, text_anchor="end"))
    maximum = max(item["count"] for item in days) or 1
    for panel_index, panel in enumerate(panels):
        top = 99 + panel_index * 170
        previous_month = None
        last_label_x = -100
        for week in panel:
            week_date = first - timedelta(days=offset) + timedelta(days=week * 7)
            month = week_date.strftime("%b")
            x = left + (week - panel.start) * step
            if month != previous_month and x - last_label_x >= 39:
                body.append(text(x, top - 12, month, p["muted"], 13))
                last_label_x = x
            previous_month = month
        for label, row in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
            body.append(text(24, top + row * step + 9, label, p["muted"], 12))
        for i, item in enumerate(days):
            week, row = divmod(offset + i, 7)
            if week not in panel:
                continue
            level = 0 if not item["count"] else min(4, max(1, (item["count"] * 4 + maximum - 1) // maximum))
            x, y = left + (week - panel.start) * step, top + row * step
            delay = round(week / max(weeks - 1, 1) * 1.2, 3)
            body.append(f'<rect class="cell" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="1" fill="{p["cells"][level]}" style="animation-delay:{delay}s"><title>{item["date"]}: {item["count"]} contributions</title></rect>')
        if mobile:
            start = max(first, first - timedelta(days=offset) + timedelta(days=panel.start * 7))
            end = min(last, first - timedelta(days=offset) + timedelta(days=panel.stop * 7 - 1))
            body.append(text(24, top + 119, f"{start} .. {end}", p["muted"], 14))
    footer = height - 45
    body += [f'<path d="M24 {footer - 16}H{width - 24}" stroke="{p["line"]}"/>',
             text(24, footer + 6, f"snapshot {observed} UTC", p["muted"], 13),
             text(24, height - 15, "Daily refresh / not a productivity score", p["muted"], 13)]
    if not mobile:
        body.append(text(643, footer + 6, "less", p["muted"], 12))
        for i, color in enumerate(p["cells"]):
            body.append(f'<rect x="{681 + i * 17}" y="{footer - 4}" width="12" height="12" rx="1" fill="{color}"/>')
        body.append(text(779, footer + 6, "more", p["muted"], 12))
    # Baseline is visible when animation is unsupported, disabled, or completed.
    style = '''<style>
@keyframes reveal { from { opacity: .35; } to { opacity: 1; } }
.cell { animation: reveal .35s ease-out both; }
@media (prefers-reduced-motion: reduce) { .cell { animation: none; } }
</style>'''
    return frame(width, height, "GitHub contribution calendar",
                 f"{sum(d['count'] for d in days):,} contributions from {first} through {last}. Snapshot {observed} UTC. Counts follow GitHub contribution rules, not commits alone. Color intensity is relative to the busiest day in this window.",
                 body, theme, style)


def activity_metrics(snapshot):
    current, longest = streaks(snapshot["days"], snapshot["observed"])
    return [("current streak", f"{current:,} days"), ("longest in window", f"{longest:,} days"),
            ("public merged PRs", f"{snapshot['merged']:,}"), ("public non-forks", f"{snapshot['repos']:,}"),
            ("stars / non-forks", f"{snapshot['stars']:,}"), ("followers", f"{snapshot['followers']:,}")]


def activity_markdown(snapshot):
    days = snapshot["days"]
    lines = ["# GitHub activity snapshot", "", f"Snapshot: {snapshot['observed']} UTC. Daily refresh, not live telemetry.", "",
             f"Calendar: {days[0]['date']} through {days[-1]['date']} (inclusive).",
             f"Total contributions in this window: **{sum(day['count'] for day in days):,}**.", "",
             "| Metric | Recorded value |", "| --- | ---: |"]
    lines += [f"| {label} | {value} |" for label, value in activity_metrics(snapshot)]
    lines += ["", "Longest streak is window-scoped. Merged PRs are public, all time. Repositories and stars cover owned public non-forks. "
              "Calendar counts follow GitHub contribution rules and can include anonymized private activity counts, never private repository metadata.", "",
              "[Counting rules](profile-evidence.md#public-catalog-and-activity) / [Back to profile](../README.md)", "",
              "<details>", "<summary>Daily calendar counts (text equivalent of every heatmap cell)</summary>", "",
              "| Date | Contributions |", "| --- | ---: |"]
    lines += [f"| {day['date']} | {day['count']} |" for day in days]
    lines += ["", "</details>", ""]
    return "\n".join(lines)


def stats(snapshot, theme="dark", mobile=False):
    p = THEMES[theme]
    width, height = (440, 430) if mobile else (860, 290)
    days = snapshot["days"]
    current, longest = streaks(days, snapshot["observed"])
    metrics = activity_metrics(snapshot)
    body = [text(24, 34, "activity / dated snapshot", p["fg"], 16)]
    for i, (label, value) in enumerate(metrics):
        if mobile:
            x, y = 24, 76 + i * 40
            body += [text(x, y, label, p["muted"], 15),
                     text(width - 24, y, value, p["accent"], 19, text_anchor="end")]
        else:
            row, column = divmod(i, 3)
            x, y = 24 + column * 280, 83 + row * 69
            body += [text(x, y, value, p["accent"], 26), text(x, y + 24, label, p["muted"], 14)]
    y = height - 96
    body += [f'<path d="M24 {y}H{width - 24}" stroke="{p["line"]}"/>',
             text(24, y + 26, f"calendar: {days[0]['date']} .. {days[-1]['date']}", p["muted"], 13),
             text(24, y + 51, "PRs: public, all time / repos: owner only", p["muted"], 13),
             text(24, y + 76, f"snapshot {snapshot['observed']} UTC / GitHub API", p["muted"], 13)]
    return frame(width, height, "GitHub activity snapshot",
                 f"Current streak {current} days; longest streak {longest} days within the displayed calendar window. {snapshot['merged']} public merged PRs, all time; {snapshot['repos']} owned public non-fork repositories; {snapshot['stars']} stars across those repositories; {snapshot['followers']} followers. Snapshot {snapshot['observed']} UTC.",
                 body, theme)


def variants(name, render):
    for mobile in (False, True):
        for theme in THEMES:
            suffix = ("-mobile" if mobile else "") + ("-light" if theme == "light" else "")
            yield f"{name}{suffix}.svg", render(theme, mobile)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check committed identity assets without rewriting them")
    args = parser.parse_args()
    for filename, svg in variants("terminal-profile", hero):
        path = ROOT / "assets" / filename
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != svg:
                raise SystemExit(f"Stale terminal asset: {path}")
        else:
            path.write_text(svg, encoding="utf-8", newline="\n")
    print("ok: terminal identity assets")


if __name__ == "__main__":
    main()
