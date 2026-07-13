# sosh-docs — Sovereign Shelf user documentation

Source for the public help site at **https://docs.sovereignshelf.net**.

## ⚠️ This repo is PUBLIC

Anything committed to `main` is one `mkdocs gh-deploy` away from being live on the public internet. Treat every file as if a competitor will read it tomorrow.

Keep out: internal service/system names, infrastructure or network details, auth/security internals (env vars, tokens, signing), internal codenames, pricing/partner/customer specifics, vendor part numbers, database schema, and staff or internal-tool references. Use product-facing names only.

If unsure, don't commit it. Internal architecture lives in the private `sosh` repo's `docs/` folder, not here.

### Voice & audience

Retail store owners. Plain language. Click-here / click-there. Screenshots over prose. No jargon. No algorithms. Nobody reading this site cares how it works internally — only what to do.

## Workflow

### Author a page (draft)

1. Create the file under `docs/drafts/<section>/<page>.md`. Files in `docs/drafts/` are excluded from production builds (configured in `mkdocs.yml` via `draft_docs`).
2. Write the page. Add screenshots to `docs/assets/<surface>/`, where `<surface>` is the thing being shown — `app/` (the handheld), `console/` (the Guardian console), `designer/` (the Template Designer), or `hardware/` (photos of the kit). Reference them with a **relative** path (`../assets/app/foo.png`); `strict: true` then fails the build on a typo, whereas an absolute `/assets/...` path silently ships broken.
3. Commit + push to `main`. **Drafts on main are safe** — they don't ship to the live site.

### Review locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open http://localhost:8000 — drafts ARE shown when serving locally (with a "DRAFT" indicator). Iterate until happy.

### Approve & publish

1. **Move** the file out of `docs/drafts/` to its real location (e.g. `docs/drafts/getting-started/binding-a-tag.md` → `docs/getting-started/binding-a-tag.md`). The move IS the approval gate.
2. Update `nav:` in `mkdocs.yml` to include the new page.
3. Run `mkdocs build --strict` locally to catch broken links.
4. Commit + push to `main`.
5. Run `mkdocs gh-deploy` — this builds the site and force-pushes to the `gh-pages` branch. GitHub Pages serves it within ~30s.

### Rollback

```bash
git revert <bad-commit>
mkdocs gh-deploy
```

## Screenshots

Screenshots of the Commander console and the Template Designer are **generated**,
not taken by hand. `tools/shotwalker/` drives both in a headless browser, captures
the images, and smoke-tests every page on the way through. Run it after a big
Commander change:

```bash
cp tools/shotwalker/shotwalker.env.example tools/shotwalker/shotwalker.env
$EDITOR tools/shotwalker/shotwalker.env     # target + sign-in; gitignored

pip install -r tools/shotwalker/requirements.txt && playwright install chromium
export PYTHONPATH=tools/shotwalker

python -m shotwalker --check   # what's missing. No browser, no device needed.
python -m shotwalker --all     # walk both surfaces, write into docs/assets/
python -m shotwalker --wire    # turn fulfilled placeholders into ![](...) refs
```

Full detail in [`tools/shotwalker/README.md`](tools/shotwalker/README.md).

### Asking for a screenshot

**The docs are the shot list.** When a page needs an image that doesn't exist yet,
leave a placeholder naming the exact file and describing the shot — including what
to outline:

```markdown
!!! screenshot "Screenshot: the Dashboard right after first sign-in, full page,
    with the Cloud pill and the Access Points tile highlighted"
    To capture: assets/console/dashboard-first-signin.png
```

Shotwalker reads every placeholder as its work list, and each is answered by a
*recipe* keyed to the same filename. Because both sides use the same key, they get
diffed on every run: a placeholder with no recipe is a **gap**, a recipe no page
asks for any more is **stale**. `--check` prints both. That diff is what stops the
images and the docs from quietly drifting apart.

So: write the placeholder first. Someone (or you) adds the recipe in
`walk_console.py` / `walk_designer.py`, and `--wire` swaps the placeholder for the
picture. Callout outlines are drawn at capture time from the art direction, which
is why the placeholder should say what to highlight.

A placeholder that survives a run is *telling the truth* about a missing image.
That's the point — some shots are deliberately withheld (a UI bug would bake a
known-bad picture into permanent docs; a card is empty on the test appliance).
`known_issues.py` records why, and the run report lists them.

### Screenshots and the privacy gate

The masking in `tools/shotwalker/shotwalker/redact.py` is part of the ⚠️ **PUBLIC
repo** rule at the top of this file, not a nicety. A screenshot is a verbatim copy
of a screen, and the console screens show things this repo must not carry:
credentials (PINs, API keys, POS passwords) and infrastructure (the appliance's LAN
address and internal API path, customer database hostnames). Those regions are
blacked out *before the image is encoded*, so they never touch disk.

This has already bitten once: the first POS screenshot shipped the appliance's LAN
IP into a public doc image. **Before adding a shot of a page that shows anything an
outsider shouldn't have, add its selector to `redact.py`** — and look at the PNG
afterwards. The same rule applies to a screenshot you take by hand.

## Verifying the privacy gate

```bash
# A file in docs/drafts/ should NOT appear in build output:
mkdocs build --strict
ls site/drafts/    # → No such file or directory ✓
```

If `site/drafts/` exists after a build, the draft gate is broken — STOP and fix `mkdocs.yml` `draft_docs` config before publishing.

## Hosting

- DNS: `docs.sovereignshelf.net` CNAME → `jimidarke.github.io`
- GitHub Pages serves from the `gh-pages` branch of this repo
- HTTPS handled by GitHub Pages (Let's Encrypt, free, auto-renewing)
