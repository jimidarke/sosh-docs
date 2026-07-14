# Shotwalker

Walks the Commander console and the Template Designer in a headless browser,
screenshots what the docs ask for, and reports on what it found.

Run it after a big Commander change. One pass gives you three things:

1. **Refreshed doc images** — the screenshots this site references, re-taken.
2. **A health report** — every page visited and checked: no 5xx, no JS
   exceptions, no broken images.
3. **A coverage table** — which images the docs still want and don't have.

## The idea

The docs already say which screenshots they need. Every page that wants one
carries a placeholder naming the exact file and describing the shot:

```markdown
!!! screenshot "Screenshot: the Dashboard right after first sign-in, full page,
    with the Cloud pill and the Access Points tile highlighted"
    To capture: assets/console/dashboard-first-signin.png
```

Shotwalker reads those placeholders as its work list, and each one is answered by
a **recipe** keyed to the same filename — which URL to open, what to click to
reveal the thing, which element to shoot. Because both sides are keyed by the
same name, they can be diffed on every run:

- **gap** — the docs want a shot nobody wrote a recipe for
- **stale** — a recipe no doc asks for any more; delete it
- **held** — captured, but deliberately not published (see *Known issues*)
- **blocked** — no recipe is *possible*, and the reason is recorded

That diff is what keeps this honest as the docs and the UI drift apart.

Blocked is separate from gap on purpose. A gap is a to-do; a blocked shot is one that
cannot be taken at all — its subject is a masked secret, or reaching it needs a write.
Rolling them together would put permanent entries on a list that is supposed to shrink
to zero, and a to-do list that can never reach zero stops being read. It would also
quietly invite the fix of last resort, which is to widen the guard until the shot
works. The guard does not move for a screenshot.

## Use

Configure the target first. **Nothing is defaulted in source** — this repo is
public, and an appliance address or console password committed here would be on
the internet:

```bash
cp tools/shotwalker/shotwalker.env.example tools/shotwalker/shotwalker.env
$EDITOR tools/shotwalker/shotwalker.env     # gitignored
```

Then:

```bash
pip install -r tools/shotwalker/requirements.txt
playwright install chromium
export PYTHONPATH=tools/shotwalker

python -m shotwalker --check          # coverage. No browser, no device. Start here.
python -m shotwalker --all            # walk both surfaces, publish into docs/assets/
python -m shotwalker --surface console
python -m shotwalker --smoke-only     # health checks only, capture nothing
python -m shotwalker --only assets/designer/icon-picker.png   # re-shoot just one
python -m shotwalker --wire           # turn fulfilled placeholders into ![](...) refs
```

Exits non-zero if a page is unhealthy or a shot fails, so it drops into CI
unchanged the day there is one.

## Three surfaces

The Commander console and the Template Designer are **separate applications** on
separate ports. The Designer is what the `owners/templates/` lessons document —
easy to miss, and it is the larger half of the browser shot list. Only the console
requires a sign-in.

The console renders its tables client-side, fetching them after page load, so
`curl` sees an empty shell. A real browser isn't a convenience here; it's the
only thing that works.

The third surface is the **staff handheld**, driven over adb (`adb.py`, `walk_app.py`).
No browser can see an Android app, which is why the `assets/app/*` shots sat as
placeholders while both web surfaces were fully automated. Nodes are located by text
out of `uiautomator dump` — never by coordinate, which works right up until someone
moves a button and the walker starts silently photographing the wrong thing. Callouts
are drawn onto the bitmap, since there is no DOM to hang an outline on.

Two things about the handheld that will cost you an hour otherwise: `adb shell input
text` does nothing (the app draws its own Compose keypad, so the keys must be tapped),
and every "scan the tag" step in the docs has a type-it-in path behind the same field
— which is why these shots can be taken on a bench with no scanner attached.

```bash
python -m shotwalker --surface app     # needs the phone on USB, adb authorised
```

## It cannot change the Commander

The two **browser** surfaces are **reveal-only**: they will open a modal, switch a tab,
expand a panel, draw an object on an unsaved canvas. They will not save, delete, push
to a tag, or restore a backup. Two independent guards enforce that, in `guard.py`:

- **Network** — every non-GET request is aborted unless it's on a short
  allowlist of endpoints that compute something and write nothing (the preview
  renderer, the pairing-QR mint the page fires on load). This one is airtight:
  whatever gets clicked, no mutation reaches the Commander.
- **DOM** — a capture-phase click listener swallows clicks on known mutating
  controls, so a mis-aimed recipe fails loudly instead of quietly half-submitting
  a form.

It's safe to point at any Commander, including a customer's.

### The handheld is the exception, and it is not a small one

**`--surface app` writes.** It cannot not: the lessons it illustrates *are* writes —
saving a multi-product grid onto a shelf tag, putting a customer's name on a pickup
sign, releasing it again. `guard.py` guards the browser; it does nothing over adb.

So the reveal-only guarantee covers the console and the Designer, and stops there. The
app walk is a **bench tool**, and pointing it at a store's handheld would rebind real
tags. The recipes are careful where they can be — `multi-product-convert-confirm` opens
the "Replace existing binding?" dialog and then *cancels* it, because confirming is the
exact accident the lesson warns readers about, and `willcall-assign-order` releases what
it assigned so a run leaves the bench as it found it — but careful is not the same as
guarded, and the difference is the whole point of the paragraph above.

Its screenshots need their own privacy pass, too: `redact.app_masks` blanks the store
UUID the app prints, matched on the node's text rather than a selector.

## It cannot leak into the docs

Secrets are masked *at capture time*, before the PNG is encoded, so they never
exist in a file on disk — not even briefly. Two classes get blacked out:

- **Credentials** — PINs, API keys, POS passwords, the licence lease.
- **Infrastructure** — the appliance's own LAN address and internal API path
  (the POS page prints them in a "Base URL" box), and customer database
  hostnames.

The second class is not hypothetical. The first `pos-config-tabs.png` shipped the
appliance's LAN IP straight into a public doc image before this masking existed.
`redact.py` is the register; add to it before adding a shot of a page that
displays anything an outsider shouldn't have.

## Determinism

Re-runs are comparable, or the images would churn for no reason. The clock is
frozen, polling intervals are neutered, animations are off, fonts are awaited,
and the viewport is pinned at 1440×900.

23 of 25 shots come out byte-identical across consecutive runs. The two that
don't, can't:

- `mobile-devices-pairing-qr.png` — the QR *is* a freshly minted token; a new one
  is generated on every page load, so the pixels change by design.
- `tags-search-and-size-chips.png` — shows live fleet state, which moves as tags
  report in.

## Known issues

`known_issues.py` is the register. Shots listed as `HELD` are captured into
`artifacts/` but never published, because a known-bad image baked into permanent
documentation is worse than a placeholder that tells the truth. Currently three
Templates-page shots are held on a black-on-black dropdown bug in `sosh`.

Re-shoot with `--only <target>` once a blocker is fixed, then `--wire`.

## Output

- `docs/assets/console/`, `docs/assets/designer/` — the published doc images.
  **Committed.**
- `artifacts/<run>/` — full-page baseline of every page, `report.md`,
  `manifest.json` (stamped with the Commander bundle version, which is what
  actually determines the pixels). **Gitignored.**
