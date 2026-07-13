"""The test half of the walk.

Every page the walker visits gets checked, not just photographed. This is what
makes the harness worth running after a big Commander change even when no
screenshot has actually changed: a route that 500s, a JS bundle that throws, an
<img> whose src rotted -- all of it surfaces here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from playwright.sync_api import Page

# Noise we don't want to fail a build over. The console is written to be
# offline-tolerant and degrades loudly when the gateway or the cloud is
# unreachable -- that's expected behaviour on a bench box, not a defect.
_IGNORED_ERRORS = (
    "favicon",
    "ERR_INTERNET_DISCONNECTED",
    "net::ERR_ABORTED",  # our own guard aborting a non-GET request
)

# Content media that simply doesn't exist yet.
#
# A tag that has never been pushed has no rendered image, and a template with no
# thumbnail has no thumbnail -- so the console asks for them, gets a 404, and
# renders a broken <img>. Verified with plain curl outside the harness: these
# 404s are real device state, not something we caused.
#
# They are worth *seeing* (the console arguably ought to show a placeholder
# instead of a broken image), but they are not a regression, and on an unseeded
# bench box there are dozens. Failing the run on them would make the smoke test
# cry wolf every time, which is the fastest way to teach someone to ignore it.
# So: counted and reported, never fatal.
_MISSING_MEDIA = re.compile(r"/tag-image/|/thumbnail|/api/images/\d+/file")


@dataclass
class PageHealth:
    label: str
    url: str
    status: int = 0
    console_errors: list[str] = field(default_factory=list)
    page_errors: list[str] = field(default_factory=list)
    failed_requests: list[str] = field(default_factory=list)
    broken_images: list[str] = field(default_factory=list)
    missing_media: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Healthy. `missing_media` is deliberately not part of this."""
        return (
            200 <= self.status < 400
            and not self.console_errors
            and not self.page_errors
            and not self.failed_requests
            and not self.broken_images
        )

    def summary(self) -> str:
        bits = []
        if not (200 <= self.status < 400):
            bits.append(f"HTTP {self.status}")
        if self.page_errors:
            bits.append(f"{len(self.page_errors)} JS exception(s)")
        if self.console_errors:
            bits.append(f"{len(self.console_errors)} console error(s)")
        if self.failed_requests:
            bits.append(f"{len(self.failed_requests)} failed request(s)")
        if self.broken_images:
            bits.append(f"{len(self.broken_images)} broken image(s)")
        if self.missing_media:
            bits.append(f"{len(self.missing_media)} unrendered image(s)")
        return ", ".join(bits) if bits else "ok"


def _interesting(text: str) -> bool:
    return not any(pat in text for pat in _IGNORED_ERRORS)


def visit(page: Page, url: str, label: str) -> PageHealth:
    """Navigate and collect everything that went wrong on the way."""
    health = PageHealth(label=label, url=url)

    def on_console(msg) -> None:
        if msg.type != "error" or not _interesting(msg.text):
            return
        # A failed-resource console error doesn't name the URL in its text, but
        # its location does -- which is how an unrendered thumbnail gets told
        # apart from a genuinely broken script.
        src = (msg.location or {}).get("url", "")
        if src and _MISSING_MEDIA.search(src):
            return  # already counted via the response handler
        health.console_errors.append(msg.text)

    def on_pageerror(err) -> None:
        if _interesting(str(err)):
            health.page_errors.append(str(err))

    def on_response(resp) -> None:
        if resp.status < 400 or not _interesting(resp.url):
            return
        if _MISSING_MEDIA.search(resp.url):
            health.missing_media.append(f"{resp.status} {resp.url}")
        else:
            health.failed_requests.append(f"{resp.status} {resp.url}")

    page.on("console", on_console)
    page.on("pageerror", on_pageerror)
    page.on("response", on_response)

    try:
        resp = page.goto(url, wait_until="domcontentloaded")
        health.status = resp.status if resp else 0
    except Exception as exc:
        health.page_errors.append(f"navigation failed: {exc}")
        return health

    from . import session

    session.settle(page)

    broken = _broken_images(page)
    health.broken_images = [b for b in broken if not _MISSING_MEDIA.search(b)]
    health.missing_media += [b for b in broken if _MISSING_MEDIA.search(b)]

    page.remove_listener("console", on_console)
    page.remove_listener("pageerror", on_pageerror)
    page.remove_listener("response", on_response)
    return health


def _broken_images(page: Page) -> list[str]:
    """Images with a source that failed to load.

    The `src` check is the whole point. The console is full of <img> nodes that
    the JS fills in later -- row templates, lazily-populated thumbnails -- and
    those sit at naturalWidth 0 with an empty src until data arrives. Counting
    those as "broken" reported 66 failures on /fleet alone, every one of them
    an image that was working exactly as designed. An image is broken when it
    was *asked* to load something and couldn't.
    """
    try:
        return page.evaluate(
            """() => Array.from(document.images)
                 .filter(i => {
                   const src = i.getAttribute('src');
                   if (!src || !src.trim()) return false;   // never asked to load
                   return i.complete && i.naturalWidth === 0;
                 })
                 .map(i => i.currentSrc || i.src)"""
        )
    except Exception:
        return []
