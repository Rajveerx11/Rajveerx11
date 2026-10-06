"""Reference-style profile art, independently implemented for Rajveer's own data.

CI uses only the standard library and the committed ASCII rows. Pillow is needed
only for the optional one-time conversion of a locally prepared portrait.
"""
import argparse
from collections import defaultdict
from datetime import date, timedelta
from html import escape
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

from gen_terminal import MONO, ROOT, streaks, text

WIDTH, HEIGHT = 840, 880
BG, TILE, BORDER = "#0d1117", "#161b22", "#30363d"
INK, MUTED, GREEN = "#e6edf3", "#9ba5b0", "#39d353"
PORTRAIT_DATA = ROOT / "data" / "portrait.json"


def svg(width, height, title, description, body, style=""):
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc" font-family="{MONO}">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(description)}</desc>
{style}
{chr(10).join(body)}
</svg>
'''
    ET.fromstring(content)
    return content


def static_svg(source):
    """Frozen equivalent for an explicit reduced-motion <picture> source.

    Browser emulation of media queries is not consistently inherited by SVG
    image documents. Selecting a truly static file at the HTML layer is reliable.
    """
    start = source.index("<style>")
    end = source.index("</style>", start) + len("</style>")
    result = source[:start] + source[end:]
    result = re.sub(r"<set\b[^>]*/>", "", result)
    ET.fromstring(result)
    return result


def window(command):
    return ['<defs><linearGradient id="surface" x2="0" y2="1"><stop stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
            f'<rect width="{WIDTH}" height="{HEIGHT}" rx="12" fill="url(#surface)"/>',
            f'<rect x=".5" y=".5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="none" stroke="{BORDER}"/>',
            f'<path d="M0 30H{WIDTH}" stroke="{BORDER}"/>',
            *[f'<circle cx="{20 + i * 16}" cy="15" r="5" fill="{color}"/>' for i, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f"))],
            text(420, 20, f"rajveer@github: ~$ {command}", MUTED, 12, text_anchor="middle")]


def validate_rows(data):
    rows = data["rows"]
    columns = data["columns"]
    if type(columns) is not int or not 40 <= columns <= 220:
        raise ValueError("Portrait columns must be an integer between 40 and 220")
    if not isinstance(rows, list) or not 20 <= len(rows) <= 140:
        raise ValueError("Portrait needs between 20 and 140 rows")
    if any(not isinstance(row, str) or len(row) != columns or any(not 32 <= ord(char) <= 126 for char in row) for row in rows):
        raise ValueError("Portrait rows must have equal widths and contain printable ASCII only")
    return rows


def portrait(data):
    rows = validate_rows(data)
    body = window("./portrait.sh")
    columns = data["columns"]
    cell_w, cell_h = 800 / columns, 800 / len(rows)
    duration = 5.8 / len(rows)
    for index, row in enumerate(rows):
        top = 38 + index * cell_h
        body.append(text(20, top + cell_h * .76, row, "#c9d1d9", round(cell_h * .86, 3),
                         **{"xml:space": "preserve", "textLength": 800, "lengthAdjust": "spacingAndGlyphs",
                            "class": "ascii-row", "style": f"animation-delay:{index * duration:.4f}s;animation-duration:{duration:.4f}s"}))
        body.append(f'<rect class="scan-cursor" opacity="0" x="20" y="{top:.3f}" width="{cell_w:.3f}" height="{cell_h:.3f}" fill="#c9d1d9" style="animation-delay:{index * duration:.4f}s;animation-duration:{duration:.4f}s"/>')
    body += [f'<path d="M0 843H{WIDTH}" stroke="{BORDER}"/>',
             text(20, 868, "rajveer@github:~$ whoami", MUTED, 17),
             text(265, 868, "Rajveer Vadnal", INK, 17),
             '<rect class="prompt-cursor" x="414" y="853" width="9" height="18" fill="#c9d1d9"/>']
    style = '''<style>
