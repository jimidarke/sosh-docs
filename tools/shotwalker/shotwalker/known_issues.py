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
    "assets/console/sales-orders-page.png": (
        "The 'Sync now' button is invisible. It carries Bootstrap's `btn-outline-light` "
        "-- white text, white border, for use on a dark background -- and sits on the "
        "console's near-white page (main.main is rgb(245,245,247)), so it renders as an "
        "empty outline. The docs art-direct this shot to call that button out, and the "
        "capture came back with a highlight box around nothing. Worth fixing in sosh "
        "regardless of the screenshot: it is the primary action on the page, and it is "
        "invisible to every user. `btn-outline-primary` or `-secondary` would do it. "
        "The rest of the shot (populated table, filter summary) is good, so re-run with "
        "--only once the class is fixed."
    ),
    "assets/console/templates-defaults-pair.png": (
        "Asks for the 'Saved tick', which the page only renders after a default is "
        "saved -- a write. Shotwalker is reveal-only, so this shot is not capturable "
        "as specified. (The black-on-black dropdown bug it was also held on is fixed "
        "as of Commander 1.0.0-20260713-175438; this blocker is the one that remains.) "
        "Either re-spec the placeholder without the tick, or shoot it by hand."
    ),
}

# Fixed in Commander 1.0.0-20260713-175438: the Templates-page dropdowns rendered
# black-on-black, which held `templates-defaults-card` and `templates-purpose-pill`.
# They now compute to rgb(14,14,14) on rgb(255,255,255) and are published.
# `templates-defaults-pair` stays held -- see above; its blocker was never the colour.

# Shots no recipe can take, and why.
#
# This is not the same thing as a gap. A gap says "somebody should write this
# recipe"; these say "no recipe is possible until something else changes." Rolling
# them together would put permanent entries on a to-do list that is supposed to
# shrink to zero -- and would quietly invite the fix of last resort, which is to
# widen the guard until the shot works. The guard is the reason shotwalker is safe
# to point at a customer's Commander. It does not move for a screenshot.
#
# Each of these is answered by re-speccing the placeholder or shooting it by hand.
BLOCKED = {
    "assets/app/wizard-scan-qr.png": (
        "Shows the pairing wizard, which only exists on an *unpaired* handheld. The "
        "bench phone is paired and Active, so capturing this means unpairing a working "
        "device and pairing it again afterwards -- a destructive round trip that a "
        "screenshot run has no business doing on its own. Deliberately skipped, not "
        "forgotten. Do it by hand, or shoot it on a phone that is being provisioned "
        "for the first time anyway."
    ),
    "assets/app/wizard-paired.png": (
        "Same as wizard-scan-qr: the wizard's success screen exists only during a "
        "first pairing. Capturing it means unpairing the bench handheld first."
    ),
    "assets/designer/image-library-crop.png": (
        "The Image Library cannot be opened at all. designer/index.html declares "
        "id='library-modal' twice -- Shared Template Library first, Image Library "
        "second -- and the handler behind #btn-image-library resolves it with "
        "getElementById, which returns the first. Clicking 'Image Library' opens the "
        "*template* library; the Image Library modal never leaves display:none, so the "
        "crop dialog behind it is unreachable. A sosh bug, not a capture problem: the "
        "feature c06 documents is currently broken in the UI. Fix the duplicate id, "
        "then write the recipe."
    ),
    "assets/console/pos-localapi-keys.png": (
        "Asks for 'a freshly generated key banner'. The banner is #key-new, which is in "
        "redact.SECRET_SELECTORS and is therefore blacked out in every capture -- the "
        "subject of the shot is a secret, and this repo is public. Minting one also "
        "needs #key-mint-btn, which is forbidden. Re-spec the placeholder around the "
        "keys *card* with the key masked, or drop it."
    ),
    "assets/console/pos-odoo-form.png": (
        "Art-directed to highlight the Base URL field. That field is #odoo-base-url, in "
        "redact.SECRET_SELECTORS (infrastructure), so the shot would outline a black "
        "rectangle. Re-spec it to call out a field that can actually be shown."
    ),
    "assets/console/pos-localdb-detect-results.png": (
        "Needs the results of 'Detect on LAN' -- a #sql-scan-btn click and a POST. Both "
        "are blocked: the button is forbidden and the network guard aborts the request. "
        "There is also no SQL Server on the bench LAN to find. Hand-shoot."
    ),
    "assets/console/pos-localdb-test-ok.png": (
        "Needs a successful 'Test connection' -- a POST the network guard aborts, "
        "against a SQL Server the bench does not have. Hand-shoot."
    ),
    "assets/console/pos-spire-test-ok.png": (
        "Needs a successful 'Test connection' -- a POST the network guard aborts, "
        "against a Spire server the bench does not have. Hand-shoot."
    ),
    "assets/console/pos-odoo-test-ok.png": (
        "Needs a successful 'Test connection' -- a POST the network guard aborts, "
        "against an Odoo server the bench does not have. Hand-shoot."
    ),
}


# Defects worth reporting that do not block any published shot.
NOTED = [
    (
        "Will-Call once leaked the internal string 'orchestrator :8750' in its empty "
        "state. NOT reproducible on Commander 1.0.0-20260713-175438: searched the "
        "rendered text with no bins, and the rendered text *and* raw HTML with bins and "
        "an assignment -- zero hits for either 'orchestrator' or '8750'. Recorded as "
        "fixed rather than deleted, because it now matters more than it did: the docs "
        "declare three Will-Call shots, so a regression here would land in a committed "
        "image on a public site rather than in the gitignored sweep. Re-check the empty "
        "state before shooting these on a fresh Commander."
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
        "assets/console/templates-library-card.png cannot be shot, and not for the "
        "reason previously recorded here. The Template Library is not local state that "
        "a bench operator can seed: it is sosh's *published* catalog, which the "
        "Commander fetches. GET /api/templates/library/available answers "
        "{'available': true, 'items': []} -- the service is up and the catalog is "
        "empty. So the card correctly says 'No library templates available to download "
        "yet', while the doc beside it describes a Download button on a library row. "
        "Nothing on this Commander can fix that; someone has to publish a template to "
        "the sosh library. The recipe raises until they do."
    ),
]


def is_held(target: str) -> bool:
    return target in HELD


def reason(target: str) -> str:
    return HELD.get(target, "")


def is_blocked(target: str) -> bool:
    return target in BLOCKED


def blocked_reason(target: str) -> str:
    return BLOCKED.get(target, "")
