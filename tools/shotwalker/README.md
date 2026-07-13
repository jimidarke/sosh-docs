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

That diff is what keeps this honest as the docs and the UI drift apart.

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

## Two surfaces

The Commander console and the Template Designer are **separate applications** on
separate ports. The Designer is what the `owners/templates/` lessons document —
easy to miss, and it is the larger half of the shot list (21 shots to the
console's 8). Only the console requires a sign-in.

The console renders its tables client-side, fetching them after page load, so
`curl` sees an empty shell. A real browser isn't a convenience here; it's the
only thing that works.

## It cannot change the device

Shotwalker is **reveal-only**: it will open a modal, switch a tab, expand a
panel, draw an object on an unsaved canvas. It will not save, delete, push to a
tag, or restore a backup. Two independent guards enforce that, in `guard.py`:

- **Network** — every non-GET request is aborted unless it's on a short
  allowlist of endpoints that compute something and write nothing (the preview
  renderer, the pairing-QR mint the page fires on load). This one is airtight:
  whatever gets clicked, no mutation reaches the Commander.
- **DOM** — a capture-phase click listener swallows clicks on known mutating
  controls, so a mis-aimed recipe fails loudly instead of quietly half-submitting
  a form.

It's safe to point at any Commander, including a customer's.

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