.ascii-row { clip-path: inset(0); animation: type-row linear both; }
@keyframes type-row { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0); } }
.scan-cursor { opacity: 0; animation: scan linear forwards; }
@keyframes scan { 0% { opacity: .85; transform: translateX(0); } 99% { opacity: .85; } 100% { opacity: 0; transform: translateX(800px); } }
.prompt-cursor { animation: blink 1.2s step-end infinite; }
@keyframes blink { 50% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) {
  .ascii-row, .prompt-cursor { animation: none; }
  .scan-cursor { display: none; }
}
</style>'''
    return svg(WIDTH, HEIGHT, "Rajveer Vadnal: animated ASCII portrait",
               "Close-cropped ASCII portrait derived locally from Rajveer's supplied photograph. Rows type left-to-right, top-to-bottom once in 5.8 seconds, then remain visible. Reduced motion shows the complete portrait immediately.", body, style)


def graph(snapshot, light=False):
    days = snapshot["days"]
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7
    weeks = (len(days) + offset + 6) // 7
    width, height = 40 + weeks * 16, 160
    body = []
    previous_month = None
    for week in range(weeks):
        month = (first + timedelta(days=week * 7 - offset)).strftime("%b")
        if month != previous_month:
            body.append(text(34 + week * 16, 16, month, "#7d8590", 13, font_weight="600"))
            previous_month = month
    for label, row in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
        body.append(text(2, 35 + row * 16, label, "#7d8590", 13, font_weight="600"))
    colors = ("#161b22", "#0e4429", "#006d32", "#26a641", "#39d353")
    maximum = max(day["count"] for day in days) or 1
    for index, day in enumerate(days):
        week, row = divmod(index + offset, 7)
        level = day.get("level", 0 if not day["count"] else min(4, max(1, (day["count"] * 4 + maximum - 1) // maximum)))
        delay = round((week + row * .55) / max(weeks + 3, 1) * 3.6, 3)
        body.append(f'<rect class="cell" x="{34 + week * 16}" y="{24 + row * 16}" width="13" height="13" rx="2.5" fill="{colors[level]}" style="animation-delay:{delay}s"><title>{day["date"]}: {day["count"]} contributions</title></rect>')
    body += [text(34, 154, f"{sum(day['count'] for day in days):,} contributions in the last year", "#24292f" if light else INK, 15, font_weight="700", **{"class": "total"}),
             text(width - 10, 154, f"snapshot {snapshot['observed']} UTC", "#7d8590", 11, text_anchor="end")]
    style = '''<style>
