# Docs CI: auto-deploy on release tags

**Date:** 2026-07-14
**Status:** Approved

## Problem

There is no CI in this repo. The public site is published only when someone runs
`mkdocs gh-deploy` by hand, which has two consequences we have already felt:

- **The published site drifts from `main`.** Nothing watches the branch, so
  `gh-pages` trails whatever commit the last manual deploy happened to run from.
- **`strict: true` failures surface late.** `mkdocs.yml` sets `strict: true`, so a
  broken link or a bad nav entry fails the build. Today that is discovered at deploy
  time — the worst possible moment — rather than when the offending commit lands.

## Goal

Publish the public site automatically, but only on deliberate releases: a pushed tag
in `major.minor.release` form whose release component is `0` (`v0.6.0`, `v1.0.0`).
Patch tags such as `v0.6.1` must not deploy.

## Design

One workflow file, `.github/workflows/docs.yml`, with two jobs.

### `build`

Runs on every push to `main` and every pull request.

Checks out, installs Python 3.12 (matching the local `.venv`), installs
`requirements.txt` with pip caching, and runs `mkdocs build --strict`. It never
deploys. Its only job is to fail fast on the strict-mode errors described above.

### `deploy`

Runs only when a tag matching `v*.*.0` is pushed, and declares `needs: build`.

That dependency is load-bearing: the strict build is not merely an advisory check on
`main`, it is the gate the release itself must clear. A tag cannot reach production
without a passing strict build.

The job checks out with full history (`gh-deploy` needs it to commit onto the
`gh-pages` branch), sets a `github-actions[bot]` git identity, and runs
`mkdocs gh-deploy --force`.

## Why `gh-deploy` and not the Pages Actions artifact

GitHub Pages for this repo is currently `build_type: "legacy"`, serving from the
`gh-pages` branch, and the Let's Encrypt certificate for `docs.sovereignshelf.net`
is mid-provisioning (API reports `https_certificate.state: "new"`).

Deploying via `actions/deploy-pages` would flip the Pages source to `"workflow"`,
which risks resetting that in-flight certificate request. `mkdocs gh-deploy` instead
just pushes a commit to `gh-pages` — exactly what we do by hand today. Pages settings
are never touched.

`CNAME` survives automatically: it lives at `docs/CNAME`, inside `docs_dir`, so every
build copies it into `site/`. This is already how the published `CNAME` got there.

## Permissions and concurrency

The `deploy` job needs `contents: write` to push the branch, using the default
`GITHUB_TOKEN`. No secrets to create.

A `concurrency` group prevents overlapping deploys, so two tags pushed back to back
cannot race each other onto `gh-pages`.

## Out of scope

- **The Commander help pack.** `mkdocs.commander.yml` builds an offline pack that is
  packaged and Ed25519-signed for Guardians. Keeping it out of CI keeps the private
  signing key off GitHub. It stays a manual build.
- **Migrating the Pages source** to the workflow build type.
- **Version-consistency and tag-shape guards.** Considered and explicitly declined.
  Note the consequence: GitHub's tag glob treats `*` as matching any character except
  `/`, dots included, so a tag shaped like `v1.0.0-rc.0` would also match `v*.*.0` and
  trigger a deploy. This is accepted on the grounds that we do not cut tags in that
  shape.
