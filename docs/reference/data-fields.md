# Data fields reference

Every field a template can display, grouped the same way they appear in the Designer's **Field** dropdown. To put one on a label, see [Show live product data](../owners/templates/c04-show-live-product-data.md).

## Product

| Field | What it shows |
|---|---|
| Full name | The product's complete name |
| Name line 1 / line 2 | The name split across two lines, for tighter layouts |
| French name / automatic-language name | The French name, or whichever language matches your store's display language |
| Description | The product's longer description |
| Category | The product's category from your POS |

## Pricing

| Field | What it shows |
|---|---|
| Regular price | The everyday shelf price |
| MSRP | The manufacturer's suggested price |
| Sale price | The sale price, when one is set |
| Register price | What the till actually charges right now — sale price during a sale, regular price otherwise |
| Default price | The everyday price, ignoring any sale |
| Sale start / Sale end | The sale's start and end dates, ready-formatted (like "Mar 01") |
| Sale tag line | The short sale message from your POS |
| Cost | Your cost for the product |
| Per-unit prices | Price per unit of measure (per 100 g, per litre, and so on) |

## Identifiers

| Field | What it shows |
|---|---|
| SKU | The product's code in your POS |
| Barcode (UPC) | The product's barcode number |

## Inventory

| Field | What it shows |
|---|---|
| Stock on hand | How many are in stock |
| Committed / Available / Backorder / On order | The usual stock breakdowns from your POS |
| Reorder point | The level that triggers a reorder |
| Stock status | In stock, low, or out — as a word |
| Minimum / Maximum | Your stocking range |
| Capacity | How full the shelf allotment is, as a percentage |

## Details

| Field | What it shows |
|---|---|
| Bin location | Where the product lives in the store |
| Warehouse code | The warehouse or zone code |
| Unit of measure | Each, kilogram, litre, and so on |
| Pack size | Units per pack |
| Weight | The product's weight |

## Supplier

| Field | What it shows |
|---|---|
| Supplier part number | The vendor's own part number |
| Vendor | The supplier's name |
| Discontinued | Whether the product is marked discontinued |

## Price levels 1–5

Volume-pricing tiers from your POS. Each level offers its **name**, **price**, and **minimum quantity** — handy for "1 for $5 / 3 for $12" layouts.

## Custom fields

Your POS's own extra fields. Once your POS is connected, they appear in the dropdown under their real names — whatever your store calls them.

## Order and will-call fields

Used on will-call pickup-sign templates: order number, customer details, pickup code, and bin label. See [Set up will-call pickup signs](../owners/operations/e6-will-call-signage.md).

## Weather fields

Used on weather display templates: current conditions, forecast, and any active weather alert for your city. The weather lessons are coming soon.

## Automatic

| Field | What it shows |
|---|---|
| Render date | The date the label was printed to the tag |
| Tag ID | The tag's own 8-character code |
| Refresh date code | The small month-day stamp many templates print. It updates on every redraw — it's a freshness marker, not a price or batch number |

## If a product doesn't have a field

Each object type handles a missing field its own way:

- **Text and paragraphs** print **blank** — the sample text simply disappears.
- **Barcodes and QR codes** fall back to their **Static Data** value.
- **Icons and pictures** keep whatever you designed.

Blank is often exactly right (no sale price, no sale line) — but always [preview with a real product](../owners/templates/c10-preview-with-real-products.md) that's missing the field, so nothing surprises you on the shelf.

## Which fields your POS provides

Field coverage depends on your POS connection. Spire provides the fullest set, including price levels and custom fields. Odoo provides the core set — name, price, barcode, stock, category, and unit of measure. SQL-database systems like Logivision cover the pricing basics. If a field shows blank for every product, your POS likely doesn't supply it.
<!-- REVIEW: keep this paragraph aligned with the POS module as integrations mature -->
