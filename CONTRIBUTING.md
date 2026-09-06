# Contributing

This repository powers Rajveer Vadnal's GitHub profile. Corrections to links, wording and presentation are welcome.

## Editing

- Update `README.md` for profile content and `assets/profile-header.svg` for the banner.
- Keep project claims tied to public releases, source, reports or documented status. Distinguish research plans from completed results.
- `assets/github-stats.svg` and `assets/project-index.svg` are generated. Update `scripts/gen_stats.py` or `scripts/gen_projects.py` rather than editing their output.
- Private project names come only from `data/private-projects.json`. Add entries only with the owner's explicit approval.

## Preview and checks

Preview the README at desktop and narrow widths. Check new links and SVG readability, then run:

```bash
python -m py_compile scripts/gen_stats.py scripts/gen_projects.py
git diff --check
```

To refresh the archive assets locally, authenticate with `gh auth login` or provide `GITHUB_TOKEN`, then run:

```bash
python scripts/gen_stats.py
python scripts/gen_projects.py
```

The `Refresh profile assets` workflow runs these generators daily and after changes on `main`.

Open a focused pull request describing the correction and how you checked it.
