---
search:
  exclude: true
---

# Tester Setup

Before you start, you need a few things in place. Allow ~10 minutes.

## Everyone

- A modern browser (Chrome, Firefox, Edge, Safari — any current version).
- A username + password from the author. You'll get these by email.
- The URLs:
  - **Admin console:** `https://sovereignshelf.net/admin`
  - **Designer:** `https://sovereignshelf.net/design`
  - **Storefront:** `https://sovereignshelf.com`
- A copy of [result-template.md](result-template.md) saved locally,
  renamed to `results-<your-first-name>.md`. You'll fill this in as
  you go.

That's enough to run the `[CLOUD]` cases.

## Mobile testers (`[MOBILE]`)

Additionally:

- An Android phone (Android 10 or newer).
- The Sovereign Shelf APK, sent to you by the author. Sideload-only —
  you'll need to enable "install from unknown sources" for your file
  manager or browser when you tap it. This is normal for our app;
  it's not on the Play Store.
- A QR code from the author for first-boot device binding. **Do not
  share this QR code** — it's tied to your tester account and burns
  on first use.

## Full-kit testers (`[KIT]`)

Additionally:

- A Guardian Commander unit (small mini-PC with multiple ethernet ports).
- A beacon (the small white box).
- At least 3 ESL tags, already provisioned by the author.
- An ethernet cable + power for the Commander.
- A spare HDMI display + USB keyboard for the TUI cases. (You can
  skip the TUI section if you don't have these — mark them `N-A`.)

The author will have already done the three-USB onboarding before
shipping the kit to you. You should not need to touch USBs. If
something looks unprovisioned (the dashboard never loads), stop and
contact the author — that's a setup issue, not a UAT failure.

## Confirm before you start

- [ ] You can reach `https://sovereignshelf.net/admin` and the page
      asks you to log in.
- [ ] Your provided credentials log you in successfully.
- [ ] You can see the demo store dashboard after login.

If any of these fail, that **is** UAT case 1 failing. Note it in your
results, but also email the author so we can unblock you for the
remaining cases.

## A note on data

You're testing on a real production deployment with a UAT-only org.
Anything you create (templates, products, tags) will be wiped after
the UAT cycle ends. Don't worry about cleaning up.

You **can't** see other testers' data. You can't break their cases.
You're isolated.

You **can't** affect real customers. The UAT org is sandboxed.
