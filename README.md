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
2. Write the page. Add screenshots to `docs/assets/<page-slug>/`.
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
