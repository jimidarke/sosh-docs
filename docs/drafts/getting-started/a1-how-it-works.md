# How Sovereign Shelf works

**You'll learn:** what each part of your Sovereign Shelf system does, and what to expect when a price changes on the shelf.

!!! video "Watch: How Sovereign Shelf works (~4 min)"
    Video coming soon — the written steps below cover everything.

Sovereign Shelf replaces paper price labels with small electronic displays that update themselves. There are three pieces of hardware in your kit, plus one thing you already own: your point-of-sale system (POS).

!!! screenshot "Screenshot: photo of the full kit on a table — one shelf tag, one Beacon, and the Guardian side by side, each labeled"
    To capture: assets/hardware/kit-tag-beacon-guardian.png

## The three parts

**Shelf tags** are the little screens on your shelves. They use e-paper — the same kind of display as an e-reader. An e-paper screen holds its image with zero power. A tag keeps showing its price even with no battery and no connection to anything. That's a feature: the shelf never goes blank, even in a power outage. Each tag runs on a small coin battery you can replace yourself, and the battery lasts years because power is only used when the picture changes.

**Beacons** are small wireless bridges. They connect to the Guardian by cable and talk to the tags over a short-range wireless signal. Each Beacon covers the tags within roughly 10–15 metres (about 30–50 feet). Tags automatically talk to whichever Beacon has the strongest signal, so you can move a tag to a new shelf without changing any settings. (The Guardian console lists Beacons as "Access Points" — same thing.)

**The Guardian** is the small computer that runs everything inside your store. It sits in the back of house, plugged into your router. You manage it through the Guardian console — the dashboard you open in a web browser on your store's network.

## Where prices come from

Your POS stays the source of truth for products and prices. You don't type prices into Sovereign Shelf. Instead:

1. You change a price in your POS, the same way you always have.
2. The Guardian checks your POS every few minutes and spots the change.
3. It updates only the tags whose displayed info actually changed. Everything else stays untouched.

The one thing you do set up in Sovereign Shelf is which tag goes with which product. That's called **bind** — link a tag to a product. You'll do your first bind later in this track.

## What to expect when a tag updates

E-paper is slow on purpose — that's what makes the battery last years. Updates take **minutes, not seconds**:

- A single tag typically refreshes in **1–3 minutes** after a change.
- While it redraws, the tag flashes black, white, and red for **3–5 seconds**. This flashing is normal, not a glitch.
- A full-store refresh of about 300 tags takes roughly **30 minutes per Beacon**. Big price changes are best scheduled, not watched.

!!! warning "A shelf can look fine while updates are paused"
    Because tags never go blank, a shelf full of prices can *look* healthy even when updates aren't going through. If you need to know whether prices are current, check the Guardian console — the console is the source of truth, not the shelf.

## The internet can go down — your store keeps running

Everything that matters runs inside your store. If your internet goes out:

- Tags keep showing their prices.
- Price changes from your POS keep flowing to the shelves.
- Staff phones keep working.

When the connection comes back, the Guardian quietly reconnects on its own.

## Your data never leaves the store

Your products, prices, and POS details stay on the Guardian, inside your store. The cloud dashboard at sovereignshelf.net is used only for health monitoring, support, and software updates. It never sees your product or price data.

## Check your work

You've got the concepts when you can say:

- The three parts are tags (screens), Beacons (wireless bridges), and the Guardian (the store's computer).
- Prices come from your POS — Sovereign Shelf follows it, never the other way around.
- Updates take minutes, and a 3–5 second black/white/red flash is normal.
- The store keeps working without internet, and your data stays local.

## If something looks wrong

**A tag flashes black, white, and red** — that's a normal redraw. Give it 5 seconds.

**You changed a price and the shelf hasn't moved after a minute** — normal. Single tags take 1–3 minutes; a big batch can take half an hour.

**The shelf looks fine but you're not sure updates are flowing** — don't trust the shelf. Open the Guardian console and check there.

**Next:** [Set up the hardware](a2-set-up-the-hardware.md)
