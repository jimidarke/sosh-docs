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
from datetime import datetime, timezone

from playwright.sync_api import Page

from . import config, session
from .recipes import recipe
from .selects import SELECT_SUBSTITUTE_NOTE, clip_around, expand_in_place, open_select

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


@recipe("assets/console/pos-spire-form.png", SURFACE)
def pos_spire_form(page: Page, shoot) -> None:
    """The Spire tab: Detect-on-LAN card above, connection details below.

    The host field is masked by redact.py (it is a customer's server), so the form
    ships with one blacked-out box. That is fine here and would not be fine for the
    Odoo shot: this one is art-directed at the *form*, and `pos-odoo-form` is
    art-directed at the Base URL field itself, which is why that one is blocked
    rather than written.

    The bench has no Spire, so the form loads empty -- and the docs ask for it "filled
    in", because the lesson is about what goes in each box. Company and Username are
    typed with obvious stand-ins. The host is not: it is masked either way, so a fake
    one would buy nothing, and the password stays empty for the same reason. Typing is
    client-side; #spire-save-btn, #spire-test-btn and #spire-run-btn are all forbidden.
    """
    page.goto(url("/admin/pos-config"))
    session.settle(page)

    page.click("#tab-spire")
    page.wait_for_timeout(500)

    pane = page.locator("#pane-spire")
    if not pane.is_visible():
        raise RuntimeError("the Spire tab did not open")

    form = pane.locator(".card:has(#spire-form)").first
    if form.count() == 0:
        raise RuntimeError("no Spire connection-details card")

    if page.locator("#spire-company").input_value() == "":
        page.locator("#spire-company").fill("ACME-RETAIL")
    if page.locator("#spire-username").input_value() == "":
        page.locator("#spire-username").fill("shelf-sync")
    page.wait_for_timeout(200)

    shoot(pane, highlight=["#spire-form", ".card:has(#spire-scan-btn)"])


@recipe("assets/console/images-page.png", SURFACE)
def images_page(page: Page, shoot) -> None:
    """The Images page: the library, and the required-size reference table.

    Both halves are the subject -- c06's rule is "an image must match the
    placeholder's size exactly", and the reference table is what tells a reader
    which size that is. An empty library would illustrate neither.
    """
    page.goto(url("/images"))
    session.settle(page)

    if page.locator("#img-grid [data-img-id]").count() == 0:
        raise RuntimeError(
            "the Image library is empty — the shot is of 'a few uploads' plus the "
            "size table; upload an image, then re-run with --only"
        )

    # The size table is a <details>, collapsed on load -- so the first take of this
    # shot highlighted a closed disclosure triangle and called it a reference table.
    # It is half the subject: c06's rule is that an image must match the placeholder's
    # size *exactly*, and this is the table that says what that size is.
    ref = page.locator("details:has(#size-ref-list)").first
    if ref.count() == 0:
        raise RuntimeError("no required-image-sizes section on /images")
    ref.evaluate("el => el.open = true")
    page.wait_for_timeout(400)

    shoot(highlight=["#img-grid", "#size-ref-list"], full_page=True)


@recipe("assets/console/system-mobile-features.png", SURFACE)
def system_mobile_features(page: Page, shoot) -> None:
    """The Mobile features card: five switches and the Save button.

    The card has no id; it is reached through a control it contains, which survives
    the card being re-ordered on the page. 'Save features' has no id either and is
    matched by role -- and never clicked: it writes.
    """
    page.goto(url("/system"))
    session.settle(page)

    card = page.locator(".card:has(#feat-price_tags)").first
    if card.count() == 0:
        raise RuntimeError("no Mobile features card on /system")

    switches = card.locator("input[id^='feat-']")
    if switches.count() != 5:
        raise RuntimeError(
            f"expected 5 feature switches, found {switches.count()} — the docs name "
            "five, so the picture and the prose would disagree"
        )

    shoot(card, highlight=["input[id^='feat-']", "button:has-text('Save features')"])


