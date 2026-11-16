# AGENTS.md

Source for totative.dev, where Totative publishes research write-ups and advisories. Jekyll built by GitHub Pages, with no JavaScript and no external requests; fonts and brand assets are served from `assets/`. The repo name is historical: `_config.yml` sets `url: https://totative.dev`, and a `chore(pages)` commit moved the release to App Platform.

## Layout

- `_posts/YYYY-MM-DD-slug.md`: a write-up, with `title` in front matter; it takes the `writeup` layout and the `/writeups/:title/` permalink.
- `_layouts/`: `default.html`, `writeup.html`. `index.html`, `writeups/index.html`, `404.html`: pages. `assets/site.css`, `assets/fonts` (Atkinson Hyperlegible Next, OFL), `assets/brand`.
- `scripts/check-copy.py`: fails if the tagline and "What we do" cards differ from `Totative/.github` `profile/README.md`. `.github/workflows/copy-sync.yml` runs it on pushes, pull requests and weekly.
- `.well-known/security.txt`. `Gemfile` and `_config.yml` `exclude` keep non-site files out of the build.

## Verify

`python3 -I scripts/check-copy.py`, `bunx --bun markdownlint-cli2 '**/*.md'`, and the preview build in `README.md` (the GitHub Pages builder image, since the pinned Jekyll does not run on current Ruby); serve `_site/` and open the page.

## Invariants

- No JavaScript, no third-party requests, no analytics. Keep `404.html` and `security.txt` working.
- Change the tagline or cards here and in `Totative/.github` in the same sitting.
- Never publish a write-up before its disclosure deadline (see `DISCLOSURE.md` in `Totative/.github`).
- Workflow actions are pinned to a full commit SHA.
