"""Reveal-only, enforced by the harness rather than by good intentions.

A recipe is allowed to change what is on screen -- open a modal, switch a tab,
expand a panel. It is not allowed to change the device. Two independent guards
enforce that, because a screenshot script that quietly pushes to a live tag
fleet is a bad day:

1. A network guard. Every non-GET request is aborted unless it matches a narrow
   allowlist of endpoints that write nothing. This is the airtight one: no
   matter what gets clicked, no mutation reaches the Commander.

2. A DOM guard. A capture-phase click listener swallows clicks on known
   mutating controls before they fire, so we also never *attempt* the thing.

The network guard alone would be sufficient for safety. The DOM guard is there
so that a mis-aimed recipe fails loudly during development instead of silently
capturing a half-submitted form.
"""

from __future__ import annotations

import re

from playwright.sync_api import Page, Route

DEFAULT_MASK = "#0B1F3A"


class MutationBlocked(RuntimeError):
    """A recipe tried to touch something that would change the device."""


# Controls that write to the device. Clicking any of these is a bug in a recipe.
FORBIDDEN_SELECTORS = [
    # Console -- tag fleet
    "#bind-push",
    "#bind-submit",
    "#btn-unbind",
    "#btn-flash",
    "#push-now",
    # Console -- system: backup, restore, secrets, PIN
    "#backup-btn",
    "#restore-btn",
    "#restore-usb-btn",
    "#secrets-export-btn",
    "#secrets-restore-btn",
    "#pin-reveal-btn",  # would print the PIN into the DOM
    "#help-btn",
    # Console -- POS: scans, tests, saves, key minting
    "#sql-save-btn",
    "#spire-save-btn",
    "#odoo-save-btn",
    "#sql-scan-btn",
    "#sql-run-btn",
    "#sql-clear-btn",
    "#spire-run-btn",
    "#odoo-run-btn",
    "#key-mint-btn",
    "#localapi-activate-btn",
    # Console -- POS: "Test connection" is not a write *here*, but it opens an
    # outbound connection to a customer's POS database with whatever credentials
    # are in the form. On someone else's Commander that is a real side effect --
    # an auth attempt, possibly a lockout -- so it stays forbidden, and the four
    # `*-test-ok` shots the docs ask for are hand-shot rather than walked.
    "#sql-test-btn",
    "#spire-test-btn",
    "#odoo-test-btn",
    # Console -- templates
    "[data-tpl-delete]",
    "[data-tpl-duplicate]",
    "[data-lib-download]",
    "#upload-template-btn",
    ".purpose-save",  # commits a template's purpose change
    # Console -- images, sales orders
    "#upload-image-btn",
    "#sync-now-btn",
    # Console -- will-call. These are plain <form> submits with no ids of their own,
    # so they are reached through the action they post to: releasing an assignment
    # blanks a customer's live pickup sign, and deleting a bin unbinds a real tag.
    'form[action^="/admin/willcall/release/"] button',
    'form[action^="/admin/willcall/bin/delete/"] button',
    'form[action="/admin/willcall/assign"] button',
    'form[action="/admin/willcall/bin/create"] button',
    # Designer -- anything that persists or pushes
    "#btn-save",
    "#btn-render",
    "#btn-render-push",
    "#btn-delete",
    "#library-upload-btn",
]

# POSTs that a page fires on its own, just to render itself, and that change
# nothing a user would care about. These are not actions the walker *chooses* --
# they happen when any human opens the page -- and blocking them means capturing
# a broken page rather than the page.
#
# Each entry earned its place by showing up in the guard's blocked list during a
# smoke run, i.e. the guard found them, which is the guard working:
#
#   /admin/mobile-binding/mint   the pairing QR is minted on page load. Blocking
#                                it left the QR card empty -- and a shot of that
#                                card is one of the images the docs ask for. The
#                                token is short-lived and self-expiring, and the
#                                explicit "New code" button (#rotateBtn) stays
#                                forbidden, so we never mint a *second* one.
#   /api/weather/preview         renders a preview image. Writes nothing.
#   render/preview endpoints     the Designer round-trips the canvas through the
#                                renderer to produce the preview popup image.
#   /render/direct               the Designer's preview render. api-client.js
#                                posts canvas JSON and gets an image back; it
#                                takes no tag address and cannot push. The push
#                                path is a different call, and is disabled
#                                outright in vault workbench mode.
ALLOWED_WRITE_PATHS = [
    re.compile(r"/api/(render|preview)"),
    re.compile(r"/render/direct"),
    re.compile(r"/render/preview"),
    re.compile(r"/api/templates/preview"),
    re.compile(r"/api/weather/preview"),
    re.compile(r"/admin/mobile-binding/mint"),
]

_SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

# Populated by the page guards so the report can show what was stopped.
blocked_requests: list[str] = []
blocked_clicks: list[str] = []


def _is_allowed(method: str, url: str) -> bool:
    if method.upper() in _SAFE_METHODS:
        return True
    return any(p.search(url) for p in ALLOWED_WRITE_PATHS)


def install(page: Page) -> None:
    """Arm both guards on a page. Call before the first navigation."""

    def _route(route: Route) -> None:
        req = route.request
        if _is_allowed(req.method, req.url):
            route.continue_()
        else:
            blocked_requests.append(f"{req.method} {req.url}")
            route.abort()

    page.route("**/*", _route)

    selectors = ",".join(FORBIDDEN_SELECTORS)
    page.add_init_script(
        """
        (selectors => {
          window.__shotwalker_blocked = [];
          addEventListener('click', e => {
            const hit = e.target.closest && e.target.closest(selectors);
            if (hit) {
              e.preventDefault();
              e.stopImmediatePropagation();
              window.__shotwalker_blocked.push(hit.id || hit.className || 'unknown');
            }
          }, true);  // capture phase: beat the page's own handlers
        })(%r);
        """
        % selectors
    )


def drain_blocked_clicks(page: Page) -> list[str]:
    """Anything the DOM guard swallowed since the last call."""
    try:
        hits = page.evaluate(
            "() => { const b = window.__shotwalker_blocked || []; "
            "window.__shotwalker_blocked = []; return b; }"
        )
    except Exception:
        return []
    blocked_clicks.extend(hits)
    return hits


def assert_safe(selector: str) -> None:
    """Raise if a recipe is about to click something it must not."""
    if selector in FORBIDDEN_SELECTORS:
        raise MutationBlocked(
            f"{selector!r} mutates the device; shotwalker is reveal-only"
        )