@recipe("assets/console/mobile-devices-table-active.png", SURFACE)
def mobile_devices_table_active(page: Page, shoot) -> None:
    """Bound mobile devices, with a phone showing the green Active badge.

    The clock is un-frozen for this one shot. Every other recipe runs at
    config.FROZEN_CLOCK so the pixels are reproducible, but this table prints
    *relative* times ("5d ago") against the browser's clock -- and a phone that
    checked in five minutes ago is, from a clock pinned to 09:00 yesterday, seen in
    the future. The first take of this shot published `-27249s ago`, which reads as
    a broken console rather than a healthy one.

    The cost is that this shot cannot be byte-identical between runs -- the "ago"
    values move. That is already true of `tags-search-and-size-chips` (live fleet)
    and `mobile-devices-pairing-qr` (a freshly minted token); this is the third, and
    for the same underlying reason: the subject genuinely changes with time.
    """
    page.clock.set_system_time(datetime.now(timezone.utc))

    page.goto(url("/admin/mobile-binding"))
    session.settle(page)

    card = page.locator(".card:has(#devicesTbody)").first
    rows = page.locator("#devicesTbody tr")
    if rows.count() == 0:
        raise RuntimeError(
            "no bound mobile devices — the shot is of a freshly paired phone; "
            "pair one, then re-run with --only"
        )
    if "active" not in card.inner_text().lower():
        raise RuntimeError(
            "a device is bound but none reads Active — the Active badge is the "
            "subject of this shot"
        )

    shoot(card, highlight="#devicesTbody tr:first-child")


@recipe("assets/console/sales-orders-sync-filter.png", SURFACE)
def sales_orders_sync_filter(page: Page, shoot) -> None:
    """The sync-filter panel, expanded: status checkboxes and Max age.

    The filter is a native <details>, not one of the console's .card divs -- so the
    usual `.card:has(#control)` finds nothing, and the panel is *closed* on load. The
    docs ask for it expanded, which is the whole subject: it is where a reader learns
    the sync only pulls the statuses ticked here.
    """
    page.goto(url("/admin/sales-orders"))
    session.settle(page)

    details = page.locator("details:has(#order-filter-form)").first
    if details.count() == 0:
        raise RuntimeError("no sync-filter panel on /admin/sales-orders")

    details.evaluate("el => el.open = true")
    page.wait_for_timeout(400)

    shoot(details, highlight=["input[id^='status-']", "#filter-max-age"])


@recipe("assets/console/sales-orders-page.png", SURFACE)
def sales_orders_page(page: Page, shoot) -> None:
    """The orders table with rows in it, Sync now and the filter summary called out."""
    page.goto(url("/admin/sales-orders"))
    session.settle(page)

    rows = page.locator("tbody tr")
    if rows.count() == 0:
        raise RuntimeError(
            "no sales orders on this Commander — the shot is of a *populated* table; "
            "push some orders through the POS source, then re-run with --only"
        )

    shoot(highlight=["#sync-now-btn", "details:has(#order-filter-form) summary"], full_page=True)


@recipe("assets/console/willcall-bins-create.png", SURFACE)
def willcall_bins_create(page: Page, shoot) -> None:
    """The Staging bins card: bins listed, and the create form filled in beneath them.

    The form is filled but never submitted -- 'Add bin' is forbidden. It binds a real
    tag and flashes a sign onto a physical shelf, which is not something a screenshot
    run gets to do to a store.
    """
    page.goto(url("/admin/willcall"))
    session.settle(page)

    card = page.locator(".card:has(#bin-tag)").first
    if card.count() == 0:
        raise RuntimeError("no Staging bins card on /admin/willcall")
    if "(0)" in card.inner_text().split("\n")[0]:
        raise RuntimeError(
            "no staging bins exist — the shot wants at least one listed above the "
            "create form; create a bin, then re-run with --only"
        )

    # Fill the create form the way the lesson tells a reader to: a spare large tag,
    # a label staff will say out loud, a zone, and the idle design.
    tag = page.locator("#bin-tag")
    free = tag.locator("option").evaluate_all(
        "els => els.map(o => o.value).filter(v => v)"
    )
    if not free:
        raise RuntimeError("no large tags left to offer as a bin")
    tag.select_option(free[-1])
    page.locator("#bin-label").fill("Bin C2")
    page.locator("#bin-zone").fill("Front counter")

    tpl = page.locator("#bin-template")
    idle = tpl.locator("option").evaluate_all("els => els.map(o => o.value).filter(v => v)")
    if not idle:
        raise RuntimeError(
            "no will-call idle template on this Commander — the bin form cannot be "
            "completed without one, and the lesson depends on the idle/active pair"
        )
    tpl.select_option(idle[0])
    page.wait_for_timeout(300)

    shoot(card, highlight=["#bin-label", "#bin-template"])


