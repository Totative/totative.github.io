"""Fail when the site's tagline, work-area cards or tools list differ from the org profile README's."""

import re
import sys
import urllib.request
from pathlib import Path

PROFILE = "https://raw.githubusercontent.com/Totative/.github/main/profile/README.md"


def profile_copy(md: str) -> tuple[str, list[tuple[str, str]], list[tuple[str, str]]]:
    tagline = re.search(r'<p align="center">\s*([^<]+?)\s*</p>', md).group(1)
    tools = re.findall(
        r"^- \[([^\]]+)\]\(https://github\.com/Totative/[^)]+\): (.+)$", md, re.M
    )
    return tagline, re.findall(r"<b>([^<]+)</b><br>([^<]+)</td>", md), tools


def site_copy(html: str) -> tuple[str, list[tuple[str, str]], list[tuple[str, str]]]:
    tagline = re.search(r"<h1>([^<]+)</h1>", html).group(1)
    tools = re.findall(
        r'<li><a href="https://github\.com/Totative/[^"]+">([^<]+)</a>: ([^<]+)</li>',
        html,
    )
    return tagline, re.findall(r"<h3>([^<]+)</h3><p>([^<]+)</p>", html), tools


def check_canonical(layout: str) -> None:
    if '<link rel="canonical" href="https://totative.dev{{ page.url }}">' not in layout:
        raise SystemExit("pages need a totative.dev canonical")


def check_home_h1(html: str) -> None:
    if re.search(r"^<h1>[^<]+</h1>\s*$", html, re.M) is None:
        raise SystemExit("home lede must be an h1")


def check_404_noindex(layout: str, not_found: str) -> None:
    branch = re.search(
        r"\{%\s*if page\.noindex\s*%\}(.*)\{%\s*else\s*%\}(.*)\{%\s*endif\s*%\}",
        layout,
        re.S,
    )
    if branch is None:
        raise SystemExit("default layout needs a page.noindex branch")
    if 'name="robots" content="noindex"' not in branch.group(1):
        raise SystemExit("noindex branch missing robots meta")
    if 'rel="canonical"' in branch.group(1):
        raise SystemExit("noindex branch must not emit canonical")
    if re.search(r"^noindex:\s*true\s*$", not_found, re.M) is None:
        raise SystemExit("404.html needs noindex: true")


def main() -> int:
    layout = Path("_layouts/default.html").read_text()
    check_canonical(layout)
    index = Path("index.html").read_text()
    check_home_h1(index)
    check_404_noindex(layout, Path("404.html").read_text())
    md = urllib.request.urlopen(PROFILE, timeout=30).read().decode()
    want, have = profile_copy(md), site_copy(index)
    assert want[1], "no cards found in the profile README"
    if want == have:
        print(
            f"site copy matches the profile: tagline, {len(have[1])} cards, {len(have[2])} tools"
        )
        return 0
    print(f"profile: {want}\nsite:    {have}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
