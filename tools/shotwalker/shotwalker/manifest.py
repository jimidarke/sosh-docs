"""The docs declare the shot list; this reads it.

Every page that wants an image carries a placeholder naming the exact file and
the art direction:

    !!! screenshot "Screenshot: the Dashboard right after first sign-in, full
        page, with the Cloud pill and the Access Points tile highlighted"
        To capture: assets/console/dashboard-first-signin.png

Parsing these is what lets the harness be checked against the docs rather than
against someone's memory of what the docs need.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from . import config

# `!!! screenshot "<art direction>"` followed by an indented `To capture: <path>`.
#
# The leading `[ \t]*` is not decoration: four of these live inside numbered list
# items and are therefore indented. Anchoring hard to the start of the line
# silently drops them, which is exactly the kind of miss this manifest exists to
# prevent. The title may also wrap, so consume to the closing quote lazily.
_PLACEHOLDER = re.compile(
    r'^[ \t]*!!! screenshot "(?P<art>.*?)"[ \t]*\n[ \t]+To capture:[ \t]*(?P<target>\S+\.png)',
    re.MULTILINE | re.DOTALL,
)

# A marker with no `To capture:` line names no file, so nothing can fulfil it.
_ORPHAN = re.compile(r'^[ \t]*!!! screenshot\b', re.MULTILINE)

# An image already wired into a page: ![alt](../../assets/designer/foo.png)
_REFERENCE = re.compile(r'!\[[^\]]*\]\([^)]*?(assets/[\w-]+/[\w.-]+\.png)\)')


@dataclass(frozen=True)
class ShotSpec:
    """One screenshot the docs are asking for."""

    target: str  # e.g. "assets/console/dashboard-first-signin.png"
    art_direction: str
    source_page: Path  # the .md that asked for it
    line: int

    @property
    def surface(self) -> str:
        """console | designer | hardware"""
        return Path(self.target).parts[1]

    @property
    def path(self) -> Path:
        """Absolute path the file should land at."""
        return config.DOCS_DIR / self.target

    @property
    def exists(self) -> bool:
        return self.path.is_file()

    def __str__(self) -> str:
        return self.target


def load(docs_dir: Path | None = None) -> list[ShotSpec]:
    """Every screenshot placeholder in the docs, in sorted target order."""
    docs_dir = docs_dir or config.DOCS_DIR
    specs: list[ShotSpec] = []

    for md in sorted(docs_dir.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for m in _PLACEHOLDER.finditer(text):
            art = " ".join(m.group("art").split())  # unwrap multi-line titles
            specs.append(
                ShotSpec(
                    target=m.group("target"),
                    art_direction=art,
                    source_page=md.relative_to(config.REPO_ROOT),
                    line=text.count("\n", 0, m.start()) + 1,
                )
            )

    specs.sort(key=lambda s: s.target)
    return specs


def referenced(docs_dir: Path | None = None) -> set[str]:
    """Images already wired into the docs as `![alt](...)`.

    A shot the docs are *using* is fulfilled, not forgotten. Without this, every
    recipe would flip from "covered" to "stale" the instant its placeholder was
    replaced by the picture it asked for -- which would make `--check` report
    a successful run as 25 orphaned recipes.
    """
    docs_dir = docs_dir or config.DOCS_DIR
    found: set[str] = set()
    for md in docs_dir.rglob("*.md"):
        for m in _REFERENCE.finditer(md.read_text(encoding="utf-8")):
            found.add(m.group(1))
    return found


def orphans(docs_dir: Path | None = None) -> list[tuple[Path, int]]:
    """Placeholders that name no target file.

    A `!!! screenshot` with no `To capture:` line asks for an image without
    saying what to call it, so no recipe can ever satisfy it and no reader will
    ever see it filled. It's a docs bug; surface it rather than skip it.
    """
    docs_dir = docs_dir or config.DOCS_DIR
    found: list[tuple[Path, int]] = []

    for md in sorted(docs_dir.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        complete = {m.start() for m in _PLACEHOLDER.finditer(text)}
        for m in _ORPHAN.finditer(text):
            if m.start() not in complete:
                found.append(
                    (md.relative_to(config.REPO_ROOT), text.count("\n", 0, m.start()) + 1)
                )
    return found


# The surfaces this harness drives. Everything else in docs/assets/ belongs to
# someone else: `app/` is the handheld, captured over adb by sosh's own
# qa-walkthrough; `hardware/` needs a camera; `branding/` is artwork.
BROWSER_SURFACES = ("console", "designer")

# The handheld, driven over adb rather than by a browser. Kept as its own tuple
# because the difference is not cosmetic: the browser surfaces are reveal-only and
# guarded, and this one writes.
DEVICE_SURFACES = ("app",)

# Everything a machine can take. `hardware` is the remainder -- photographs of the
# kit on a bench, which no harness is ever going to produce.
AUTOMATABLE_SURFACES = BROWSER_SURFACES + DEVICE_SURFACES


def capturable(specs: list[ShotSpec]) -> list[ShotSpec]:
    """The ones a machine can take -- browser or handheld."""
    return [s for s in specs if s.surface in AUTOMATABLE_SURFACES]
