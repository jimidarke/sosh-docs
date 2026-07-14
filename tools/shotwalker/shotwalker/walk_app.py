"""The staff handheld walk (adb).

The third surface, and the only one that is not a browser. See adb.py for the two
rules that shape everything here: nodes are found by text rather than by coordinate,
and **this surface is not reveal-only** -- the lessons it illustrates are writes.

Notes from the app that will save the next person an hour:

* `adb shell input text` does nothing. The tag-code sheet draws its own keypad in
  Compose rather than using an IME, so characters typed at the system level land
  nowhere and the field keeps its placeholder. Device.type_hex taps the keys.

* On that sheet, "Ready" is a *label* -- it means the 8 hex characters are complete.
  The button is "OK". Tapping the reassuring word does nothing at all.

* The scanner is disconnected on the bench, and it does not matter: every flow the
  docs describe as "scan the tag" has a type-it-in path behind the same field, which
  is what these recipes use. The screenshots are identical either way -- the app does
  not know how the code arrived.
"""

from __future__ import annotations

import re

from .adb import Device, Node
from .recipes import recipe

SURFACE = "app"

# Bench fixtures. Not hardcoded out of laziness -- these are *specific* states the
# shots need (a large tag; a free bin; an occupied one), and the walker cannot create
# them: making a bin is a console write, and there is exactly one TAG58 on the bench.
# If they rot, the recipes fail loudly and say so rather than shooting the wrong tag.
LARGE_TAG = "15100a4b"      # the only TAG58; the Multi-product button needs a large tag
FREE_BIN = "c5100563"       # Bin B1  — available
OCCUPIED_BIN = "c51004c9"   # Bin A3  — holds SO-24817


# Screens that sit *on top of* a tab. The bottom nav stays visible behind all of
# them, so "can I see the Tags button?" is not the question -- the multi-product
# editor shows the whole nav bar and is emphatically not the Tags screen. Asking only
# about the nav made home() return immediately from inside the editor, and the next
# recipe then hunted for a TAG field that was two screens away.
_SUBSCREEN_TEXT = ("Multi-product bind", "Enter tag code", "Find product")
_SUBSCREEN_DESC = ("Drag handle", "Close sheet")


def home(d: Device) -> None:
    """Back out to a tab root, whatever screen we inherited from the last recipe."""
    for _ in range(6):
        nodes = d.dump()
        texts = {n.text for n in nodes if n.text}
        descs = {n.desc for n in nodes if n.desc}

        on_subscreen = any(t in texts for t in _SUBSCREEN_TEXT) or any(
            x in descs for x in _SUBSCREEN_DESC
        )
        if not on_subscreen and {"Home", "Tags", "More"} <= texts:
            return
        d.back()

    raise RuntimeError("could not get back to a tab root")


def open_tab(d: Device, name: str) -> None:
    home(d)
    d.tap(d.need(name, exact=True), settle=1.5)


_HEX8 = re.compile(r"^[0-9a-f]{8}$", re.I)


def tag_field(d: Device) -> Node:
    """Whatever opens the tag-code keypad on the current screen.

    Three different things, depending where you are:

    * Tags tab, nothing loaded -- the placeholder "Scan a tag, or tap to type".
    * Tags tab, tag already loaded -- the field now reads `15100a4b`, and the
      placeholder is gone. The app keeps the last tag between visits, so on the second
      recipe of a run the first lookup finds nothing, which is a confusing way to learn
      that screens have memory.
    * Will-Call -- not a field at all, but a "Type tag code" button under "Scan a
      will-call sign tag".
    """
    for label in ("Scan a tag, or tap to type", "Type tag code"):
        hit = d.find(label)
        if hit is not None:
            return hit

    tag_label = d.find("TAG", exact=True)
    for n in d.dump():
        if _HEX8.match(n.text) and (tag_label is None or n.bounds[1] >= tag_label.bounds[1]):
            return n

    raise RuntimeError("nothing on this screen opens the tag-code keypad")


