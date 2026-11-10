"""Fail when the site's tagline or work-area cards differ from the org profile README's."""
import re
import sys
import urllib.request
from pathlib import Path

PROFILE = "https://raw.githubusercontent.com/Totative/.github/main/profile/README.md"


def profile_copy(md: str) -> tuple[str, list[tuple[str, str]]]:
    tagline = re.search(r'<p align="center">\s*([^<]+?)\s*</p>', md).group(1)
    return tagline, re.findall(r"<b>([^<]+)</b><br>([^<]+)</td>", md)


def site_copy(html: str) -> tuple[str, list[tuple[str, str]]]:
    tagline = re.search(r"<p>([^<]+)</p>", html).group(1)
    return tagline, re.findall(r"<h3>([^<]+)</h3><p>([^<]+)</p>", html)


def main() -> int:
    md = urllib.request.urlopen(PROFILE, timeout=30).read().decode()
    want, have = profile_copy(md), site_copy(Path("index.html").read_text())
    assert want[1], "no cards found in the profile README"
    if want == have:
        print(f"site copy matches the profile: tagline and {len(have[1])} cards")
        return 0
    print(f"profile: {want}\nsite:    {have}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
