"""Where the Commander lives, and what a capture should look like.

The target address and credentials come from the environment and are NOT
defaulted here. That is deliberate, not fussiness: sosh-docs is a public repo,
and its README says plainly to keep infrastructure, network details, and auth
internals out of it. A hardcoded appliance IP and password in this file would be
on the public internet the moment it was pushed.

Put them in `shotwalker.env` (gitignored) beside this tool, or export them:

    SOSH_HOST=<commander-address>
    SOSH_USER=<console-user>
    SOSH_PASS=<console-password>

`shotwalker.env.example` shows the shape.
"""

from __future__ import annotations

import os
from pathlib import Path

# tools/shotwalker/shotwalker/config.py -> repo root is three parents up.
REPO_ROOT = Path(__file__).resolve().parents[3]
DOCS_DIR = REPO_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
ENV_FILE = Path(__file__).resolve().parents[1] / "shotwalker.env"


def _load_env_file() -> None:
    """Read shotwalker.env, if present. Real env vars win."""
    if not ENV_FILE.is_file():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


_load_env_file()


class MissingTarget(RuntimeError):
    """No Commander address configured."""


def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise MissingTarget(
            f"{name} is not set. Copy tools/shotwalker/shotwalker.env.example to "
            f"tools/shotwalker/shotwalker.env and fill it in, or export {name}. "
            f"Nothing is defaulted in source — this repo is public."
        )
    return value


def console_url() -> str:
    return os.environ.get("SOSH_CONSOLE_URL") or f"http://{_required('SOSH_HOST')}:8080"


def designer_url() -> str:
    return os.environ.get("SOSH_DESIGNER_URL") or f"http://{_required('SOSH_HOST')}:8090"


def username() -> str:
    return _required("SOSH_USER")


def password() -> str:
    return _required("SOSH_PASS")

# From sosh/docs/trackers/2026-07-11-guardian-training-docs.md, "Screenshot
# system": fixed 1440x900, light theme. Below ~1280 the Designer replaces the
# whole page with a "Desktop Only" overlay, so this is a floor, not a taste.
VIEWPORT = {"width": 1440, "height": 900}
DEVICE_SCALE_FACTOR = 2

# Existing docs/assets/app/ captures are all 720px wide; match them.
DOC_IMAGE_WIDTH = 720

# Brand copper. The docs bake callout outlines into the PNG, so we draw them at
# capture time rather than leaving them for someone to add by hand.
HIGHLIGHT_COLOUR = "#C2703D"
MASK_COLOUR = "#0B1F3A"  # brand navy, for redacted regions

# The clock is frozen here so relative timestamps ("2 minutes ago") and the
# 1Hz tickers render identically on every run. Any fixed instant works; this
# one is arbitrary but stable.
FROZEN_CLOCK = "2026-07-13T09:00:00"

NAV_TIMEOUT_MS = 20_000
SETTLE_MS = 1_200
