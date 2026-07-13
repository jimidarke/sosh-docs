"""Swap fulfilled placeholders for real image references.

A `!!! screenshot` block is a promise; once the PNG exists, the promise should
become the picture. This does that swap, and only for targets whose file is
actually on disk -- so a held or failed shot keeps its placeholder, and the docs
keep telling the truth about what's missing.

Idempotent and re-runnable: when a held shot is finally captured, run it again
and only that one block turns into an image.

Two details that would otherwise break the build:

* Paths must be relative to the *page*, not the site root. `mkdocs.yml` sets
  `strict: true`, which turns a bad relative path into a build failure -- but an
  absolute `/assets/...` path sails through the build and silently 404s for the
  reader. Relative is the only option that fails loudly when it's wrong.

* Indentation must be preserved. Four placeholders sit inside numbered list
  items; an image dedented to column 0 would end the list and reflow the page.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from . import config, manifest

# The whole block: the admonition line plus its indented `To capture:` line.
_BLOCK = re.compile(
    r'(?P<indent>[ \t]*)!!! screenshot "(?P<art>.*?)"[ \t]*\n'
    r'[ \t]+To capture:[ \t]*(?P<target>\S+\.png)[ \t]*\n',
    re.MULTILINE | re.DOTALL,
)


@dataclass
class Wired:
    page: Path
    target: str
    alt: str


def _alt_text(art: str) -> str:
    """Turn the art direction into alt text.

    The direction is written for whoever takes the shot ("Screenshot: the
    Dashboard..., with the Cloud pill highlighted"). Alt text is for a reader who
    cannot see the image, so drop the instruction to the photographer and keep
    the description -- and say "outlined", which is what the reader would see,
    matching the phrasing already used across docs/assets/app/.
    """
    text = re.sub(r"^Screenshot:\s*", "", art).strip()
    text = re.sub(r";\s*highlight\s+", ", with ", text)
    text = text.replace(" highlighted", " outlined")
    return text[:1].upper() + text[1:]


def _relative(target: str, page: Path) -> str:
    """Path from the page to the image, e.g. ../../assets/designer/x.png."""
    img = (config.DOCS_DIR / target).resolve()
    start = (config.DOCS_DIR / page.relative_to("docs")).parent.resolve()

    up = []
    base = start
    while not str(img).startswith(str(base) + "/"):
        up.append("..")
        base = base.parent
    rel = img.relative_to(base)
    return "/".join(up + [str(rel)]) if up else str(rel)


def run(apply: bool = False) -> list[Wired]:
    """Replace placeholders whose image exists. Returns what changed."""
    specs = {s.target: s for s in manifest.load()}
    done: list[Wired] = []

    pages = sorted({s.source_page for s in specs.values()})
    for page in pages:
        path = config.REPO_ROOT / page
        text = path.read_text(encoding="utf-8")

        def swap(m: re.Match) -> str:
            target = m.group("target")
            spec = specs.get(target)
            if not spec or not spec.exists:
                return m.group(0)  # not captured yet — leave the promise in place

            indent = m.group("indent")
            alt = _alt_text(m.group("art"))
            rel = _relative(target, page)
            done.append(Wired(page=page, target=target, alt=alt))
            return f"{indent}![{alt}]({rel})\n"

        updated = _BLOCK.sub(swap, text)
        if apply and updated != text:
            path.write_text(updated, encoding="utf-8")

    return done