.cell { transform-box: fill-box; transform-origin: center; animation: pop .55s ease-out both; }
@keyframes pop { 0% { opacity: .15; transform: scale(.2); } 60% { opacity: 1; transform: scale(1.1); } 100% { opacity: 1; transform: scale(1); } }
@media (prefers-reduced-motion: reduce) { .cell { animation: none; } }
</style>'''
    return svg(width, height, "Rajveer's GitHub contribution graph",
               f"{sum(day['count'] for day in days):,} contributions from {days[0]['date']} through {days[-1]['date']}. Snapshot {snapshot['observed']} UTC. Live colors use GitHub contribution levels; every daily count is available in the linked text snapshot.", body, style)


def metrics(snapshot):
    days = snapshot["days"]
    current, longest = streaks(days, snapshot["observed"])
    total = sum(day["count"] for day in days)
    active = sum(day["count"] > 0 for day in days)
    best = max(days, key=lambda day: day["count"])
    average = total / active if active else 0
    return [("current streak", current, " days", "today / yesterday; UTC", GREEN),
            ("longest streak", longest, " days", "within displayed window", INK),
            ("contributions", total, "", "in the last year", INK),
            ("active days", active, f" / {len(days)}", f"{active / len(days):.0%} of displayed days", INK),
            ("best day", best["count"], "", best["date"], INK),
            ("avg / active day", average, "", "contributions", INK)]


def number(value, template):
    return f"{value:,.1f}" if isinstance(template, float) else f"{round(value):,}"


def monthly(days):
    totals = defaultdict(int)
    for day in days:
        totals[day["date"][:7]] += day["count"]
    return sorted(totals.items())


def card(snapshot):
    body = window("./stats.sh")
    for index, (label, value, suffix, caption, color) in enumerate(metrics(snapshot)):
        row, column = divmod(index, 2)
        x, y = 20 + column * 408, 54 + row * 166
        delay = index * .15
        body += [f'<g class="tile" style="animation-delay:{delay:.3f}s">',
                 f'<rect x="{x}" y="{y}" width="392" height="150" rx="10" fill="{TILE}" stroke="{BORDER}"/>',
                 text(x + 24, y + 40, f"$ {label}", MUTED, 22)]
        for step in range(1, 13):
            final = step == 12
            value_at_step = value if final else value * (1 - (1 - step / 12) ** 3)
            start = delay + .27 + (step - 1) * .1
            label_svg = text(x + 24, y + 100, number(value_at_step, value), color, 54, font_weight="700",
                             **{"class": "counter-final" if final else "counter-step", "opacity": 1 if final else 0})
            # SMIL opacity switches work reliably in GitHub's SVG image documents.
            # Final value is the baseline when animation support is absent.
            switches = (f'<set attributeName="opacity" to="0" begin="0s"/>'
                        f'<set attributeName="opacity" to="1" begin="{start:.3f}s"/>' if final else
                        f'<set attributeName="opacity" to="1" begin="{start:.3f}s"/>'
                        f'<set attributeName="opacity" to="0" begin="{start + .1:.3f}s"/>')
            body.append(label_svg.replace("</text>", f'<tspan font-size="24" font-weight="400" fill="{MUTED}">{escape(suffix)}</tspan>{switches}</text>'))
        body += [text(x + 24, y + 132, caption, MUTED, 20), "</g>"]
    body += [f'<rect x="20" y="552" width="800" height="308" rx="10" fill="{TILE}" stroke="{BORDER}"/>',
             text(44, 594, "$ contributions / month", MUTED, 22)]
    months = monthly(snapshot["days"])
    peak = max(total for _, total in months) or 1
    slot = 752 / len(months)
    for index, (month, total) in enumerate(months):
        bar_height = 176 * total / peak
        x, y = 44 + index * slot + slot * .19, 810 - bar_height
        delay = 1.3 + index * .06
        body.append(f'<rect class="bar" x="{x:.3f}" y="{y:.3f}" width="{slot * .62:.3f}" height="{bar_height:.3f}" rx="3" fill="{GREEN if total == peak else "#26a641"}" style="animation-delay:{delay:.3f}s"><title>{month}: {total} contributions</title></rect>')
        center = x + slot * .31
        body.append(text(round(center, 3), 839, date.fromisoformat(month + "-01").strftime("%b"), MUTED, 18, text_anchor="middle"))
        if total == peak:
            body.append(text(round(center, 3), round(y - 10, 3), f"{total:,}", INK, 18, text_anchor="middle"))
    body.append(text(420, 875, f"window {snapshot['days'][0]['date']} .. {snapshot['days'][-1]['date']} / snapshot {snapshot['observed']} UTC", MUTED, 12, text_anchor="middle"))
    style = '''<style>
