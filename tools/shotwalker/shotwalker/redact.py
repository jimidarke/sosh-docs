"""Keep secrets out of the PNGs.

Masking happens at capture time -- Playwright paints a solid block over the
region before the image is encoded -- so a PIN or an API key never exists in a
file on disk, not even briefly. That matters because these images are committed
to a public docs repo.

Two classes of mask, and the difference is deliberate:

  SECRET   always masked, in every capture. Non-negotiable.
  VOLATILE masked only in the baseline sweep, where run-to-run diffing is the
           point. Doc shots keep the real content -- the Dashboard shot is
           explicitly meant to show the Cloud pill, so masking it there would
           defeat the shot.
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page

# Credentials, keys, and PINs. Never allowed into an image.
SECRET_SELECTORS = [
    'input[type="password"]',  # sql/spire/odoo passwords, secrets export/restore
    "#pin-input",
    "#pin-reveal-value",
    "#key-new",  # a freshly minted API key, shown once
    "#key-list",
    "#secrets-pw",
    "#secrets-pw2",
    "#secrets-restore-pw",
    # Infrastructure. sosh-docs is a PUBLIC repo, and its README is explicit:
    # no infrastructure or network details. The POS page prints the Commander's
    # own LAN address and internal API path in its "Base URL" box, and the POS
    # source tabs echo back customer database hostnames -- all of which would
    # otherwise be baked into an image on the public help site. (It happened:
    # the first pos-config-tabs.png shipped the appliance's LAN IP.)
    "#localapi-base",
    "#odoo-base-url",
    "#odoo-host",
    "#spire-host",
    "#sql-host",
    "#odoo-database",
    "#sql-database",
]

# The /license page prints its lease UUID and signature into bare <code> blocks
# with no ids of their own, so it gets a page-scoped rule.
SECRET_SELECTORS_BY_PATH = {
    "/license": ["code"],
}

# Real content, but it churns between runs and would make every baseline diff
# look like a change: the cloud-status pill flips with actual cloud reachability,
# the licence banner appears and changes colour over time, the update badge
# alters the sidebar on every page, and relative timestamps tick.
VOLATILE_SELECTORS = [
    ".status-bar",
    ".license-banner",
    ".nav-pill",
    "[data-relative-time]",
]


def secret_masks(page: Page, path: str = "") -> list[Locator]:
    """Locators to black out in every capture."""
    selectors = list(SECRET_SELECTORS)
    for prefix, extra in SECRET_SELECTORS_BY_PATH.items():
        if path.startswith(prefix):
            selectors.extend(extra)
    return [page.locator(s) for s in selectors]


def volatile_masks(page: Page) -> list[Locator]:
    """Locators to black out only in the baseline sweep."""
    return [page.locator(s) for s in VOLATILE_SELECTORS]