@recipe("assets/console/willcall-assign.png", SURFACE)
def willcall_assign(page: Page, shoot) -> None:
    """The Assign card with an order picked and a bin chosen -- not submitted."""
    page.goto(url("/admin/willcall"))
    session.settle(page)

    card = page.locator(".card:has(#wc-so)").first
    if card.count() == 0:
        raise RuntimeError(
            "no Assign card on /admin/willcall — it only renders once a staging bin "
            "exists; create a bin first"
        )

    so = page.locator("#wc-so")
    orders = so.locator("option").evaluate_all("els => els.map(o => o.value).filter(v => v)")
    if not orders:
        raise RuntimeError(
            "no unassigned will-call orders — the shot is of one being picked; push a "
            "will-call SO (ship_via 'Will Call'), then re-run with --only"
        )
    so.select_option(orders[0])

    bin_sel = page.locator("#wc-tag")
    bins = bin_sel.locator("option").evaluate_all("els => els.map(o => o.value).filter(v => v)")
    if not bins:
        raise RuntimeError("no bin to assign to")
    bin_sel.select_option(bins[0])
    page.wait_for_timeout(300)

    shoot(card, highlight=["#wc-so", "#wc-tag"])


@recipe("assets/console/willcall-active-pickup.png", SURFACE)
def willcall_active_pickup(page: Page, shoot) -> None:
    """Active assignments: a live pickup code, and the Pickup button on its row.

    The Pickup button is the subject and must never be clicked -- it releases the
    assignment and blanks the sign. It is a bare form submit with no id, so the guard
    reaches it through the action it posts to.
    """
    page.goto(url("/admin/willcall"))
    session.settle(page)

    card = page.locator(".card:has(table)").first
    rows = card.locator("tbody tr")
    if rows.count() == 0:
        raise RuntimeError(
            "no active assignments — the shot is of a live pickup code; assign a "
            "will-call SO to a bin, then re-run with --only"
        )

    pickup = page.get_by_role("button", name="Pickup")
    if pickup.count() == 0:
        raise RuntimeError("an assignment exists but no Pickup button on its row")

    pickup.first.evaluate("el => el.setAttribute('data-shotwalker-pickup', '1')")
    shoot(card, highlight="[data-shotwalker-pickup]")


@recipe("assets/console/tag-detail-image-dropdown.png", SURFACE)
def tag_detail_image_dropdown(page: Page, shoot) -> None:
    """The bind form on a placeholder template, Image dropdown open.

    Two things have to line up and neither is the first thing you'd reach for. The
    Image dropdown only exists when the *selected template* carries an image
    placeholder, and it only offers anything when the library holds an image at that
    placeholder's exact resolution -- c06's whole rule. So the recipe finds a template
    that reveals #image-fields with a real option behind it, rather than picking one
    and hoping.

    Shot as the form, not the card: the only TAG58 tag on the bench is already bound,
    so the card is titled "Re-bind Tag", and a heading contradicting the lesson beside
    it is exactly the sort of thing that makes a doc image worse than no image.
    """
    _bind_form_for(page, want_image=True)

    select = page.locator("#bind-image")
    if select.locator("option").count() < 2:
        raise RuntimeError(
            "the Image dropdown offers only '— none —' — the library has no image at "
            "this placeholder's resolution, so the open dropdown would show nothing"
        )

    expand_in_place(page, "#bind-image")
    result = shoot(page.locator("#bind-form"), highlight="#bind-image")
    result.note = SELECT_SUBSTITUTE_NOTE


