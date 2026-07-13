# Common questions & fixes

Find your symptom, get the fix.

## Tags and prices

### A tag is not updating

Open the Queue page in the Guardian console — the dashboard you open in a web browser on your store's network. If your change is listed there, it's still on its way: the Guardian retries on its own every few minutes, and a full refresh runs every night. If the tag never catches up, open its page and check the signal and battery readings — a weak signal or a low battery is the usual cause. See [Bind your first tag](../getting-started/a5-bind-your-first-tag.md).

!!! tip "The shelf can look fine even when it isn't"
    These screens never go blank, so an out-of-date tag looks just like a healthy one. When in doubt, trust the Guardian console, not the shelf.

### The tag flashed black and white for a few seconds

That's normal. The screen flashes black, white, and red for a few seconds every time it redraws. It's how these displays change their picture — not a defect.

### I unbound a tag but it still shows the old price

That's expected. The screen keeps its last image even with no power. Unbinding removes the link to the product, but the display won't change until you bind the tag again (bind — link a tag to a product). Pull the tag off the shelf, or bind it to something new.

### The shelf shows a sale that should not exist

The tag shows exactly what your point-of-sale system (POS) sends. If a product's sale price is at or above its regular price, the tag still displays it as a sale. Fix the promo in your POS — the tag corrects itself after the next sync.

### The stock count on a tag looks stale

Only changes to a product's name, price, or sale dates redraw a tag right away. Stock-only changes wait for the nightly refresh, so the count catches up overnight. Nothing is broken.

### My weather sign disappeared

Someone bound a product to that tag — a product binding always wins over the weather display. Unbind the tag and it goes back to showing the weather.
<!-- REVIEW: weather lessons are not yet published — add a link once the weather module lands -->

## The Guardian console

### I clicked Stage and nothing happened

That's what Stage is for: it saves your change for delivery later, so shelves don't flicker in front of customers. Push sends the update to the tag now. If you want the tag to change right away, use Push instead. See [Bind your first tag](../getting-started/a5-bind-your-first-tag.md).

### There is no cancel button on the Queue page

Correct — that's by design. To fix a change you didn't mean to send, just re-bind the tag. The newer change automatically replaces the older one waiting in the queue.

### I cannot reach the console address

Some routers block friendly local names like http://commander.local:8080.
<!-- REVIEW: confirm commander.local on shipping builds -->
Use the Guardian's IP address instead: find it in your router's device list, then type that address into your browser. [Sign in to your Guardian console](../getting-started/a3-sign-in.md) walks through it.

### How do I design my own templates?

The [Designing your shelf labels](../owners/templates/index.md) module walks you through it, from downloading ready-made designs to building your own from scratch.

## Products and your POS

### Prices stopped syncing mid-week

Your POS password probably changed — that's the most common cause. Open the POS page in the console, re-enter the new password, and click Save. It takes effect immediately, no restart needed. See [Connect your product data](../getting-started/a4-connect-your-product-data.md).

### The Save button on the POS page is greyed out

Run Test connection first. Save stays locked until a test passes — it's a safety check, not a bug. Once the test succeeds, Save unlocks.

## Store handhelds

### A tab is missing on the handheld

The owner turned that feature off. The toggles live on the console's System page, and changes reach the phones within about a minute. The reverse can happen too: when a phone can't reach the Guardian, it shows everything — so a turned-off tab may reappear until the phone reconnects.

### The handheld says it's in the wrong store

The phone is on another store's network. Move it back to your store, and it works again. If the phone should belong to this store, reset it and pair it fresh. See [Train your team](../getting-started/a7-train-your-team.md).

### The barcode scanner stopped working after a phone reset

A reset wipes the scanner's Bluetooth pairing. A manager needs to re-pair it in the app's Settings, which is protected by the manager PIN. One more thing: the scanner status icon's colour isn't reliable — test with a real scan instead of waiting for it to turn green.

### There is an unfamiliar Wi-Fi network in my store

That's your Beacons — the wireless bridges that talk to your tags. They broadcast their own small network for the store handhelds. It's expected. Leave it alone. See [Set up the hardware](../getting-started/a2-set-up-the-hardware.md).

### How do I pick orders with the flashing lights?

Lesson coming soon — Pick by Light gets its own staff lesson.

### How do I set up will-call pickup signs?

Lesson coming soon — will-call pickup signage gets its own lessons for owners and staff.

## Getting help

### How do I get help?

Email Sovereign Shelf support (support@sovereignshelf.com). Describe what you see and what you were doing. With your consent, support can also assist remotely through your Guardian's built-in secure connection — no firewall changes and nothing to install on your side.
