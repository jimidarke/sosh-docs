# Fix POS problems

Find your symptom, get the fix. Everything here plays out on the **POS** page of the Guardian console — and most fixes take under a minute.

### Prices stopped syncing mid-week

The number-one cause, by a wide margin: **the password changed on the POS side**. IT rotated it, the POS provider did maintenance, someone tidied up accounts — and the Commander's stored copy went stale.

The fix is quick: open the **POS** page, re-enter the new password on your system's tab, click **Test connection**, then **Save**. It takes effect immediately — no restart, and the next sync catches up on everything missed in between.

### The connection test fails

The failure message tells you which part went wrong. Match it up:

- **Can't reach the server** — the address or port is wrong, the POS server is off, or a firewall or separate network segment stands between it and the Commander. This one's for your IT support.
- **Sign-in refused** — the username, password, API key, or company is wrong or was changed. Re-enter and test again; ask your POS provider if you're locked out.
- **Database problems** — the database name is wrong, or the login can't see it. On the Local DB tab, click **List** next to the Database box to see what the login *can* see; if the list is empty, your POS provider needs to grant access.

On the Local DB tab, **Auto-detect TLS** is worth one click before you call anyone — it clears up the connection-security mismatches that produce the most confusing errors.

### The Save button is greyed out

Run **Test connection** first. Save stays locked until a test passes — it's a safety check that keeps a broken connection from being stored, not a bug.

### My saved connection disappeared

Your Commander keeps exactly **one** active POS source. If someone saved a connection on a different tab — even "just to try it" — it replaced yours. Nothing is lost that can't be redone: go back to your system's tab, re-enter the details, test, and save. And agree on who owns this page.

### The Commander was replaced or re-provisioned

After a hardware swap or a re-provisioning visit, POS syncing stops until you re-enter your credentials — and that's **by design**, not a fault. Credentials are encrypted so tightly to each individual Commander that a replacement can't read the old ones. (Today this surfaces as a generic sync error rather than a friendly prompt — if syncing died right after a swap, this is why.)

Re-enter the credentials on the POS page, test, save, done. The same applies after restoring from a backup.

!!! tip "This is the moment the password manager pays off"
    Sovereign Shelf never has a copy of your POS credentials — they never leave the store. Keep them in your own password manager so a re-entry moment is a 60-second job, not an archaeology dig.

### Syncs are green but the shelf didn't change

The connection is fine — the change you're waiting for just doesn't redraw a tag immediately:

- **Stock counts** wait for the nightly pass. Prices move within minutes; inventory catches up overnight ([How product sync works](b0-how-sync-works.md)).
- **Is a tag even bound to that product?** A product with no bound tag has nowhere to show its price ([Bind your first tag](../../getting-started/a5-bind-your-first-tag.md)).
- **Still stuck?** Check the Queue page — if the change is listed there, it's on its way and retries on its own. A tag that never catches up usually has a weak signal or a low battery; the [FAQ](../../reference/faq.md) covers that chase.

### The shelf shows a sale that shouldn't exist

The tag is faithfully displaying what your POS sent. If a sale price is at or above the regular price, the shelf still dresses it as a sale — there's no guard. Fix the promo in your POS; the tag corrects itself on the next sync.

### An order is missing from the Sales Orders page

Almost always the sync filter — the order's status isn't ticked, or it's older than your max age. [Bring in sales orders](b5-sales-orders.md) walks the filter end to end.

### Products page is empty after the first sync

A large catalog takes a while on its very first pass. Give it a few minutes and refresh. If it's still empty, check the **Recent syncs** list on the POS page — a green run with a product count means data is arriving; a red one names the error.

### Still stuck?

Email Sovereign Shelf support (support@sovereignshelf.com) with what you see on the POS page — the **Current configuration** card and the last few entries in **Recent syncs** say most of what support needs to know.

**Next:** [Designing your shelf labels](../templates/index.md)
