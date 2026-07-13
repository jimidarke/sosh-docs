"""Browser context: authenticated, frozen in time, and unable to hang.

Three things here are load-bearing, and each was found by reading the Commander
source rather than by guessing:

* HTTP Basic. The console answers with `WWW-Authenticate: Basic realm="Guardian
  Monitor"`. Playwright's http_credentials handles it; there is no login form to
  drive and no session to establish.

* Dialogs. The Dashboard's quick actions call alert(), and template delete calls
  confirm(). Playwright blocks forever on an unhandled dialog, so the run would
  simply stop. The handler is installed before the first navigation.

* Clocks. The Dashboard reruns a relative-time tick at 1Hz, the QR page counts
  down at 1Hz, and four pages poll on intervals. Left alone, no two runs would
  ever produce the same pixels.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from . import config, guard

# Neuter the pollers. The pages fetch once on load (which we want -- the tables
# are drawn client-side from /api/*), then re-fetch on a timer (which we don't).
_KILL_TIMERS = """
(() => {
  const realSetInterval = window.setInterval;
  window.setInterval = (fn, ms, ...rest) => {
    // Let genuinely short timers through -- some UI code uses setInterval as a
    // one-shot poll for a value it's waiting on. Anything on a human-visible
    // cadence is a refresh loop, and that's what makes runs diverge.
    if (ms && ms >= 500) return 0;
    return realSetInterval(fn, ms, ...rest);
  };
})();
"""

_KILL_MOTION = """
*, *::before, *::after {
  animation: none !important;
  transition: none !important;
  caret-color: transparent !important;
}
"""


@contextmanager
def browser() -> Iterator[Browser]:
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True)
        try:
            yield b
        finally:
            b.close()


@contextmanager
def page_for(b: Browser, *, authenticated: bool = True) -> Iterator[Page]:
    """A page armed with auth, guards, frozen time, and no animation.

    `authenticated` exists because the Designer on :8090 has no auth at all --
    sending credentials there is harmless but pointless.
    """
    ctx: BrowserContext = b.new_context(
        viewport=config.VIEWPORT,
        device_scale_factor=config.DEVICE_SCALE_FACTOR,
        reduced_motion="reduce",
        color_scheme="light",  # the console has no dark theme; be explicit
        http_credentials=(
            {"username": config.username(), "password": config.password()}
            if authenticated
            else None
        ),
        ignore_https_errors=True,
    )
    page = ctx.new_page()

    # Order matters: guards and init scripts must be in place before any
    # navigation, or the first page load races them.
    page.on("dialog", lambda d: d.dismiss())
    page.add_init_script(_KILL_TIMERS)
    guard.install(page)
    page.clock.install(time=config.FROZEN_CLOCK)
    page.set_default_timeout(config.NAV_TIMEOUT_MS)

    try:
        yield page
    finally:
        ctx.close()


def settle(page: Page) -> None:
    """Wait for the page to stop moving.

    The console renders its tables client-side from /api/*, so 'loaded' is not
    'ready'. Fonts matter too: Font Awesome drives every icon button, and if it
    hasn't landed the buttons capture as empty boxes.
    """
    try:
        page.wait_for_load_state("networkidle", timeout=config.NAV_TIMEOUT_MS)
    except Exception:
        pass  # a stuck poll shouldn't fail the shot; the timeout is the budget
    try:
        page.evaluate("() => document.fonts.ready")
    except Exception:
        pass
    page.add_style_tag(content=_KILL_MOTION)
    page.wait_for_timeout(config.SETTLE_MS)