.tile { animation: slide .45s ease-out both; }
@keyframes slide { from { opacity: .15; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
.bar { transform-box: fill-box; transform-origin: bottom; animation: grow .6s ease-out both; }
@keyframes grow { from { transform: scaleY(0); } to { transform: scaleY(1); } }
@media (prefers-reduced-motion: reduce) {
  .tile, .bar { animation: none; }
  .counter-final { opacity: 1 !important; }
  .counter-step { display: none; }
}
</style>'''
    description = "; ".join(f"{label}: {number(value, value)}{suffix}" for label, value, suffix, _, _ in metrics(snapshot))
    return svg(WIDTH, HEIGHT, "Rajveer's contribution and streak statistics", description + f". Longest streak is window-scoped, not all time. Snapshot {snapshot['observed']} UTC. See linked text for daily and monthly counts.", body, style)


def activity_markdown(snapshot):
    days = snapshot["days"]
    lines = ["# GitHub activity snapshot", "", f"Snapshot: {snapshot['observed']} UTC. Daily refresh, not live telemetry.", "",
             f"Calendar: {days[0]['date']} through {days[-1]['date']} (inclusive).",
             f"Total contributions in this window: **{sum(day['count'] for day in days):,}**.", "",
             "| Metric | Recorded value | Detail |", "| --- | ---: | --- |"]
    lines += [f"| {label} | {number(value, value)}{suffix} | {caption} |" for label, value, suffix, caption, _ in metrics(snapshot)]
    lines += ["", "Longest streak is window-scoped. Best-day ties use the earliest day. Average divides contributions by active days, not all calendar days. "
              "Calendar counts follow GitHub contribution rules and may include anonymized private counts; no private repository metadata is published.", "",
              "[Counting rules](profile-evidence.md#public-catalog-and-activity) / [Back to profile](../README.md)", "",
              "## Contributions by month", "", "| Month | Contributions |", "| --- | ---: |"]
    lines += [f"| {month} | {total} |" for month, total in monthly(days)]
    lines += ["", "<details>", "<summary>Daily calendar counts (text equivalent of every heatmap cell)</summary>", "",
              "| Date | Contributions |", "| --- | ---: |"]
    lines += [f"| {day['date']} | {day['count']} |" for day in days]
    lines += ["", "</details>", "", "## Additional public profile counts", "",
              f"Public merged PRs, all time: {snapshot['merged']:,}. Owned public non-forks: {snapshot['repos']:,}. "
              f"Stars across those repositories: {snapshot['stars']:,}. Followers at refresh: {snapshot['followers']:,}.", ""]
    return "\n".join(lines)


def convert_photo(path):
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    image = ImageOps.exif_transpose(Image.open(path)).convert("RGBA")
    background = Image.new("RGBA", image.size, "white")
    image = Image.alpha_composite(background, image).convert("L")
    image = ImageOps.fit(image, (800, 800), Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.15)
    image = ImageEnhance.Brightness(image).enhance(1.20)
    image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
    columns, rows = 180, 96
    image = image.resize((columns, rows), Image.Resampling.LANCZOS)
    ramp = " .,:;irsXA253hMHGS#9B&@"
    output = []
    for y in range(rows):
        line = []
        for x in range(columns):
            lum = image.getpixel((x, y)) / 255
            line.append(" " if lum >= .92 else ramp[round((1 - lum) * (len(ramp) - 1))])
        output.append("".join(line))
    return {"columns": columns, "rows": output}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="One-time conversion of a cropped, background-cleaned local portrait; requires Pillow")
    parser.add_argument("--check", action="store_true", help="Validate committed portrait against its ASCII rows; no photo or Pillow required")
    args = parser.parse_args()
    if args.input and args.check:
        parser.error("--input and --check cannot be combined")
    if args.input:
        data = convert_photo(args.input)
        validate_rows(data)
        PORTRAIT_DATA.parent.mkdir(exist_ok=True)
        PORTRAIT_DATA.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
    data = json.loads(PORTRAIT_DATA.read_text(encoding="utf-8"))
    output = portrait(data)
    for name, content in (("rajveer-ascii.svg", output), ("rajveer-ascii-static.svg", static_svg(output))):
        path = ROOT / "assets" / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit("Stale ASCII portrait; run python scripts/gen_profile.py")
        else:
            path.write_text(content, encoding="utf-8", newline="\n")
    print("ok: reference-style ASCII portrait")


if __name__ == "__main__":
    main()