@recipe("assets/console/tag-detail-multi-bind.png", SURFACE)
def tag_detail_multi_bind(page: Page, shoot) -> None:
    """The bind form on a multi-product template: Title box and numbered slots.

    "Partly filled" is the point -- the lesson is that you fill the slots you have
    products for and leave the rest empty, so filling all five would illustrate the
    opposite. Two of five are typed in.

    The slot boxes are type-aheads. Typing into them is not a write; the form is only
    submitted by #bind-submit / #bind-push, both forbidden.
    """
    _bind_form_for(page, want_multi=True)

    header = page.locator("#multi-header")
    if header.count() == 0:
        raise RuntimeError("no Title box — is this really a multi-product template?")
    header.fill("Sale — 4 for $10")

    slots = page.locator("#multi-slots input")
    if slots.count() < 3:
        raise RuntimeError(f"expected several product slots, found {slots.count()}")

    # Empty every slot first. This tag is already bound, so the form loads with all
    # nine slots pre-filled from its current binding -- and a shot of a *full* grid
    # illustrates the opposite of what the form itself says two lines below it ("Fill
    # from the top; leave trailing slots empty to render blank cells"). Clearing is
    # client-side; the binding only changes if #bind-submit or #bind-push is clicked,
    # and both are forbidden.
    for i in range(slots.count()):
        slots.nth(i).fill("")
    page.wait_for_timeout(200)

    for i, sku in enumerate(("sosh-0010", "sosh-0011")):
        slots.nth(i).fill(sku)
        page.wait_for_timeout(250)

    # Blur the last slot to close its type-ahead. Escape alone does not: the suggestion
    # list stayed open and hung across the slot beneath it, which is how the first take
    # of this shot came out with a dropdown lying over row 3.
    page.evaluate("() => document.activeElement && document.activeElement.blur()")
    page.wait_for_timeout(400)
    if page.locator("#sku-suggest:visible, #multi-slots .suggest:visible").count():
        raise RuntimeError("a type-ahead is still open over the slots")

    shoot(page.locator("#bind-form"), highlight=["#multi-header", "#multi-slots"])


