# Connect your product data

**You'll learn:** how the Guardian gets products and prices from your point-of-sale system, and how to run your first sync.

**Before you start:**

- You're signed in to the Guardian console — the dashboard you open in a web browser on your store's network ([Sign in to your Guardian console](a3-sign-in.md)).
- You have the connection details for your point-of-sale system (POS): the server address, plus a read-only username and password (or API key). Your POS provider or IT support can give you these.

Every product and price on your shelf tags comes from your POS. There is no form for typing products in by hand. The Guardian reads your catalog straight from the POS, so the shelf always matches the register.

This lesson gets your first sync running. Each POS also gets its own detailed walkthrough later, in the Connecting your POS lessons — SQL-database systems like Logivision, Spire, Odoo, and the Local API for custom integrations.

1. In the Guardian console, click **POS** in the left menu, under **Configuration**.
2. Pick the tab that matches your system. There are four tabs, one per source type:

    - **Local DB** — POS systems built on a SQL database, such as Logivision.
    - **Spire API** — Spire.
    - **Odoo** — Odoo.
    - **Local API** — custom integrations built by your own developer or IT team.

    !!! screenshot "Screenshot: POS Configuration page with all four tabs visible, tab row highlighted"
        To capture: assets/console/pos-config-tabs.png

3. Find your POS server. Click **Detect on LAN** where the tab offers it — it scans your store network and lists what it finds, and clicking a result fills in the address for you. Otherwise, type the server address yourself.
4. Enter the read-only username and password (or API key) from your POS provider.
5. Click **Test connection**. The test runs entirely on your Guardian and finishes in seconds. If it fails, the message names the exact stage that failed — that's your clue for the fixes below.
6. Click **Save**. The button stays disabled until your test passes. Your credentials are encrypted and stored on your Guardian only — they never leave the store.
7. Click **Run sync now**. (If you skip this, the first sync starts on its own within about 5 minutes.)
8. Click **Products** in the left menu and watch your catalog fill in.

    !!! screenshot "Screenshot: Products page filled with a synced catalog, search box highlighted"
        To capture: assets/console/products-page-synced.png

!!! warning "One source at a time"
    Exactly one POS source can be active. Saving a different tab replaces your current connection. Don't fill in a second tab "just to try it" unless you mean to switch.

!!! tip "Keep your POS credentials somewhere safe"
    Because your credentials never leave the store, Sovereign Shelf can't recover them for you. Keep them in your own password manager — you'll need to type them in again if your Guardian is ever replaced.

From here on, there's nothing to click. The Guardian re-checks your POS about every 5 minutes. Change a price at the register, and the matching shelf tags update on their own.

??? note "No POS system, or a custom one?"
    The Guardian has no manual product-entry form, so products must arrive through a connection. If your system isn't one of the named tabs, the **Local API** tab lets your own developer send products to the Guardian directly — it includes built-in API documentation. Not sure which path fits your store? Ask Sovereign Shelf support (support@sovereignshelf.com).

## Check your work

- The **Products** page shows your catalog. Try searching for a product you know you carry.
- On the **POS** page, the **Recent syncs** list shows green, successful runs.

## If something looks wrong

**Test fails at the network stage** — check the server address and port, and ask your IT support whether a firewall is blocking the Guardian from reaching the POS server.

**Test fails at the login stage** — the username, password, or API key is wrong. Re-enter it and test again.

**Sync succeeded but Products looks empty** — a very large catalog can take a while on its first sync. Wait a few minutes, then refresh the page.

Your products are flowing in. Next you'll bind your first tag — bind means linking a tag to a product — and watch a real price appear on the shelf.

**Next:** [Bind your first tag](a5-bind-your-first-tag.md)
