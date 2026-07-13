"""The Commander console walk (:8080).

The nav is enumerated live, from the DOM, on every run. Nothing here hardcodes
the page list: if a new nav item ships, the walker finds it, sweeps it, and the
coverage report names it as uncovered. That's the difference between a harness
that tracks the product and a list that rots.

Selector notes, since the console has no data-testid anywhere:
  * The Dashboard's tiles carry real ids (#card-cloud, #card-aps) -- these map
    one-to-one onto what the docs ask to highlight.
  * The chip/table pages use data-* (data-filter, data-value).
  * Cards without ids are reached through the control they contain, e.g.
    `.card:has(#pin-input)`. That survives re-ordering, which nth-child doesn't.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from playwright.sync_api import Page

from . import config, session
from .recipes import recipe

SURFACE = "console"


def url(path: str = "/") -> str:
    return f"{config.console_url()}{path}"


# Live routes that the sidebar deliberately does not link. They can't be
# discovered by enumeration -- by definition -- so they're listed explicitly.
HIDDEN_ROUTES = [
    ("Monitor (kiosk)", "/monitor"),
    ("Push", "/push"),
    ("Assignments", "/assignments"),
    ("API docs", "/admin/api-docs"),
]


@dataclass(frozen=True)
class NavItem:
    section: str
    label: str
    href: str

    @property
    def slug(self) -> str:
        s = self.href.strip("/").replace("/", "-") or "dashboard"
        return s


def enumerate_nav(page: Page) -> list[NavItem]:
    """Read the left navigation out of the live DOM."""
    page.goto(url("/"), wait_until="domcontentloaded")
    session.settle(page)

    raw = page.evaluate(
        """() => {
            const out = [];
            for (const sec of document.querySelectorAll('aside.sidebar .nav-section')) {
              const label = sec.querySelector('.nav-section-label');
              const section = label ? label.textContent.trim() : '';
              for (const a of sec.querySelectorAll('a.nav-link')) {
                out.push({
                  section,
                  label: a.textContent.trim(),
                  href: a.getAttribute('href'),
                });
              }
            }
            // The Help link lives in a pinned footer, outside the nav sections.
            for (const a of document.querySelectorAll('aside.sidebar .sidebar-foot a.nav-link')) {
              out.push({ section: 'Help', label: a.textContent.trim(), href: a.getAttribute('href') });
            }
            return out;
        }"""
    )
    return [NavItem(**r) for r in raw if r["href"] and r["href"].startswith("/")]


# e.g. 1.0.0-20260713-134730 — the provisioned Commander bundle.
_BUILD_VERSION = re.compile(r"\d+\.\d+\.\d+(?:-[\w.]+)*")


def commander_version(page: Page) -> str:
    """The bundle version, which is what actually determines the pixels.

    Read from the Dashboard's Build Version tile. Scanning the System page for
    "a line mentioning version" instead picked up the *help pack* version — both
    say "version", and the wrong one stamps every run with a number that has
    nothing to do with the UI in the images.
    """
    try:
        page.goto(url("/"), wait_until="domcontentloaded")
        session.settle(page)
        tile = page.locator("#card-build")
        if tile.count():
            m = _BUILD_VERSION.search(tile.inner_text())
            if m:
                return m.group(0)
    except Exception:
        pass
    return "unknown"


# --------------------------------------------------------------------------
# Recipes -- one per screenshot the docs ask for.
# --------------------------------------------------------------------------


@recipe("assets/console/dashboard-first-signin.png", SURFACE)
def dashboard_first_signin(page: Page, shoot) -> None:
    """Full Dashboard; the docs want the Cloud pill and Access Points tile called out."""
    page.goto(url("/"))
    session.settle(page)
    shoot(highlight=["#card-cloud", "#card-aps"], full_page=True)


@recipe("assets/console/tags-search-and-size-chips.png", SURFACE)
def tags_search_and_size_chips(page: Page, shoot) -> None:
    """The search box and the three size chips.

    Viewport, not full page. The bench box has 81 tags, and a full-page shot
    came out 13,642px tall -- a picture of the entire fleet when the subject is
    a filter bar at the top.
    """
    page.goto(url("/fleet"))
    session.settle(page)
    shoot(highlight=["#search", '.chip[data-filter="type"]'])


@recipe("assets/console/tag-detail-bind-card.png", SURFACE)
def tag_detail_bind_card(page: Page, shoot) -> None:
    """The Bind Tag card, Preview and Push highlighted.

    The tag address is discovered live, never hardcoded -- a fixed address would
    rot the first time the bench box is reflashed.

    Fleet rows are not links. They're divs carrying `data-addr`, navigated by JS,
    so there is no <a href="/tags/..."> to follow; the address comes off the
    attribute and the URL is built from it.
    """
    page.goto(url("/fleet"))
    session.settle(page)

    # Filter to unbound tags first. The lesson this illustrates is "Bind your
    # first tag", and an already-bound tag titles the card "Re-bind Tag" -- so
    # picking any old tag produced an image whose heading contradicted the page
    # it sits on.
    unbound = page.locator('.chip[data-value="unbound"]')
    if unbound.count():
        unbound.first.click()
        page.wait_for_timeout(800)

    addr = page.evaluate(
        """() => {
            const el = document.querySelector('[data-addr]');
            return el ? el.getAttribute('data-addr') : null;
        }"""
    )
    if not addr:
        raise RuntimeError("no unbound tags on /fleet — cannot show a first-bind card")

    page.goto(url(f"/tags/{addr}"))
    session.settle(page)
    card = page.locator(".card:has(#bind-form)").first
    shoot(card, highlight=["#bind-preview", "#bind-push"])


@recipe("assets/console/products-page-synced.png", SURFACE)
def products_page_synced(page: Page, shoot) -> None:
    """A synced catalog, search box called out. Viewport — the full catalog is
    thousands of pixels tall and the subject is the top of the page."""
    page.goto(url("/products"))
    session.settle(page)
    shoot(highlight="#search")


@recipe("assets/console/pos-config-tabs.png", SURFACE)
def pos_config_tabs(page: Page, shoot) -> None:
    """All four source tabs visible, the tab row called out."""
    page.goto(url("/admin/pos-config"))
    session.settle(page)
    shoot(highlight="#pos-tabs", full_page=True)


@recipe("assets/console/system-picker-pin-card.png", SURFACE)
def system_picker_pin_card(page: Page, shoot) -> None:
    """The Picker PIN card.

    The PIN itself is masked by redact.py, and the guard blocks #pin-reveal-btn,
    so the card is capturable without the secret ever reaching the PNG.
    """
    page.goto(url("/system"))
    session.settle(page)
    card = page.locator(".card:has(#pin-input)").first
    # The docs ask for the default-PIN warning and the Set PIN button, which is
    # the pair a reader needs to act on -- not the input box.
    shoot(card, highlight=[".badge:has-text('Default PIN')", "button:has-text('Set PIN')"])


@recipe("assets/console/mobile-devices-pairing-qr.png", SURFACE)
def mobile_devices_pairing_qr(page: Page, shoot) -> None:
    page.goto(url("/admin/mobile-binding"))
    session.settle(page)
    card = page.locator(".card:has(#rotateBtn)").first
    if card.count() == 0:
        card = page.locator(".card").first
    shoot(card)


@recipe("assets/console/templates-defaults-card.png", SURFACE)
def templates_defaults_card(page: Page, shoot) -> None:
    """HELD: the dropdowns this shot is *about* render black-on-black.

    Captured anyway so the artifacts show the bug, but known_issues.HELD keeps
    it out of the docs until the styling is fixed in sosh.
    """
    page.goto(url("/templates"))
    session.settle(page)
    card = page.locator(".card:has(select[data-role='default-select'])").first
    if card.count() == 0:
        raise RuntimeError("no Defaults card on /templates")
    shoot(card, highlight="select[data-role='default-select']")


@recipe("assets/console/templates-library-card.png", SURFACE)
def templates_library_card(page: Page, shoot) -> None:
    """The Template Library card, with a downloadable row.

    Mis-filed by the docs under designer/ — it's a console page. Kept at the
    target the docs name so the reference resolves; flagged in the report rather
    than silently renamed.

    The emptiness check matters. The docs want "one row's Download button and
    badge highlighted"; on a bench box with no library content the card just
    reads "No library templates available to download yet". Publishing that
    would put an image in the docs that contradicts the text beside it, so this
    fails loudly instead — the library needs content before the shot can exist.
    """
    page.goto(url("/templates"))
    session.settle(page)

    card = page.locator(".card:has(#library-list)").first
    rows = page.locator("#library-list [data-lib-download]")
    if rows.count() == 0:
        raise RuntimeError(
            "Template Library is empty on this Commander — the shot needs at "
            "least one downloadable row; seed the library, then re-run with "
            "--only assets/console/templates-library-card.png"
        )

    shoot(card, highlight="[data-lib-download]")


@recipe("assets/console/templates-purpose-pill.png", SURFACE)
def templates_purpose_pill(page: Page, shoot) -> None:
    """HELD: black-on-black dropdown. Console page, mis-filed under designer/."""
    page.goto(url("/templates"))
    session.settle(page)
    pill = page.locator("[data-tpl-purpose]").first
    if pill.count() == 0:
        raise RuntimeError("no template cards on /templates")
    pill.click()
    page.wait_for_timeout(300)
    card = page.locator(".card:has([data-tpl-purpose])").first
    shoot(card, highlight="[data-tpl-purpose]")


@recipe("assets/console/templates-defaults-pair.png", SURFACE)
def templates_defaults_pair(page: Page, shoot) -> None:
    """HELD: black-on-black dropdown. Console page, mis-filed under designer/."""
    page.goto(url("/templates"))
    session.settle(page)
    card = page.locator(".card:has(select[data-role='default-select'])").first
    if card.count() == 0:
        raise RuntimeError("no Defaults card on /templates")
    shoot(card, highlight="select[data-role='default-select']")