def _bind_form_for(page: Page, *, want_multi: bool = False, want_image: bool = False) -> None:
    """Open a tag's bind form on a template that reveals the fields we need.

    Neither the tag nor the template is hardcoded. Which templates exist, and which
    tag sizes they fit, is device state -- the multi-product templates on the bench
    are all TAG58, so a recipe that grabbed the first tag on /fleet would land on a
    TAG21 and never see a multi-product field. So: walk the tags, walk the templates
    each one offers, and stop at the first combination that actually reveals the
    section the shot is about.
    """
    page.goto(url("/fleet"))
    session.settle(page)

    rows = page.evaluate(
        """() => [...document.querySelectorAll('[data-addr]')].map(e => ({
             addr: e.getAttribute('data-addr'),
             size: ((e.textContent || '').match(/TAG\\d+/) || [''])[0],
           }))"""
    )
    if not rows:
        raise RuntimeError("no tags on /fleet")

    # Try one tag of each size before trying a second of any size. A template only
    # offers itself to a tag of the size it was drawn for, so the thing that decides
    # whether the multi-product fields can appear at all is the *size* -- and the
    # bench's only TAG58 sits somewhere in a fleet of 81. Walking the list in order
    # spent a minute on TAG21s that could never have shown a multi-product field.
    seen: set[str] = set()
    first_of_size, rest = [], []
    for r in rows:
        (first_of_size if r["size"] not in seen else rest).append(r["addr"])
        seen.add(r["size"])

    for addr in first_of_size + rest[:6]:
        page.goto(url(f"/tags/{addr}"))
        session.settle(page)

        select = page.locator("#bind-template")
        if select.count() == 0:
            continue

        for i in range(1, select.locator("option").count()):
            select.select_option(index=i)
            page.wait_for_timeout(450)

            if want_multi and not page.locator("#multi-fields").is_visible():
                continue
            if want_image:
                if not page.locator("#image-fields").is_visible():
                    continue
                if page.locator("#bind-image option").count() < 2:
                    continue
                # An image-*placeholder* template, not a multi-product one that
                # happens to have an image slot: c06 is teaching the single case.
                if page.locator("#multi-fields").is_visible():
                    continue
            return

    raise RuntimeError(
        "no tag/template pair on this Commander reveals the "
        f"{'multi-product' if want_multi else 'image'} fields — the shot needs a "
        "template of that kind, on a tag of the size it fits"
    )


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
    """The Defaults card, with one size row's Normal/Onsale pair called out.

    The docs ask for *one row's* pair, not every dropdown on the card. The lesson
    beside it is "set both sides of a pair and they link automatically"; outlining
    all eight selects turned that into "set all of these", which is a different
    instruction from the one the page is giving.

    The selects carry nothing that identifies their row -- no size, no purpose,
    only `data-current-default`, which is a template id and rots the moment the
    library changes. So the pair is taken positionally (the first PRICE TAGS row)
    and tagged, rather than matched on a value that will not hold.
    """
    page.goto(url("/templates"))
    session.settle(page)

    card = page.locator(".card:has(select[data-role='default-select'])").first
    if card.count() == 0:
        raise RuntimeError("no Defaults card on /templates")

    selects = page.locator("select[data-role='default-select']")
    if selects.count() < 2:
        raise RuntimeError(
            "Defaults card has fewer than two dropdowns — no Normal/Onsale pair to show"
        )
    for i in (0, 1):
        selects.nth(i).evaluate("el => el.setAttribute('data-shotwalker-pair','1')")

    shoot(card, highlight="[data-shotwalker-pair]")


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
    """One template card, purpose dropdown open, the ✓ button called out.

    Scoped to a single `.tpl-card`, not the library card that contains them: the
    library holds 19 templates, and the card-level shot came out 1,118px tall with
    every pill in the grid outlined -- a picture of the whole library, when the
    subject is one pill on one template.

    Clicking the pill swaps it for a `.purpose-edit` control (a <select> plus a ✓),
    and the ✓ renders `hidden` until the select's value actually *changes*. So the
    recipe has to pick a different purpose for the button the docs ask for to exist
    at all. That is client-side only -- nothing is written unless ✓ is clicked, and
    `.purpose-save` is on the forbidden list precisely so it never is.
    """
    page.goto(url("/templates"))
    session.settle(page)

    card = page.locator(".tpl-card:has([data-tpl-purpose])").first
    if card.count() == 0:
        raise RuntimeError("no template cards on /templates")

    card.locator("[data-tpl-purpose]").first.click()
    page.wait_for_timeout(300)

    select = card.locator("select.purpose-select").first
    if select.count() == 0:
        raise RuntimeError("purpose pill did not open into a select")

    # Choose something other than the current value, or the ✓ stays hidden.
    select.evaluate("el => el.setAttribute('data-shotwalker-purpose','1')")
    values = select.locator("option").evaluate_all(
        "els => els.map(o => o.value).filter(v => v)"
    )
    current = select.input_value()
    nxt = next((v for v in values if v != current), None)
    if nxt is None:
        raise RuntimeError("purpose select offers no alternative value")
    select.select_option(nxt)
    page.wait_for_timeout(250)

    save = card.locator(".purpose-save").first
    if save.count() == 0 or save.is_hidden():
        raise RuntimeError(
            "the ✓ Save button is still hidden after changing the purpose — "
            "the shot is *of* that button, so a card without it is the wrong image"
        )

    rect = open_select(page, "[data-shotwalker-purpose]")
    result = shoot(
        clip=clip_around(page, card.bounding_box(), rect),
        highlight=[".purpose-save", "#shotwalker-open-list"],
    )
    result.note = SELECT_SUBSTITUTE_NOTE


@recipe("assets/console/templates-defaults-pair.png", SURFACE)
def templates_defaults_pair(page: Page, shoot) -> None:
    """STILL HELD, and no longer for the reason it was.

    The black-on-black dropdown bug this was originally held on is fixed as of
    Commander 1.0.0-20260713-175438. The *second* blocker is not: the shot asks for
    "the Saved tick", which the page only renders after a default is saved -- a
    write. Shotwalker is reveal-only, so it cannot produce that state, and this
    recipe would otherwise capture the identical picture to
    `templates-defaults-card` (it did: the two PNGs came out byte-identical).

    Two honest ways out, neither of which is "click Save": re-spec the placeholder
    without the tick, or shoot it by hand. Captured into artifacts/ regardless, so
    the held image is there to look at.
    """
    page.goto(url("/templates"))
    session.settle(page)
    card = page.locator(".card:has(select[data-role='default-select'])").first
    if card.count() == 0:
        raise RuntimeError("no Defaults card on /templates")
    shoot(card, highlight="select[data-role='default-select']")
