# Contributing

This repository powers Rajveer Vadnal's GitHub profile. Corrections to links, wording and presentation are welcome.

## Editing

- Keep `README.md` visual-first: SVG panels plus short native link rows. Put detailed descriptions, attribution, regression checks, and accessible text in `docs/profile-evidence.md`. Keep image alt text meaningful; SVG-internal links do not work when an image is embedded in GitHub.
- Update `scripts/gen_atlas.py` for the hero, overview, execution atlas, selected systems, flight recorder, evaluation, working set, and contact panels. Run it to regenerate all light/dark and narrow-screen variants. Do not edit those generated SVGs by hand. Keep visual claims, alt text, and the text companion consistent.
- Keep project claims tied to public releases, source, reports or documented status. Atlas paths describe project roles, not implemented integrations. The flight recorder summarizes a pinned public commit, not a simulated live session.
- `assets/github-stats.svg`, `assets/project-index.svg`, and `docs/public-repositories.md` are generated. Update `scripts/gen_stats.py` or `scripts/gen_projects.py` rather than editing their output.
- Include public repositories only. Keep forks marked and organization namespaces visible in the linked index; inclusion does not imply sole authorship.
- `docs/execution-atlas.html` preserves the approved interactive design as a downloadable single file. Its dated repository snapshot is separate from the daily generated catalog.

## Preview and checks

Preview the GitHub-rendered README at desktop and narrow widths in both color themes. Check new links, image alternative text, and SVG readability, then run:

```bash
python -m py_compile scripts/*.py
python -m unittest discover -s scripts -v
python scripts/gen_atlas.py --check
git diff --check
```

To regenerate the design panels:

```bash
python scripts/gen_atlas.py
```

To refresh the public catalog and activity snapshot locally, authenticate with `gh auth login` or provide `GITHUB_TOKEN`, then run:

```bash
python scripts/gen_stats.py
python scripts/gen_projects.py
```

The `Refresh profile assets` workflow validates changes on pull requests and `main`. On `main` and the daily schedule it also refreshes the public API assets. Its generated-only commits do not recursively trigger refreshes.

Open a focused pull request describing the correction and how you checked it.
