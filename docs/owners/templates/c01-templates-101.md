# Understand templates

**You'll learn:** what a template is, how sizes and purposes work, and the three ways to get templates onto your Guardian.

**Before you start:**

- You're signed in to the Guardian console ([Sign in to your Guardian console](../../getting-started/a3-sign-in.md)).
- That's it — this lesson is mostly concepts, with a few clicks at the end.

## What a template is

Every tag in your store shows a small picture. A **template** is the layout behind that picture. It decides where the product name sits, how big the price is, and whether a barcode goes in the corner.

A template doesn't hold a specific product. It holds placeholders — "product name goes here, price goes here." When your Guardian draws the label for a tag, it fills those placeholders with the real product's information from your point-of-sale system (POS). Think of a name-tag sticker: the design is the same for everyone, only the name changes.

The pieces of information a template can show — name, prices, barcode number, stock, and more — are called **data fields**. The full list is in the [data fields reference](../../reference/data-fields.md).

Templates are stored on your Guardian, so browsing, editing, and previewing them keeps working even when the internet is down.

## One template, one size

Tags come in three sizes: 2.1-inch, 3.5-inch, and 5.8-inch. The console shows these as size codes — **TAG21**, **TAG35**, and **TAG58**.

Every template is built for exactly one size. A layout drawn for a small 2.1-inch label can't stretch to fill a 5.8-inch one, so when you bind a tag, you're only offered templates that match its size. Plan on having at least one template for each size you own.

## Every template has a purpose

A template's **purpose** is its job in the store:

- **Normal price** — the everyday shelf label.
- **On-sale** — the layout a tag switches to while its product is on sale.
- **Pick-by-Light** — what tags show while staff pick orders.
- **Will-call** — pickup signs for customer orders.
- **Weather** — weather display boards.

Purposes let your Guardian pick the right layout on its own — for example, flipping a tag to the on-sale look when a sale starts. Downloaded designs sometimes arrive with the wrong purpose, and fixing that takes one click on the Templates page — covered in [Sale layouts and store defaults](c12-sale-layouts-and-defaults.md). For the full picture, see the [template purposes reference](../../reference/template-purposes.md).

## Download ready-made designs

The fastest way to get started is the Sovereign Shelf template library.

1. Click **Templates** in the sidebar.
2. Find the **Template Library** card. It lists ready-made designs published by Sovereign Shelf, each with a badge: **Not downloaded**, **Downloaded**, or **Update available**.
3. Browse freely — nothing installs until you click **Download** on a row.
4. Click **Download** on a design that matches one of your tag sizes. It appears in your own template list, ready to use or edit.

A downloaded template becomes **your copy**. If Sovereign Shelf later improves the original, its row shows **Update available** — but nothing changes until you act. Library updates never overwrite your edits; you choose whether to take the new version.

!!! screenshot "Screenshot: Templates page showing the Template Library card, with one row's Download button and badge highlighted"
    To capture: assets/console/templates-library-card.png

## Import a template file someone shared

Templates can travel as files — useful when another store, or support, sends you a design.

1. On the **Templates** page, click **Upload template** and choose the file you were given.
2. The design appears in your template list, just like one you downloaded.

To share a design the other way, click the download button on any template card. It saves the template as a file you can email or carry on a USB stick — handy for moving designs between stores.

## Build your own

The **+ New template** and **Open Designer** buttons on the Templates page open the **Template Designer** — a drag-and-drop design tool built into your Guardian. The rest of this module teaches it from zero, starting with a tour in the next lesson. No design experience needed.

!!! warning "The golden rule: saving a template changes nothing on the shelf"
    A template in your list is just a design. It only appears on real tags when you set it as a store default for its size ([Sale layouts and store defaults](c12-sale-layouts-and-defaults.md)) or bind tags to it ([Bind your first tag](../../getting-started/a5-bind-your-first-tag.md)). Keep this in mind through the whole module.

## Check your work

- You can say what a template is in one sentence: the layout a tag displays, with live product data filled in when the label is drawn.
- You can match the size codes: TAG21 = 2.1-inch, TAG35 = 3.5-inch, TAG58 = 5.8-inch.
- You can name the five purposes and the three ways to get a template: download, import a file, build your own.
- You remember the golden rule: saving a template changes nothing on any shelf by itself.

## If something looks wrong

**You downloaded a template but your shelves didn't change** — that's expected. A template does nothing until it's a store default or bound to tags. See the golden rule above.

**The library warns it may be out of date** — your Guardian keeps a saved copy of the library, so you can still browse and download while the internet is down. The list freshens when the connection returns.

**You edited a downloaded template and worry an update will erase your work** — it won't. Updates never apply automatically; the **Update available** badge only offers you the choice.

**Next:** [Tour the Designer](c02-designer-tour.md)
