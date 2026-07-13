"""UI defects that affect what a capture would show.

These live in the `sosh` repo, not here. They're recorded so the report says
"blocked on a known bug" instead of quietly shipping a bad image, and so nobody
re-diagnoses them next time.

Source: sosh/docs/trackers/2026-07-11-guardian-training-docs.md, which asks for
both to be fixed before shooting. We chose to shoot first and re-take the
affected shots later with `--only`.
"""

from __future__ import annotations

# Captured into artifacts/ for inspection, but NOT published into docs/assets/.
# A known-bad image baked into permanent documentation is worse than a missing
# one -- the placeholder at least tells the truth.
HELD = {
    "assets/console/templates-defaults-card.png": (
        "Templates-page dropdowns render black-on-black (sosh UI bug); the "
        "dropdown is the subject of this shot, so it would be unreadable"
    ),
    "assets/console/templates-defaults-pair.png": (
        "Two blockers. The dropdowns render black-on-black (sosh UI bug), AND "
        "the shot asks for the 'Saved tick', which only appears after saving a "
        "default -- a write. Shotwalker is reveal-only, so this shot is not "
        "capturable as specified even once the styling is fixed. Either re-spec "
        "it without the tick, or shoot it by hand."
    ),
    "assets/console/templates-purpose-pill.png": (
        "Templates-page purpose-pill dropdown renders black-on-black (sosh UI bug)"
    ),
}

# Defects worth reporting that do not block any published shot.
NOTED = [
    (
        "Will-Call empty state leaks the internal string 'orchestrator :8750'. "
        "No Will-Call shot is declared in the docs, so this never reaches a "
        "committed image -- it appears only in the gitignored artifacts sweep."
    ),
    (
        "designer/index.html declares id='library-modal' twice (Shared Template "
        "Library, then Image Library). getElementById returns the first, so the "
        "Image Library is unreachable by id."
    ),
    (
        "The console renders a broken <img> for tags with no pushed image and "
        "templates with no thumbnail (/tag-image/<addr> and /thumbnail both 404). "
        "Real device state, not a regression -- but a placeholder would look "
        "better than a broken-image icon. 14 on /fleet, 18 on /weather-settings."
    ),
    (
        "assets/console/templates-library-card.png cannot be shot on a Commander "
        "whose Template Library is empty -- the card just says 'No library "
        "templates available to download yet', while the doc describes a "
        "Download button on a library row. Seed the library, then re-run with "
        "--only."
    ),
]


def is_held(target: str) -> bool:
    return target in HELD


def reason(target: str) -> str:
    return HELD.get(target, "")