def product_field(d: Device) -> Node:
    """Whatever reopens the product search, empty or already holding a product.

    The same memory the TAG field has: once a product is chosen, the placeholder is
    replaced by the product's name, and looking for "Scan a UPC..." finds nothing.
    """
    placeholder = d.find("Scan a UPC, or tap to search")
    if placeholder is not None:
        return placeholder

    label = d.need("PRODUCT", exact=True)
    below = [
        n
        for n in d.dump()
        if n.hit_bounds is not None and 0 < n.bounds[1] - label.bounds[3] < 160
    ]
    if not below:
        raise RuntimeError("no PRODUCT field on this screen")
    return min(below, key=lambda n: n.bounds[1])


def enter_tag(d: Device, code: str) -> None:
    """Put a tag code into the TAG field.

    The docs say "scan the tag". The app accepts the same code from its own keypad and
    lands on exactly the same screen -- it does not know how the code arrived -- which
    is why these shots can be taken on a bench with no scanner attached.
    """
    d.tap(tag_field(d), settle=1.5)

    # Wait for the keypad, don't assume it. The sheet animates in, and typing into a
    # screen that has not finished arriving fails on the first character with "no 'c'
    # key" -- which reads like a broken keypad rather than a race, and cost an hour.
    d.wait_for("CLR", timeout=8)

    if d.find(code.upper(), exact=True) is None:
        d.tap(d.need("CLR", exact=True), settle=0.5)   # drop whatever was there

    d.type_hex(code)
    d.wait_for("Ready", timeout=6)   # the 8 characters are complete
    d.tap(d.need("OK", exact=True), settle=3.0)


# --------------------------------------------------------------------------
# Multi-product (Tags tab)
# --------------------------------------------------------------------------


@recipe("assets/app/multi-product-button.png", SURFACE)
def multi_product_button(d: Device, shoot) -> None:
    """The Tags tab with a large tag loaded, Multi-product called out.

    The button only exists for a large tag -- which is the point the lesson is making
    two lines above the screenshot ("Small tags hold one product only, and the button
    below won't appear for them"). Loading a TAG21 here would produce a picture that
    contradicts its own caption, so a missing button is a failure, not a shrug.
    """
    open_tab(d, "Tags")
    enter_tag(d, LARGE_TAG)

    if d.find("Multi-product") is None:
        raise RuntimeError(
            f"no Multi-product button after loading {LARGE_TAG} — is it still a large "
            "tag? The button is the subject of this shot"
        )
    shoot(highlight="Multi-product")


