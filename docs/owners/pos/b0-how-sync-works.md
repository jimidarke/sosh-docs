# How product sync works

**You'll learn:** what your Commander copies from your POS, how often, and which changes reach the shelf right away.

**Before you start:**

- Nothing to click in this lesson — it's a five-minute read.
- If you haven't yet, skim [Connect your product data](../../getting-started/a4-connect-your-product-data.md) for the one-page version of this story.

## Little and often

Your Commander checks your POS for changes about **every 5 minutes**, around the clock. Each check picks up only what changed since the last one, so it's light work for your POS server — your register never notices it.

Once a night, in the small hours (around 3 a.m.), the Commander also re-reads your **whole catalog** from scratch. That nightly pass catches anything the quick checks could have missed and trues everything up while the store is closed.

You don't schedule any of this, and you can't forget to run it. The only button you'll ever press is **Run sync now** on the POS page, and even that is optional — it just saves you a few minutes of waiting after you change something.

## What redraws a tag right away

Not every change in your POS is worth waking a shelf tag for. The Commander redraws a tag within minutes when a product's **name**, **price**, or **sale dates** change — the things a shopper actually reads.

Everything else — stock counts especially — waits for the nightly pass.

!!! tip "A stale stock count doesn't mean sync is broken"
    If you sell three units and the tag still shows yesterday's count, nothing is wrong. Stock-only changes catch up overnight, by design. Prices always move within minutes.

## Sales start and end on their own

Put a sale price and its start and end dates on a product in your POS, and that's the whole job. On the start date the product's tags flip to your sale layout, and when the sale ends they flip back — including the midnight changeovers, while nobody is in the store.

For the flip to work, your store needs a sale layout paired with its everyday one. You set that up once on the Templates page — [Put templates to work](../templates/c12-sale-layouts-and-defaults.md) walks through it.

!!! warning "The shelf trusts your POS — even about bad promos"
    Tags show exactly what your POS sends. If a product's sale price is *at or above* its regular price, the shelf still dresses it up as a real sale — there is no guard against it. Before a promo goes live, make sure the numbers in your POS are the numbers you mean.

## Your POS stays in charge

The connection runs in one direction: the Commander **reads** your catalog. It doesn't edit your prices, rename your products, or touch your inventory — your POS remains the single source of truth, which is also why there's no form for typing products in by hand.

That has one consequence worth knowing: if you **delete** a product from your POS, its shelf tags don't hold the old price forever. They revert to your store's default layout at the next sync, so the shelf never advertises something you no longer sell.

If your IT support or POS provider asks what this connection does to their system, the answer is: it signs in with the read-only access you gave it, reads products and prices, and nothing more.

## Your credentials stay in the store

The username and password (or API key) you enter on the POS page are encrypted and stored **on your Commander** — they are never sent to the cloud, and Sovereign Shelf never sees them.

!!! tip "Keep your POS credentials in your own password manager"
    Because your credentials never leave the store, nobody can recover them for you. If your Commander is ever replaced or re-provisioned, you'll type them in again — that's a security feature, not a fault. [Fix POS problems](b6-troubleshooting.md) covers what that moment looks like.

## Check your work

There's nothing to configure in this lesson, but you can watch the rhythm happen: open the **POS** page in the Guardian console and look at the **Recent syncs** list. You'll see a fresh entry appear every few minutes, each one green.

**Next:** pick the lesson for your system — [SQL-database POS](b1-sql-database-pos.md) (Logivision and others), [Spire](b2-spire.md), or [a custom system](b4-local-api.md).
