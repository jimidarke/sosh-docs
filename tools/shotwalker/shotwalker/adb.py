"""Driving the handheld over adb.

The third surface. The console and the Designer are web apps and are driven with a
browser; the staff app is an Android build on a real phone, and no browser can see
it -- which is why eight `assets/app/*` shots sat as placeholders while every other
surface was automated.

Two things here are deliberate and worth knowing before you extend this:

* **Nodes are found by text, not coordinates.** `uiautomator dump` gives a tree with
  bounds; this module looks a node up by its text/description/id and taps the centre
  of *that*. Tapping literal coordinates works exactly until someone moves a button,
  and then it silently taps the wrong thing and screenshots the result -- which is
  worse than failing.

* **This surface is NOT reveal-only, and cannot be.** The lessons it illustrates are
  writes: saving a multi-product grid, assigning a will-call order, releasing a sign.
  guard.py protects the *browser* surfaces and does nothing here. So this module has
  no business pointing at a store's phone -- it is a bench tool. The browser guards
  are what make shotwalker safe against a customer's Commander; nothing makes this
  safe against a customer's handheld, and it should not pretend otherwise.
"""

from __future__ import annotations

import io
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from PIL import Image

PACKAGE = "com.sovereignshelf.mobile"


class AdbError(RuntimeError):
    pass


@dataclass(frozen=True)
class Node:
    text: str
    desc: str
    rid: str
    cls: str
    bounds: tuple[int, int, int, int]  # left, top, right, bottom
    clickable: bool = False
    # The nearest clickable ancestor's bounds, if this node is not itself the button.
    # Compose renders a button's label as its own node, so the text you search for is
    # usually a child of the thing a finger actually hits. Highlighting the label
    # instead of the button draws a box *inside* the button, which reads as a nested
    # control rather than a callout.
    hit_bounds: tuple[int, int, int, int] | None = None

    @property
    def box(self) -> tuple[int, int, int, int]:
        return self.hit_bounds or self.bounds

    @property
    def centre(self) -> tuple[int, int]:
        l, t, r, b = self.box
        return (l + r) // 2, (t + b) // 2

    def __str__(self) -> str:
        label = self.text or self.desc or self.rid or self.cls
        return f"{label!r} @ {self.box}"


_BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")


def _sh(*args: str, binary: bool = False, timeout: int = 30):
    proc = subprocess.run(
        ["adb", *args], capture_output=True, timeout=timeout, check=False
    )
    if proc.returncode != 0:
        raise AdbError(f"adb {' '.join(args)} failed: {proc.stderr.decode()[:200]}")
    return proc.stdout if binary else proc.stdout.decode("utf-8", "replace")


