# Connect Odoo

**You'll learn:** how to connect your Commander to Odoo with an API key, and run your first sync — products, prices, and sales orders.

**Before you start:**

- Read [How product sync works](../owners/pos/b0-how-sync-works.md) — five minutes, nothing to click.
- You're signed in to the Guardian console ([Sign in](../getting-started/a3-sign-in.md)).
- You can sign in to Odoo as a user who can read products and sales orders. You'll create an API key for that user in step 1.
- Using Odoo Online (hosted at odoo.com)? API access needs their Custom plan — check yours before you start. Self-hosted Odoo, including the free Community edition, works fully.

1. First, get an API key from Odoo — the Commander signs in with a key, not your password. In Odoo, click your avatar in the top-right corner, open **Preferences** (called **My Profile** in some versions), go to the **Account Security** tab, and click **New API Key**. Give it a name like "Shelf tags", copy the key Odoo shows you, and keep it somewhere safe — Odoo shows it only once.

2. In the Guardian console, click **POS** in the left menu, under **Configuration**, then click the **Odoo** tab.

3. Tell the Commander where Odoo lives:

    - Odoo running in your store or on your own server: type its address into **Host / IP / FQDN** and check the **Port** (Odoo's standard is 8069).
    - Odoo hosted on the web (or behind your company's own web address): put the full address — like `https://acme.odoo.com` — into **Base URL (optional)** instead. When a Base URL is set, it wins over the host and port boxes.

    !!! screenshot "Screenshot: Odoo tab with connection details filled in, Base URL field highlighted"
        To capture: assets/console/pos-odoo-form.png

4. Click **List** next to **Database** and pick your Odoo database. Some Odoo servers keep this list private — if the button comes back empty-handed, just type the database name exactly (whoever runs your Odoo knows it).

5. Enter your **Username / login** — the email address you sign in to Odoo with — and paste the **API key** from step 1 into the **API key** box. It's the key that goes here, not your Odoo password.

6. The **Verify TLS certificate** box: tick it if your Odoo has a real, public web address (hosted Odoo always does). Leave it unticked for a self-hosted Odoo with a self-signed certificate on your own network.

7. Click **Test connection**, then **Save** — the button unlocks once the test passes — then **Run sync now**. Click **Products** in the left menu and watch your catalog fill in.

    !!! screenshot "Screenshot: Odoo Test result card showing OK, Save button enabled"
        To capture: assets/console/pos-odoo-test-ok.png

## What an Odoo connection carries

Odoo gives you the full package: your product catalog and prices for the shelf tags, **plus your customer sales orders** — the fuel for picking lights and will-call pickup signs. Once products are flowing, [Bring in sales orders](../owners/pos/b5-sales-orders.md) shows you how to control which orders sync.

??? note "Advanced options: language, company, pricelist, custom fields"
    Most stores never open the **Advanced (optional)** section. It matters in four cases:

    - **Language** — if your Odoo runs product names in more than one language, set which one the shelf shows (like `en_US`).
    - **Company ID** — if one Odoo runs several companies, pick which company this store syncs from.
    - **Sale pricelist ID** — if your promo prices live on an Odoo pricelist, name it here so sale prices reach the tags.
    - **UDF fields** — a comma-separated list of your custom Odoo product fields (like `x_studio_material`) you want available for label designs, alongside the standard ones in the [data fields reference](../reference/data-fields.md).

    The values for the last three come from whoever administers your Odoo.

## Check your work

- The **Current configuration** card shows your Odoo connection with a green **Active** badge and a **Last sync** time.
- The **Recent syncs** list shows green, completed runs.
- The **Products** page shows your catalog — search for a product you know you carry.

## If something looks wrong

**Test fails at sign-in** — the usual suspect is the key: make sure the **API key** box holds the key from step 1, not your Odoo password. If the key was deleted in Odoo, make a new one.

**The database List comes back empty** — many Odoo servers disable public database listing. Type the name in yourself.

**Products synced, but sale prices didn't** — your promos likely live on a pricelist. Set **Sale pricelist ID** under Advanced and sync again.

**Anything else** — [Fix POS problems](../owners/pos/b6-troubleshooting.md) has the symptom-first list.

**Next:** [Bring in sales orders](../owners/pos/b5-sales-orders.md)
