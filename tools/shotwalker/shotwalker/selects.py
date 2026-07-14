"""Photographing an open <select>.

A headless browser cannot photograph an open native <select>: the option list is
painted by browser chrome, outside the page's render tree, so it is absent from
every screenshot -- this is true of Playwright, Puppeteer and Selenium alike.
Setting `size` re-renders the same <option> elements as an inline listbox, which
*is* in the page and does show the real options (including <optgroup> headings).
It reads as a listbox rather than a floating popup. Recipes that rely on this flag
it, and the report says so, so nobody mistakes it for a pixel-accurate capture of
the real control.

Expanding the select *in place* fights the layout and loses: the Designer toolbar
is a centring flexbox, so a taller control grows in both directions and the first
option ends up above the top of the page (measured: top went to -13.5px).
align-self didn't override it.

So don't touch the real control. Clone it, expand the clone, and hang it directly
beneath the original -- which is where a native popup would appear anyway, so the
result reads like an open dropdown instead of a mangled toolbar. The real control
stays pixel-correct underneath it.

Lives in its own module because both walks need it: the Designer's tag-size and
field dropdowns, and the console's template purpose pill.
"""

from __future__ import annotations

from playwright.sync_api import Page

_OPEN_SELECT = """
(el) => {
  document.getElementById('shotwalker-open-list')?.remove();
  const r = el.getBoundingClientRect();
  const clone = el.cloneNode(true);
  clone.id = 'shotwalker-open-list';
  clone.setAttribute('size', String(Math.min(Math.max(el.options.length, 2), 12)));
  clone.selectedIndex = el.selectedIndex;
  Object.assign(clone.style, {
    position: 'fixed',
    left: r.left + 'px',
    top: (r.bottom + 2) + 'px',
    width: r.width + 'px',
    height: 'auto',
    maxHeight: 'none',
    zIndex: '99999',
  });
  document.body.appendChild(clone);
  const c = clone.getBoundingClientRect();
  return {left: c.left, top: c.top, right: c.right, bottom: c.bottom};
}
"""

SELECT_SUBSTITUTE_NOTE = (
    "dropdown rendered as an inline listbox — headless browsers cannot capture "
    "an open native <select> popup"
)


def open_select(page: Page, selector: str) -> dict:
    """Render `selector`'s options as an open list. Returns the list's rect."""
    rect = page.eval_on_selector(selector, _OPEN_SELECT)
    page.wait_for_timeout(200)
    return rect


def expand_in_place(page: Page, selector: str) -> None:
    """Expand a <select> into an inline listbox *inside* its own container.

    The clone-and-hang trick above exists to survive the Designer's centring flexbox
    toolbar. On an ordinary block form -- the console's tag bind form -- it is the
    wrong tool: the clone is `position: fixed` (viewport coordinates) while
    `page.screenshot(clip=...)` takes page coordinates, and on a form long enough to
    scroll the two do not agree. The first take of tag-detail-image-dropdown came out
    as a 60px sliver of the top of the form.

    A block form has room to simply grow, so grow it. The options end up in the
    element's own box, and an ordinary element screenshot captures them.
    """
    page.eval_on_selector(
        selector,
        """(el) => {
            el.setAttribute('size', String(Math.min(Math.max(el.options.length, 2), 12)));
            el.scrollIntoView({block: 'center'});
        }""",
    )
    page.wait_for_timeout(250)


def clip_around(page, box: dict | None, rect: dict, pad: int = 4) -> dict:
    """A clip rectangle covering an element's box *and* its open list.

    An element screenshot guillotines the list where the element's own box ends,
    which is how the first tag-size shot came out as a 96px strip with the last
    option sliced off.
    """
    from . import config

    box = box or {"x": rect["left"], "y": rect["top"], "width": 0, "height": 0}
    left = min(box["x"], rect["left"])
    top = min(box["y"], rect["top"])
    right = max(box["x"] + box["width"], rect["right"])
    bottom = max(box["y"] + box["height"], rect["bottom"])

    left = max(left - pad, 0)
    top = max(top - pad, 0)
    return {
        "x": left,
        "y": top,
        "width": min(right - left + 2 * pad, config.VIEWPORT["width"] - left),
        "height": min(bottom - top + 2 * pad, config.VIEWPORT["height"] - top),
    }
