# Put templates to work: purposes, sale pairs, and defaults

**You'll learn:** how to give each template a purpose, link Normal and On-sale layouts into an automatic sale pair, set your store defaults, and keep your template library tidy.

**Before you start:**

- You're signed in to the Guardian console ([Sign in to your Guardian console](../../getting-started/a3-sign-in.md)).
- You have at least one saved template per tag size you own — downloaded, imported, or built yourself ([Understand templates](c01-templates-101.md)).

One thing up front: this whole lesson happens on the **console's Templates page**, not in the Designer. The Designer draws layouts; putting those layouts to work — purposes, pairs, defaults — is console work. You can leave the Designer closed.

## Give each template a purpose

A template's purpose is its job: Normal price, On-sale, Pick-by-Light (idle and active), Will-call (idle and active), or Weather (normal and alert). The purpose is how your Guardian knows which layout to reach for on its own. The full taxonomy — and what resolves automatically where — is in the [template purposes reference](../../reference/template-purposes.md).

1. Click **Templates** in the sidebar.
2. Look at your template cards. Each one shows a **purpose pill** — a small label naming its job.
3. To change one, click the pill, pick the right purpose from the dropdown, then click the **checkmark** to confirm.

!!! screenshot "Screenshot: a template card with its purpose pill dropdown open, the checkmark button highlighted"
    To capture: assets/console/templates-purpose-pill.png

!!! warning "Fix the pill before anything else"
    Downloaded and imported templates often arrive with the wrong purpose. Check the pill first — only templates with the correct purpose (and marked active) appear in the Defaults dropdowns below. A "missing" template is almost always a mislabeled one.

## Set the store defaults

You met the Defaults card in [Set your first-day settings](../../getting-started/a6-first-day-settings.md). Here's the deeper why.

The **Defaults** card picks one template per tag size for each job. That single choice does a lot of quiet work:

1. On the **Templates** page, find the **Defaults** card. Under Price tags there's one row per tag size — TAG21, TAG35, TAG58 (2.1-inch, 3.5-inch, and 5.8-inch labels).
2. Pick a template in the **Normal** dropdown for each size you own. This is the everyday price layout — and it's what handheld binds rely on. When staff bind a tag from a phone, the Guardian uses this default automatically.
3. Pick a template in the **Onsale** dropdown for each size too. Setting **both** Normal and Onsale for a size links them as a **pair**.
4. Watch for the **Saved** tick — each pick saves instantly.

Once a pair is linked, sales run themselves. While a product's sale window — the sale dates from your point-of-sale system (POS) — is active, its tags flip to the On-sale layout. When the sale ends, they flip back. Flips happen automatically just after midnight, store time, with nothing to click.

The rows below Price tags work the same way for other jobs: Pick-by-Light (Idle and Active), Will-call (Idle and Active), and Weather (Regular and Alert). Each feature's own lesson covers when to fill them in.

!!! screenshot "Screenshot: the Defaults card with one size row's Normal and Onsale dropdowns both set, the Saved tick visible"
    To capture: assets/console/templates-defaults-pair.png

??? note "When several templates share a purpose"
    If more than one active template has the same size and purpose, automatic picks use the **alphabetically first** one. To control which wins, rename the templates — the name lives in the Designer's Template Parameters panel ([Tour the Designer](c02-designer-tour.md)) — or have staff pick a template explicitly with the **Edit** button on the handheld.

## Tidy your library

As your library grows, three card buttons keep it manageable:

- **Duplicate** makes a copy — the safe way to experiment. Edit the copy freely; the original keeps working on your shelves.
- **Deactivate** hides a template from every dropdown — bind forms and Defaults alike — without touching tags that already use it. Perfect for retiring seasonal layouts.
- **Delete** removes a template for good, but it's blocked while the template is a store default or bound to any tag. If delete refuses, deactivate instead.

To move a design between stores, use the file buttons: the download button on a card saves the template as a file, and **Upload template** imports one you were given. Email it or carry it on a USB stick.

## Check your work

- Every template card shows the purpose pill you expect.
- The Defaults card has both **Normal** and **Onsale** set for every tag size you own.
- Templates you no longer offer are deactivated, not deleted.

## If something looks wrong

**A handheld says "no default template configured"** — the error names a tag size. Set the **Normal** default for that size on the Defaults card.

**A template is missing from a Defaults dropdown** — its purpose pill is wrong, or it's deactivated. Fix the pill or reactivate it; it appears right away.

**The sale price shows but the layout didn't change** — that size has no **Onsale** default, so there's no pair. The tag keeps the Normal layout and just shows the sale price data. Set the Onsale dropdown for that size.

## You've finished the module

That's the loop closed: design in the Designer, then purpose, pair, and default on the console — and your shelves take care of themselves. Revisit any lesson from the [module index](index.md). Two more lessons are coming soon: pictures and image placeholders, and multi-product templates.

**Next:** [Template purposes reference](../../reference/template-purposes.md) — keep it handy while you sort your library.