def row_buttons(d: Device, label: str) -> list[Node]:
    """The icon buttons on the row belonging to `label`, left to right.

    Every row in the editor (HEADER, SLOT 1, SLOT 2 ...) carries a keyboard icon and a
    clear icon, and *neither has a text or a content-desc* -- they are bare clickable
    boxes. So there is nothing to look them up by, and they have to be found the way a
    person finds them: the buttons on the same row as the label.

    (Their having no accessible label is an app bug in its own right. A screen reader
    cannot name either of them, and neither can anything else.)
    """
    row = d.need(label)
    y = (row.bounds[1] + row.bounds[3]) // 2
    hits = [
        n
        for n in d.dump()
        if n.clickable
        and n.bounds[0] >= 480
        and 0 < ((n.bounds[1] + n.bounds[3]) // 2) - y < 120
    ]
    return sorted(hits, key=lambda n: n.bounds[0])


def clear_row(d: Device, label: str) -> None:
    """Tap the clear (X) icon on a row -- the rightmost of its two buttons."""
    btns = row_buttons(d, label)
    if len(btns) < 2:
        raise RuntimeError(f"no clear button on the {label!r} row")
    d.tap(btns[-1], settle=0.8)


@recipe("assets/app/multi-product-editor.png", SURFACE)
def multi_product_editor(d: Device, shoot) -> None:
    """The editor: a layout chosen, three slots filled, the rest left empty.

    Three, not four, and not nine. The lesson's next line is "Slots you left empty show
    as blank cells, and that's usually exactly right" -- so a grid filled to the brim
    would illustrate the opposite of the sentence beneath it.

    The bench's TAG58 is already bound to Multi 9 with nine products, and the editor
    opens pre-filled from that binding. So the recipe drops it to the 5-slot layout and
    clears the tail, which is also the shape a reader will actually have: a layout
    picked, a few products scanned in, blanks below.
    """
    open_tab(d, "Tags")
    enter_tag(d, LARGE_TAG)
    d.tap(d.need("Multi-product"), settle=2.5)

    tpl = d.find("Multi 9 T58") or d.find("slots)")
    if tpl is None:
        raise RuntimeError("no TEMPLATE control in the multi-product editor")
    d.tap(tpl, settle=1.5)
    d.tap(d.need("Multi 5 T58"), settle=2.0)

    # The tag's own header is bench test data ("Test Title of a Big Multi Product 9").
    # Retype it: the shot sits under a step about what the HEADER field is for, and a
    # published image of somebody's leftover test string teaches nothing. One word --
    # the app's keypad has no space bar.
    clear_row(d, "HEADER (OPTIONAL)")
    d.tap(row_buttons(d, "HEADER (OPTIONAL)")[0], settle=1.5)
    d.type_keys("VALVES")
    d.tap(d.need("OK", exact=True), settle=1.5)

    for slot in ("SLOT 5", "SLOT 4"):
        d.scroll(-400)
        if d.find(slot, exact=True) and _slot_filled(d, slot):
            clear_row(d, slot)
    d.scroll(700)   # back to the top, where the template and first slots are

    filled = [s for s in ("SLOT 1", "SLOT 2", "SLOT 3", "SLOT 4", "SLOT 5") if _slot_filled(d, s)]
    if len(filled) != 3:
        raise RuntimeError(
            f"{len(filled)} slot(s) filled, expected 3 — the caption says three"
        )
    shoot()


def _slot_filled(d: Device, label: str) -> bool:
    """A slot is filled if a SKU line sits under its label."""
    row = d.find(label, exact=True)
    if row is None:
        return False
    y = (row.bounds[1] + row.bounds[3]) // 2
    return any(
        n.text.startswith("sosh-") and 0 < ((n.bounds[1] + n.bounds[3]) // 2) - y < 120
        for n in d.dump()
    )


@recipe("assets/app/multi-product-convert-confirm.png", SURFACE)
def multi_product_convert_confirm(d: Device, shoot) -> None:
    """The confirmation you get for putting a single product on a multi-product tag.

    Reached the way a person hits it by accident, which is what the lesson is about:
    load a tag that is already multi-product, then bind a single product to it the
    ordinary way. The app does not ask at the moment of choosing -- it shows an inline
    "Already bound to ... Bind will replace." note -- and only asks when you commit. So
    the dialog is behind PUSH, and PUSH is where the recipe has to go to find it.

    Then **Cancel**. Confirming would replace a nine-product binding with a single SKU
    on a real tag, which is precisely the accident the page is warning readers about.
    The dialog exists to be refused, and this recipe refuses it.
    """
    open_tab(d, "Tags")
    enter_tag(d, LARGE_TAG)

    d.tap(product_field(d), settle=2.0)
    d.type_keys("SOSH")               # the search needs 3+ characters
    d.wait_for("sosh-", timeout=10)

    hit = next(
        (n for n in d.dump() if n.text.startswith("sosh-") and n.hit_bounds is not None),
        None,
    )
    if hit is None:
        raise RuntimeError("product search returned nothing to pick")
    d.tap(hit, settle=2.5)

    push = next((n for n in d.dump() if n.text == "PUSH"), None)
    if push is None:
        raise RuntimeError("no PUSH button — cannot reach the confirmation")
    d.tap(push, settle=3.0)

    if d.find("Replace existing binding?") is None:
        raise RuntimeError(
            "no confirmation appeared — the shot is *of* that dialog, and without it "
            "PUSH may have replaced the binding outright"
        )
    shoot()

    cancel = next((n for n in d.dump() if n.text == "Cancel"), None)
    if cancel is None:
        raise RuntimeError("the dialog has no Cancel — refusing to leave it open")
    d.tap(cancel, settle=2.0)


# --------------------------------------------------------------------------
# Will-Call (More -> Will-Call)
# --------------------------------------------------------------------------


def open_willcall(d: Device) -> None:
    """Open Will-Call, and put it back to its "scan a sign" state.

    The screen remembers the last bin scanned -- across a back-out and a re-entry --
    and while it does, the "Type tag code" button is gone, replaced by the scanned bin
    and a Clear. So the second will-call recipe of a run found no way to open the
    keypad, fell through to a text node, and tapped a label. Clearing first makes each
    recipe independent of the one before it, which is the whole contract here.
    """
    open_tab(d, "More")
    if d.find("Will-Call") is None:
        raise RuntimeError(
            "no Will-Call in the More menu — the feature is off for this store "
            "(System -> Mobile features), and all three will-call shots need it on"
        )
    d.tap(d.need("Will-Call"), settle=2.0)

    clear = d.find("Clear", exact=True)
    if clear is not None:
        d.tap(clear, settle=1.5)


@recipe("assets/app/willcall-scan-sign.png", SURFACE)
def willcall_scan_sign(d: Device, shoot) -> None:
    """A free bin tag just scanned: the app says the sign is available."""
    open_willcall(d)
    enter_tag(d, FREE_BIN)

    if d.find("Assign") is None:
        raise RuntimeError(
            "no assignable order after scanning the bin — the shot is of a free sign "
            "ready to take an order; push a will-call SO and leave a bin empty"
        )
    shoot()


def _pickup_codes(d: Device) -> dict[str, Node]:
    """Every pickup code currently on the board, keyed by code."""
    return {
        n.text.split()[-1]: n
        for n in d.dump()
        if n.text.startswith("Pickup ") and len(n.text.split()) > 1
    }


@recipe("assets/app/willcall-assign-order.png", SURFACE)
def willcall_assign_order(d: Device, shoot) -> None:
    """The order assigned, its pickup code on the phone.

    This one genuinely writes -- it puts a customer's name on a physical sign, which is
    the lesson, and cannot be faked. It then *releases* what it assigned, so the bench
    is left as it was found: otherwise the first run eats the only free bin and every
    run after it fails for want of one.

    Two traps here, both of which shipped a wrong image before they were caught:

    * `find("Assign")` matches the *heading* "Un-assign-ed will-call orders (2)". It is
      a substring, and the heading is not a button, so the tap did nothing at all. The
      button has to be matched exactly, and it has to be clickable.

    * With nothing assigned, the check "is a pickup code on screen?" still passed --
      because SO-24817 was already on Bin A3 with a code of its own from an earlier
      run. The shot came out highlighting *somebody else's* assignment while both
      orders sat plainly unassigned above it. So the test is not "a code exists", it is
      "a code exists that was not there a moment ago".
    """
    open_willcall(d)
    enter_tag(d, FREE_BIN)

    before = _pickup_codes(d)

    button = next(
        (
            n
            for n in d.dump()
            if n.text == "Assign" and (n.clickable or n.hit_bounds is not None)
        ),
        None,
    )
    if button is None:
        raise RuntimeError(
            "no Assign button — the shot needs an unassigned will-call order and a "
            "free bin; push a will-call SO and leave a bin empty"
        )
    d.tap(button, settle=3.5)

    after = _pickup_codes(d)
    fresh = set(after) - set(before)
    if not fresh:
        raise RuntimeError(
            f"nothing was assigned — the board still shows the same pickup code(s) "
            f"{sorted(before) or '[]'}. The shot is *of* a new assignment."
        )

    code = after[fresh.pop()]
    shoot(highlight=code)

    # Put the bench back: release the row we just created, not one that was already
    # there. Matched by the order number so a pre-existing assignment is never touched.
    row_y = code.bounds[1]
    release = next(
        (
            n
            for n in d.dump()
            if n.text == "Release" and abs(n.box[1] - row_y) < 140
        ),
        None,
    )
    if release is not None:
        d.tap(release, settle=2.5)


@recipe("assets/app/willcall-release.png", SURFACE)
def willcall_release(d: Device, shoot) -> None:
    """An occupied sign scanned, Release called out."""
    open_willcall(d)
    enter_tag(d, OCCUPIED_BIN)

    release = d.find("Release")
    if release is None:
        raise RuntimeError(
            "no Release button — the shot needs an *occupied* sign; assign an order "
            "to a bin first"
        )
    shoot(highlight=release)
