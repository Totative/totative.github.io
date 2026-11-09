# totative.github.io

Source for <https://totative.github.io>, where Totative publishes research write-ups and advisories.

Jekyll, built by GitHub Pages. No JavaScript, no external requests.

To add a write-up, create `_posts/YYYY-MM-DD-slug.md` with a `title` in front matter.

Preview with the same builder GitHub runs, since the pinned Jekyll
doesn't run on current Ruby, then serve `_site/`:

```sh
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD":/github/workspace:Z -w /github/workspace \
  -e GITHUB_WORKSPACE=/github/workspace \
  -e INPUT_SOURCE=./ -e INPUT_DESTINATION=./_site -e INPUT_FUTURE=false \
  -e INPUT_VERBOSE=false -e INPUT_BUILD_REVISION=local -e INPUT_TOKEN= \
  ghcr.io/actions/jekyll-build-pages:v1.0.13
python3 -m http.server -d _site 4000
```