class Device:
    """One connected handheld."""

    def __init__(self) -> None:
        out = _sh("devices")
        live = [l for l in out.splitlines()[1:] if l.strip().endswith("device")]
        if not live:
            raise AdbError(
                "no handheld on adb — plug the phone in and authorise the host, "
                "then re-run (`adb devices` should list it as 'device')"
            )
        self.serial = live[0].split()[0]
        self._cache: list[Node] | None = None

    # -- reading -----------------------------------------------------------

    def _stale(self) -> None:
        """The screen may have changed; the next read must go to the device."""
        self._cache = None

    def dump(self) -> list[Node]:
        """The current screen's node tree, cached until something is tapped.

        The cache is not an optimisation for its own sake. A `uiautomator dump` is a
        round trip to the phone and costs the better part of a second, and the helpers
        here ask "what is on screen?" constantly -- checking a row, finding a button,
        counting filled slots. Uncached, one recipe spent minutes doing nothing but
        re-reading a screen that had not moved, and timed out.

        Every method that touches the device invalidates it, so a stale tree is never
        handed back after an interaction.
        """
        if self._cache is not None:
            return self._cache
        self._cache = self._read_nodes()
        return self._cache

    def _read_nodes(self) -> list[Node]:
        _sh("shell", "uiautomator", "dump", "/sdcard/sw.xml")
        xml = _sh("shell", "cat", "/sdcard/sw.xml")
        xml = xml[xml.find("<?xml") :].strip()
        try:
            root = ET.fromstring(xml)
        except ET.ParseError as exc:
            raise AdbError(f"could not parse the UI dump: {exc}") from exc

        nodes: list[Node] = []

        def walk(el, clickable_box: tuple[int, int, int, int] | None) -> None:
            m = _BOUNDS.match(el.get("bounds", ""))
            box = tuple(int(g) for g in m.groups()) if m else None
            clickable = el.get("clickable") == "true"

            # Carry the nearest clickable ancestor down the tree.
            inherited = box if (clickable and box) else clickable_box

            if box:
                nodes.append(
                    Node(
                        text=el.get("text", ""),
                        desc=el.get("content-desc", ""),
                        rid=el.get("resource-id", ""),
                        cls=el.get("class", ""),
                        bounds=box,  # type: ignore[arg-type]
                        clickable=clickable,
                        hit_bounds=None if clickable else clickable_box,
                    )
                )
            for child in el:
                walk(child, inherited)

        for el in root:
            walk(el, None)
        return nodes

    def find(
        self,
        text: str | None = None,
        *,
        desc: str | None = None,
        rid: str | None = None,
        exact: bool = False,
    ) -> Node | None:
        """First node matching. Substring match unless `exact`."""

        def hit(hay: str, needle: str) -> bool:
            return hay == needle if exact else needle.lower() in hay.lower()

        for n in self.dump():
            if text is not None and n.text and hit(n.text, text):
                return n
            if desc is not None and n.desc and hit(n.desc, desc):
                return n
            if rid is not None and n.rid and hit(n.rid, rid):
                return n
        return None

    def need(self, text: str | None = None, **kw) -> Node:
        n = self.find(text, **kw)
        if n is None:
            wanted = text or kw.get("desc") or kw.get("rid")
            raise AdbError(f"no {wanted!r} on screen")
        return n

    def wait_for(self, text: str | None = None, *, timeout: float = 10.0, **kw) -> Node:
        deadline = time.time() + timeout
        while time.time() < deadline:
            self._stale()
            n = self.find(text, **kw)
            if n is not None:
                return n
            time.sleep(0.5)
        wanted = text or kw.get("desc") or kw.get("rid")
        raise AdbError(f"{wanted!r} never appeared (waited {timeout:.0f}s)")

    def screen(self) -> Image.Image:
        return Image.open(io.BytesIO(_sh("exec-out", "screencap", "-p", binary=True)))

    # -- driving -----------------------------------------------------------

    def tap(self, target: Node | str, *, settle: float = 1.2, **kw) -> None:
        node = target if isinstance(target, Node) else self.need(target, **kw)
        x, y = node.centre
        _sh("shell", "input", "tap", str(x), str(y))
        self._stale()
        time.sleep(settle)

    def type_keys(self, text: str, *, settle: float = 0.3) -> None:
        """Type on the app's own on-screen keypad, one tap per character.

        `adb shell input text` does nothing here. The app's sheets draw their own
        Compose keypad rather than using an IME, so system-level text goes nowhere and
        the field keeps its placeholder -- which looks exactly like a hung script.

        There is no space key, on any of the sheets. That is the app's constraint, not
        this harness's: a header typed on the handheld is a single word.
        """
        keys = {n.text.upper(): n for n in self.dump() if len(n.text) == 1}
        for ch in text:
            key = keys.get(ch.upper())
            if key is None:
                raise AdbError(
                    f"no {ch!r} key on this keypad"
                    + (" (the app's keypads have no space key)" if ch == " " else "")
                )
            x, y = key.centre
            _sh("shell", "input", "tap", str(x), str(y))
            self._stale()
            time.sleep(settle)

    # Kept: the tag sheet is hex-only, and naming that at the call site documents it.
    type_hex = type_keys

    def swipe(self, x1: int, y1: int, x2: int, y2: int, ms: int = 400, *, settle: float = 1.0) -> None:
        _sh("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms))
        self._stale()
        time.sleep(settle)

    def scroll(self, dy: int = -500) -> None:
        """Negative dy scrolls down the page (content moves up)."""
        self.swipe(360, 1100, 360, 1100 + dy)

    def back(self, *, settle: float = 1.0) -> None:
        _sh("shell", "input", "keyevent", "KEYCODE_BACK")
        self._stale()
        time.sleep(settle)

    def wake(self) -> None:
        """Wake, dismiss the keyguard, and stop the screen sleeping mid-run."""
        _sh("shell", "input", "keyevent", "KEYCODE_WAKEUP")
        time.sleep(0.5)
        _sh("shell", "input", "swipe", "360", "1400", "360", "400", "300")
        time.sleep(1.0)
        _sh("shell", "settings", "put", "system", "screen_off_timeout", "600000")
        self._stale()

    def restart_app(self) -> None:
        """Back to a known screen. Recipes must not inherit each other's state."""
        _sh("shell", "am", "force-stop", PACKAGE)
        time.sleep(1.0)
        _sh("shell", "monkey", "-p", PACKAGE, "-c", "android.intent.category.LAUNCHER", "1")
        self._stale()
        time.sleep(3.0)
