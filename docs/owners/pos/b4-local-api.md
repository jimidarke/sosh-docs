# Connect a custom system with the Local API

**You'll learn:** how to feed the shelf tags from your own software when your system isn't one of the named tabs — or when you have no POS at all.

**Before you start:**

- Read [How product sync works](b0-how-sync-works.md) — the sync rhythm works a little differently here, and this lesson explains how.
- You're signed in to the Guardian console ([Sign in](../../getting-started/a3-sign-in.md)).
- You have a developer. This is the one lesson in the module written for a technical reader — if that's not you, your job is just to hand this page to whoever builds or maintains your software.

The named tabs all work the same way: the Commander reaches out to your POS and pulls data in. The **Local API** turns that around. Your own system does the talking — it *sends* products, prices, inventory, and sales orders to the Commander whenever they change, over your store's own network. The Commander treats that data exactly like data pulled from a POS: tags render the same, sales flip the same, defaults apply the same.

1. In the Guardian console, click **POS** in the left menu, under **Configuration**, then click the **Local API** tab.

2. Click **Use Local API as POS source**.

    !!! warning "This switches your store's source"
        Your Commander listens to one POS source at a time. Activating the Local API switches off any saved Local DB or Spire connection — only do this if the Local API is genuinely how this store's data will arrive.

3. In the **API keys** card, click **Generate key** and choose what the key may do: a **read-write** key can push data and bind tags; a **read-only** key can only look. Your integration wants read-write; give read-only keys to anything that just reports.

    !!! screenshot "Screenshot: Local API tab with the API keys card showing a freshly generated key banner"
        To capture: assets/console/pos-localapi-keys.png

4. Copy the key the moment it appears. The secret is shown **once** — the console keeps only enough to recognize it, so a lost key can't be re-displayed, only replaced. Store it in your password manager.

5. Hand your developer three things, all on this page:

    - The **Base URL** shown in the **Reference & docs** card — every request goes there.
    - The API key from step 4.
    - The **Open API docs & console** button — it opens the Commander's built-in API reference, with a try-it console for testing calls and a downloadable `openapi.json`. It all works right off the Commander, no internet needed.

## What your integration can do

Through the Local API, your system can push products and price changes, report inventory, submit sales orders, bind tags to products, and read back the state of any tag, product, or order. Anything a polled POS can put on a shelf, a Local API push can too — including sale windows that flip layouts automatically.

Two things behave differently from the polling tabs, and they're both by design:

- **There is no sync schedule.** Data lands the moment your system sends it — the 5-minute rhythm from [How product sync works](b0-how-sync-works.md) doesn't apply, because there's nothing to poll. Fresh is whatever your system makes fresh.
- **Keys work only inside the store.** The API listens on your store's network and nowhere else. A key can never be used from the internet, so a leaked key is useless to anyone who isn't standing in your building — but rotate it anyway.

??? note "Managing keys over time"
    Every key in the list has **Rotate** and **Revoke** buttons. **Rotate** issues a fresh secret for the same key — the old secret stops working, so update your integration in the same sitting. **Revoke** kills the key outright; use it when a system is decommissioned or a contractor moves on. Generate a separate key per system that talks to the Commander, so you can revoke one without breaking the others.

## Check your work

- The **Current configuration** card shows **Local API** as the active source.
- After your developer's first successful push, the **Products** page shows those products — search for one you know was sent.
- Bind one tag to a pushed product ([Bind your first tag](../../getting-started/a5-bind-your-first-tag.md)) and watch the price appear on the shelf.

## If something looks wrong

**The key is lost** — it can't be recovered, only replaced. Click **Rotate** for a fresh secret, or generate a new key and revoke the old one.

**Your integration gets an "unauthorized" answer** — the key was mistyped, rotated without updating the integration, or revoked. Compare against the password manager copy.

**Calls work in the store but not from the office** — that's by design. The Local API never leaves the store network; your integration has to run inside it.

**Next:** [Designing your shelf labels](../templates/index.md)
