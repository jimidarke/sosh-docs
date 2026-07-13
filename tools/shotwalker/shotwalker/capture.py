"""Take the picture.

The docs' house style bakes the callout into the image -- alt text throughout
reads "...with the Cloud pill outlined" -- and each placeholder's art direction
already names what to highlight. So `highlight=` draws that outline before the
shutter, and the walker emits the annotated image the docs expect rather than a
clean one somebody has to mark up by hand afterwards.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image
from playwright.sync_api import Locator, Page

from . import config, redact


@dataclass
class ShotResult:
    target: str
    path: Path
    ok: bool
    error: str = ""
    held: bool = False  # captured, but deliberately not published
    note: str = ""
    blocked_clicks: list[str] = field(default_factory=list)


_OUTLINE = """
.shotwalker-highlight {
  outline: 3px solid %s !important;
  outline-offset: 2px !important;
  border-radius: 2px;
}
"""


class Shooter:
    """Bound to one page and one target; recipes call it as `shoot(...)`."""

    def __init__(self, page: Page, target: str, out_dir: Path, *, path_hint: str = ""):
        self.page = page
        self.target = target
        self.out_dir = out_dir
        self.path_hint = path_hint
        self.result: ShotResult | None = None

    def __call__(
        self,
        subject: Locator | None = None,
        *,
        highlight: str | list[str] | None = None,
        full_page: bool = False,
        clip: dict | None = None,
    ) -> ShotResult:
        """Shoot `subject` (an element), a `clip` rectangle, or the viewport.

        `clip` exists for content that escapes its own container: an expanded
        <select> renders its list outside the toolbar's box, so an element shot
        of the toolbar slices the options in half.
        """
        out = self.out_dir / Path(self.target).name
        out.parent.mkdir(parents=True, exist_ok=True)

        if highlight:
            selectors = [highlight] if isinstance(highlight, str) else highlight
            self.page.add_style_tag(content=_OUTLINE % config.HIGHLIGHT_COLOUR)
            for sel in selectors:
                # Mark every match; a highlight naming e.g. a tab row is one node,
                # but "the Normal and Onsale dropdowns" is two.
                self.page.eval_on_selector_all(
                    sel, "els => els.forEach(e => e.classList.add('shotwalker-highlight'))"
                )

        masks = redact.secret_masks(self.page, self.path_hint)
        shot_target = subject if subject is not None else self.page

        try:
            if subject is not None:
                subject.scroll_into_view_if_needed()
                subject.screenshot(path=str(out), mask=masks, mask_color=config.MASK_COLOUR)
            elif clip is not None:
                self.page.screenshot(
                    path=str(out), clip=clip, mask=masks, mask_color=config.MASK_COLOUR
                )
            else:
                shot_target.screenshot(
                    path=str(out),
                    full_page=full_page,
                    mask=masks,
                    mask_color=config.MASK_COLOUR,
                )
        except Exception as exc:
            self.result = ShotResult(self.target, out, ok=False, error=str(exc))
            return self.result

        _downscale(out, config.DOC_IMAGE_WIDTH)
        self.result = ShotResult(self.target, out, ok=True)
        return self.result


def _downscale(path: Path, width: int) -> None:
    """Shrink to the 720px width the existing docs/assets/app/ captures use.

    Captured at device_scale_factor=2 for sharpness, then resized down -- that's
    how you get a crisp image instead of a soft one.

    Only ever shrinks. Several panels (the Designer's properties column is 598px
    wide) are already narrower than the target, and blowing them up to 720 would
    just add blur to invent pixels that were never there.
    """
    with Image.open(path) as im:
        if im.width <= width:
            return
        height = round(im.height * width / im.width)
        im.resize((width, height), Image.LANCZOS).save(path, optimize=True)


def baseline(page: Page, out_dir: Path, slug: str, path_hint: str = "") -> Path:
    """Full-page capture for the artifacts sweep.

    Volatile chrome is masked here but *not* in doc shots: run-to-run diffing is
    the whole point of a baseline, and the cloud pill flipping to OFFLINE would
    otherwise churn every image in the corpus.
    """
    out = out_dir / f"{slug}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    masks = redact.secret_masks(page, path_hint) + redact.volatile_masks(page)
    page.screenshot(path=str(out), full_page=True, mask=masks, mask_color=config.MASK_COLOUR)
    return out
