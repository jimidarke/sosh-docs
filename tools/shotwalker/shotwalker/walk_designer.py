"""The Template Designer walk (:8090).

A separate application from the console -- nginx-served, no auth, vanilla JS on
a Fabric.js canvas -- and the one the docs' largest section actually documents.

Everything here is reveal-only in the strongest sense: objects are drawn onto an
unsaved canvas, which is pure client-side state. Nothing is written server-side,
and the guard blocks #btn-save and #btn-render-push regardless.

Two facts from the source shape these recipes:
  * CanvasManager.addObject() calls setActiveObject(), so creating an object
    also selects it -- one click both draws the shape and populates the
    properties panel.
  * The panel titles its sections in plain text ('Text', 'Shape', 'Barcode',
    'QR Code', 'Data Binding', 'Conditional Rules'), with no ids, so sections
    are located by text.
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from . import config, session
from .recipes import recipe
from .selects import SELECT_SUBSTITUTE_NOTE, open_select  # noqa: F401  (re-exported)

SURFACE = "designer"


def open_designer(page: Page) -> None:
    page.goto(config.designer_url())
    session.settle(page)
    # Below ~1280px the Designer replaces the entire page with a "Desktop Only"
    # overlay. At 1440x900 it stays hidden; assert that rather than discover it
    # by finding 18 screenshots of a warning banner.
    warn = page.locator("#mobile-warning")
    if warn.count() and warn.is_visible():
        raise RuntimeError(
            "Designer is showing its 'Desktop Only' overlay — viewport too narrow"
        )


def panel(page: Page) -> Locator:
    return page.locator("#property-panel")


def clear_toasts(page: Page) -> None:
    """Drop any toast notification before the shutter.

    The Designer toasts on every object added ('Image placeholder added — bind an
    image on ...'). Normally it fades, but session._KILL_MOTION sets
    `transition: none` on everything to keep runs deterministic -- so the toast that
    would have faded instead sits there forever, and it is positioned over the
    properties panel, which is the subject of most of these shots. It came out
    sliced in half across the bottom of the panel.

    Determinism and the toast's exit animation are the same mechanism, so the toast
    has to be removed rather than waited out.
    """
    page.evaluate("() => document.querySelectorAll('.toast').forEach(t => t.remove())")


def add(page: Page, button_id: str) -> None:
    """Click a tool button; the new object lands selected."""
    page.click(f"#{button_id}")
    page.wait_for_timeout(400)
    clear_toasts(page)


def section(page: Page, title: str) -> Locator:
    """A properties-panel section (`.prop-section`) by its header text.

    Headers render uppercase ('DATA BINDING'), but Playwright's has-text matches
    case-insensitively, so the human-readable name works.
    """
    return panel(page).locator(
        f'.prop-section:has(.prop-section-header:has-text("{title}"))'
    )


def expand_section(page: Page, title: str) -> Locator:
    """Open a collapsed properties section and return it.

    Data Binding and Conditional Rules both render default-collapsed -- shooting
    the panel without opening them captures a section header and nothing else,
    which is what the first Data Binding attempt did.
    """
    sec = section(page, title).first
    if sec.count() == 0:
        raise RuntimeError(f"no {title!r} section — is the object data-bindable?")

    body = sec.locator(".prop-section-body")
    if body.count() and not body.first.is_visible():
        sec.locator(".prop-section-header").first.click()
        page.wait_for_timeout(350)

    sec.scroll_into_view_if_needed()
    page.wait_for_timeout(200)
    return sec


def wait_for_rules_panel(page: Page) -> None:
    """The Conditional Rules section only exists once RulesPanel has loaded.

    app.js injects src/rules-panel.js with a dynamically-appended <script>, and
    property-panel.js renders the section only `if (typeof RulesPanel !==
    'undefined')`. Select an object before that script lands and the section is
    silently absent -- which is exactly how the first run failed.
    """
    page.wait_for_function("() => typeof RulesPanel !== 'undefined'", timeout=15_000)


def select_all_on_canvas(page: Page) -> int:
    """Rubber-band drag across the canvas to build a Fabric multi-selection.

    Align and distribute only appear on a selection of 2+ objects: app.js gates
    #align-section on the `selection:created` event's count. There's no keyboard
    select-all, and CanvasManager isn't exposed on window, so the only way in is
    the way a user does it -- drag a marquee over the objects from empty canvas.
    """
    box = page.locator("#design-canvas").bounding_box()
    if not box:
        raise RuntimeError("no #design-canvas to select on")

    page.mouse.move(box["x"] + 2, box["y"] + 2)
    page.mouse.down()
    page.mouse.move(
        box["x"] + box["width"] - 2, box["y"] + box["height"] - 2, steps=12
    )
    page.mouse.up()
    page.wait_for_timeout(500)

    status = page.locator("#status-selected")
    text = status.inner_text() if status.count() else ""
    return int(text.split()[0]) if text and text.split()[0].isdigit() else 0


def enable_multi_product(page: Page, slots: int = 3) -> None:
    """Flip Template Parameters to Multi-Product and set the slot count.

    The toggle is a pair of unlabelled <button>s ('Single Product' /
    'Multi-Product') with inline styles and no ids, so it is reached by role and
    name. Turning it on is what makes the Slots field -- and the per-slot Data
    Binding dropdown -- exist at all; without it, Data Binding offers only the
    three group-level fields and there is no Product 1/2/3 to bind to.

    The Slots input is likewise id-less: it is the only number input in the
    Multi-Product section. `change` is dispatched explicitly because filling an
    input does not fire the event the panel listens on.
    """
    toggle = panel(page).get_by_role("button", name="Multi-Product", exact=True)
    if toggle.count() == 0:
        raise RuntimeError("no Multi-Product toggle in the Template Parameters panel")
    toggle.first.click()
    page.wait_for_timeout(400)

    box = multi_product_section(page).locator("input[type=number]").first
    if box.count() == 0:
        raise RuntimeError("Multi-Product is on but there is no Slots field")
    box.fill(str(slots))
    box.dispatch_event("change")
    page.wait_for_timeout(500)


def multi_product_section(page: Page) -> Locator:
    return section(page, "Multi-Product").first


def position_inputs(page: Page) -> Locator:
    """Left, Top, Width, Height, Angle — in that order, none of them with an id."""
    return section(page, "Position").first.locator("input[type=number]")


def place(page: Page, left: int, top: int) -> None:
    """Move the selected object. Canvas-only; nothing is written."""
    boxes = position_inputs(page)
    for i, v in ((0, left), (1, top)):
        boxes.nth(i).fill(str(v))
        boxes.nth(i).dispatch_event("change")
    page.wait_for_timeout(250)


def bind_slot(page: Page, slot: str, field: str) -> None:
    """Bind the selected object to `field` on multi-product slot `slot`.

    Data Binding renders two dropdowns once Multi-Product is on: the first picks
    the slot ('Group / Title', 'Product 1', 'Product 2', ...), and the second is
    repopulated from it -- pick a slot and the field list becomes the product
    fields (product_name_line1, price, sku, ...). Setting the field before the
    slot silently binds it to the group instead.

    Then **Apply Binding**, which is the step that actually writes the binding onto
    the object. Choosing the dropdowns alone does nothing durable: deselect and
    re-select and the panel reads back 'Group / Title', because nothing was ever
    applied. (That behaviour looked like a binding-persistence bug in sosh until the
    captured screenshot showed the Apply button sitting right there, unclicked.)

    Apply is canvas-only -- unsaved client-side object state, exactly like drawing a
    rectangle. Nothing reaches the Commander; #btn-save and #btn-render-push are the
    controls that would, and both are forbidden.
    """
    sec = expand_section(page, "Data Binding")
    selects = sec.locator("select")
    if selects.count() < 2:
        raise RuntimeError("Data Binding has no slot dropdown — is Multi-Product on?")

    selects.nth(0).select_option(label=slot)
    page.wait_for_timeout(400)

    fields = selects.nth(1).locator("option").all_inner_texts()
    if field not in fields:
        raise RuntimeError(f"{field!r} not offered for slot {slot!r}; got {fields[:6]}")
    selects.nth(1).select_option(label=field)
    page.wait_for_timeout(300)

    apply_btn = sec.get_by_role("button", name="Apply Binding")
    if apply_btn.count() == 0:
        raise RuntimeError("no 'Apply Binding' button — the binding would not stick")
    apply_btn.first.click()
    page.wait_for_timeout(400)


def select_product(page: Page, term: str = "sos") -> None:
    """Pick a product in the left panel, which is what enables Preview.

    Two steps are easy to miss, and both were: a store must be chosen before the
    type-ahead returns anything, and the search needs 3+ characters. Skip either
    and the Preview button stays disabled -- so a shot of "the enabled Preview
    button" quietly captures a disabled one.
    """
    store = page.locator("#product-store-select")
    if store.count() and store.is_visible():
        options = store.locator("option")
        if options.count() > 1:
            store.select_option(index=1)
            page.wait_for_timeout(800)

    search = page.locator("#product-search")
    if search.count() == 0:
        raise RuntimeError("no #product-search in the Designer's product panel")

    search.click()
    search.fill("")
    search.type(term, delay=100)

    dropdown = page.locator("#product-search-dropdown")
    dropdown.wait_for(state="visible", timeout=10_000)
    dropdown.locator("> *").first.click()
    page.wait_for_timeout(800)

    if page.locator("#btn-preview-render").is_disabled():
        raise RuntimeError("selected a product but Preview is still disabled")


# --------------------------------------------------------------------------
# Workspace and template management
# --------------------------------------------------------------------------


@recipe("assets/designer/workspace-overview.png", SURFACE)
def workspace_overview(page: Page, shoot) -> None:
    """The whole window on a blank canvas — the docs label the five areas."""
    open_designer(page)
    shoot(full_page=False)


@recipe("assets/designer/tag-size-dropdown.png", SURFACE)
def tag_size_dropdown(page: Page, shoot) -> None:
    """The Tag size control, showing all three sizes.

    Clipped rather than shot as an element: the expanded list hangs below the
    toolbar's own box, so an element screenshot of the toolbar guillotines it --
    the first attempt captured a 96px strip with TAG58 sliced off.
    """
    open_designer(page)
    rect = open_select(page, "#profile-select")

    result = shoot(
        clip={
            "x": 0,
            "y": 0,
            "width": min(rect["right"] + 80, config.VIEWPORT["width"]),
            "height": min(rect["bottom"] + 20, config.VIEWPORT["height"]),
        },
        highlight=["#profile-select", "#shotwalker-open-list"],
    )
    result.note = SELECT_SUBSTITUTE_NOTE


@recipe("assets/designer/template-parameters-name.png", SURFACE)
def template_parameters_name(page: Page, shoot) -> None:
    open_designer(page)
    name = page.locator("#property-panel input").first
    if name.count():
        name.fill("Shelf label — 3.5in")
    shoot(panel(page), highlight="#property-panel input")


def _tag(locator: Locator, name: str) -> str:
    """Mark one element so `highlight=` can name it in plain CSS.

    The panel's sections have no ids, and `highlight` takes CSS selectors that get
    passed to querySelectorAll -- so ':has-text' and nth-of-a-Locator are not
    available there. Tagging the element we already found is how the existing
    Data Binding recipe solves the same problem.
    """
    locator.evaluate(f"el => el.setAttribute('data-shotwalker-{name}', '1')")
    return f"[data-shotwalker-{name}]"


@recipe("assets/designer/template-params-multi.png", SURFACE)
def template_params_multi(page: Page, shoot) -> None:
    """Template Parameters with Multi-Product on and the slot count set."""
    open_designer(page)
    enable_multi_product(page, slots=3)

    sec = multi_product_section(page)
    if sec.count() == 0:
        raise RuntimeError("no Multi-Product section in the panel")

    shoot(panel(page), highlight=_tag(sec, "multi"))


@recipe("assets/designer/multi-product-rows.png", SURFACE)
def multi_product_rows(page: Page, shoot) -> None:
    """Three product rows on the canvas, the second selected on its Product 2 binding.

    A "product row" is not a designer primitive -- it is an ordinary text object
    bound to a slot. So the recipe builds what the lesson describes: three text
    objects, stacked, each bound to a different slot, then leaves the middle one
    selected so the panel shows *its* binding, which is the whole point of the
    shot ("one row selected showing its Product 2 binding").

    Shot as the viewport, not an element: the subject spans the canvas *and* the
    properties panel, which are opposite ends of the window.
    """
    open_designer(page)
    enable_multi_product(page, slots=3)

    for i in range(1, 4):
        add(page, "btn-text")
        place(page, left=20, top=10 + (i - 1) * 40)
        bind_slot(page, f"Product {i}", "product_name_line1")

    # Re-select the middle row: the last row added is the one left selected, and the
    # docs ask for the Product 2 row. The layer panel lists topmost-first (reverse
    # insertion order), which makes "row 2 is .layer-item[1]" true today and false the
    # moment layering changes -- so don't trust the order. Click each row and ask the
    # panel what it is bound to. The check *is* the selection.
    #
    # Ask the *label*, not the dropdowns. Applying a binding resets the two selects
    # back to 'Group / Title' -- they are the input control, not the read-out -- and
    # the applied binding is what the section then prints: `product_2_...`. Asserting
    # on the selects instead reads a control that has done its job and gone home, which
    # is what made this recipe look, twice, like a binding-persistence bug in sosh.
    rows = page.locator("#layer-panel .layer-item")
    if rows.count() != 3:
        raise RuntimeError(f"expected 3 product rows, found {rows.count()}")

    for i in range(rows.count()):
        rows.nth(i).click()
        page.wait_for_timeout(400)
        sec = expand_section(page, "Data Binding")
        if "product_2_" in sec.inner_text():
            break
    else:
        raise RuntimeError(
            "no row shows a product_2_* binding — the shot is *of* the Product 2 row, "
            "so any other row would be the wrong image"
        )

    shoot(highlight=_tag(sec, "binding"))


@recipe("assets/designer/image-placeholder-required-resolution.png", SURFACE)
def image_placeholder_required_resolution(page: Page, shoot) -> None:
    """The Image Placeholder's Required-resolution read-out.

    #btn-image-placeholder drops the box onto the canvas already selected (see
    the CanvasManager.addObject note at the top), so the panel is populated in one
    click. The read-out is derived from the box's size -- resize it and the
    required resolution changes -- which is exactly the rule c06 is teaching.
    """
    open_designer(page)
    page.click("#btn-image-placeholder")
    page.wait_for_timeout(700)
    clear_toasts(page)

    sec = section(page, "Image Placeholder").first
    if sec.count() == 0:
        raise RuntimeError(
            "no 'Image Placeholder' section — did the placeholder land unselected?"
        )
    if "resolution" not in sec.inner_text().lower():
        raise RuntimeError("Image Placeholder section has no Required-resolution read-out")

    shoot(panel(page), highlight=_tag(sec, "reqres"))


@recipe("assets/designer/template-browser.png", SURFACE)
def template_browser(page: Page, shoot) -> None:
    open_designer(page)
    page.click("#btn-load")
    page.wait_for_selector("#template-modal", state="visible")
    session.settle(page)
    shoot(page.locator("#template-modal"), highlight="#modal-search")


# --------------------------------------------------------------------------
# Text
# --------------------------------------------------------------------------


@recipe("assets/designer/text-properties-panel.png", SURFACE)
def text_properties_panel(page: Page, shoot) -> None:
    open_designer(page)
    add(page, "btn-text")
    shoot(panel(page))


@recipe("assets/designer/paragraph-wrap-properties.png", SURFACE)
def paragraph_wrap_properties(page: Page, shoot) -> None:
    open_designer(page)
    add(page, "btn-paragraph")
    shoot(panel(page))


@recipe("assets/designer/data-binding-field-dropdown.png", SURFACE)
def data_binding_field_dropdown(page: Page, shoot) -> None:
    """The Data Binding section with its Field list open.

    Shot as a section, not the whole panel: the properties column runs 1,560px
    tall, and Data Binding sits collapsed at the very bottom of it.
    """
    open_designer(page)
    add(page, "btn-text")

    sec = expand_section(page, "Data Binding")

    field = sec.locator(".prop-section-body select").last
    if field.count() == 0:
        raise RuntimeError("no field dropdown inside the Data Binding section")

    field.evaluate("el => el.setAttribute('data-shotwalker-field','1')")
    rect = open_select(page, "[data-shotwalker-field]")

    # Clip to cover the section *and* the open list. An element shot of the
    # section alone guillotines the list where the section's box ends.
    box = sec.bounding_box() or {"x": 0, "y": 0, "width": 0, "height": 0}
    left = min(box["x"], rect["left"])
    top = min(box["y"], rect["top"])
    result = shoot(
        clip={
            "x": max(left - 4, 0),
            "y": max(top - 4, 0),
            "width": min(
                max(box["x"] + box["width"], rect["right"]) - left + 8,
                config.VIEWPORT["width"] - left,
            ),
            "height": min(
                max(box["y"] + box["height"], rect["bottom"]) - top + 8,
                config.VIEWPORT["height"] - top,
            ),
        },
        highlight="[data-shotwalker-field]",
    )
    result.note = SELECT_SUBSTITUTE_NOTE


@recipe("assets/designer/price-prefix-superscript.png", SURFACE)
def price_prefix_superscript(page: Page, shoot) -> None:
    open_designer(page)
    add(page, "btn-text")
    shoot(panel(page))


# --------------------------------------------------------------------------
# Shapes, barcodes, QR, icons
# --------------------------------------------------------------------------


@recipe("assets/designer/shape-properties-panel.png", SURFACE)
def shape_properties_panel(page: Page, shoot) -> None:
    open_designer(page)
    add(page, "btn-rect")
    shoot(panel(page))


@recipe("assets/designer/wbr-colour-preview.png", SURFACE)
def wbr_colour_preview(page: Page, shoot) -> None:
    """The three-colour (white/black/red) preview, toggled on."""
    open_designer(page)
    add(page, "btn-rect")
    add(page, "btn-text")
    page.click("#btn-wbr-preview")
    page.wait_for_timeout(600)
    shoot(page.locator("#canvas-area"), highlight="#btn-wbr-preview")


@recipe("assets/designer/barcode-properties.png", SURFACE)
def barcode_properties(page: Page, shoot) -> None:
    open_designer(page)
    add(page, "btn-barcode")
    shoot(panel(page))


@recipe("assets/designer/qr-properties.png", SURFACE)
def qr_properties(page: Page, shoot) -> None:
    open_designer(page)
    add(page, "btn-qrcode")
    shoot(panel(page))


@recipe("assets/designer/icon-picker.png", SURFACE)
def icon_picker(page: Page, shoot) -> None:
    open_designer(page)
    page.click("#btn-icon")
    page.wait_for_selector("#icon-modal", state="visible")
    session.settle(page)
    shoot(page.locator("#icon-modal"), highlight="#icon-search")


@recipe("assets/designer/conditional-rule-sale-burst.png", SURFACE)
def conditional_rule_sale_burst(page: Page, shoot) -> None:
    """Conditional Rules, expanded, on an icon.

    It must be an icon, and not just because the docs say "burst icon": Data
    Binding and Conditional Rules only render for data-bindable object types. A
    rectangle gets IDENTITY / POSITION / APPEARANCE / SHAPE and nothing else, so
    the section it's meant to show simply isn't there.

    The section also renders default-collapsed, and only exists once RulesPanel
    has lazily loaded -- hence the wait before the object is added.
    """
    open_designer(page)
    wait_for_rules_panel(page)

    page.click("#btn-icon")
    page.wait_for_selector("#icon-modal", state="visible")
    page.wait_for_timeout(400)
    page.locator("#icon-grid > *").first.click()
    page.wait_for_timeout(800)

    sec = expand_section(page, "Conditional Rules")

    add_rule = sec.get_by_text("Add Rule", exact=False).first
    if add_rule.count() == 0:
        raise RuntimeError("no '+ Add Rule' button in the Conditional Rules section")
    add_rule.click()
    page.wait_for_timeout(600)

    # Fill the rule in. The docs describe it reading "IF sale price exists THEN
    # Show" -- an empty rule row would leave the image contradicting the prose
    # next to it.
    selects = sec.locator("select")
    if selects.count() >= 2:
        _select_matching(selects.nth(0), ["sale", "price"])
        _select_matching(selects.nth(1), ["exist", "not empty", "is set"])
        page.wait_for_timeout(400)

    shoot(sec)


def _select_matching(select: Locator, keywords: list[str]) -> None:
    """Choose an option by keyword, honouring keyword order as priority.

    The order matters: scanning options for "any keyword" picked `regular_price`
    for ["sale", "price"], because regular_price came first in the list. The
    docs specifically describe a *sale* price rule.
    """
    labels = [t.lower() for t in select.locator("option").all_inner_texts()]
    for keyword in keywords:
        for i, label in enumerate(labels):
            if keyword in label:
                select.select_option(index=i)
                return


# --------------------------------------------------------------------------
# Layout, layers, products
# --------------------------------------------------------------------------


@recipe("assets/designer/align-section.png", SURFACE)
def align_section(page: Page, shoot) -> None:
    """Align and distribute. Needs 3 objects: distribute is meaningless on 2."""
    open_designer(page)
    add(page, "btn-rect")
    add(page, "btn-circle")
    add(page, "btn-text")

    count = select_all_on_canvas(page)
    if count < 2:
        raise RuntimeError(
            f"marquee selected {count} object(s); align needs 2+ to appear"
        )

    target = page.locator("#align-section")
    target.wait_for(state="visible", timeout=5_000)
    shoot(target)


@recipe("assets/designer/layers-panel.png", SURFACE)
def layers_panel(page: Page, shoot) -> None:
    open_designer(page)
    add(page, "btn-rect")
    add(page, "btn-text")
    add(page, "btn-barcode")
    shoot(page.locator("#layer-panel"))


@recipe("assets/designer/product-panel-preview-enabled.png", SURFACE)
def product_panel_preview_enabled(page: Page, shoot) -> None:
    """The Product panel with a product chosen -- and Preview genuinely enabled.

    select_product() asserts the button actually came alive. Without that check
    this shot "passes" while showing a greyed-out button, which is the exact
    opposite of what the docs asked for.
    """
    open_designer(page)
    add(page, "btn-text")
    select_product(page)
    shoot(page.locator("#product-panel"), highlight="#btn-preview-render")


@recipe("assets/designer/render-preview-popup.png", SURFACE)
def render_preview_popup(page: Page, shoot) -> None:
    """The rendered-label popup, showing a real product's name and price.

    Preview is disabled until a product is bound to the canvas, so the product
    must be selected first -- and this is the one recipe that needs a POST: the
    preview round-trips the canvas through the renderer. guard.ALLOWED_WRITE_PATHS
    permits that endpoint specifically, because it computes an image and writes
    nothing.
    """
    open_designer(page)
    add(page, "btn-text")
    add(page, "btn-barcode")
    select_product(page)

    page.click("#btn-preview-render")
    page.wait_for_selector("#preview-modal", state="visible", timeout=30_000)
    session.settle(page)

    # The modal opens whether or not the render succeeded. Assert an image
    # actually came back, so a failed render can't pass as a screenshot of a
    # blank popup -- which is precisely what happened when the guard was
    # silently aborting /render/direct.
    rendered = page.evaluate(
        """() => {
            const m = document.getElementById('preview-modal');
            if (!m) return false;
            return [...m.querySelectorAll('img, canvas')]
              .some(e => (e.naturalWidth || e.width || 0) > 1);
        }"""
    )
    if not rendered:
        raise RuntimeError("preview modal opened but no rendered image came back")

    shoot(page.locator("#preview-modal"))
