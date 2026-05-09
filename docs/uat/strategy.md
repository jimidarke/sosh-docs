---
search:
  exclude: true
---

# UAT Strategy

## Why we're doing this

Sosh is at v50. Multi-tenancy is hardened. The product is roughly 85%
complete and a Spire-conference push is coming June 2026. Before more
people see it, every functional promise needs a non-author set of eyes
on it. The author has spent two years staring at this code and is
biased toward "of course it works." Friends and family are not. They
will click the wrong thing in the wrong order, and that is exactly
what we need.

## What "acceptance" means here

Pass means: a normal person, given the documented steps, sees the
documented result, and is not confused along the way. Fail means: they
didn't, or they were. Severity is for the author to assign during
triage — testers only mark Pass / Fail / Blocked / N-A.

This is **not** a substitute for the unit and integration tests in the
codebase. Those check correctness of code. UAT checks correctness of
**experience** — that the product, end-to-end, delivers what the
brochure says it does.

## Out of scope

- Performance and load (separate workstream)
- Security and multi-tenant isolation (already exercised; adversarial
  testing is its own engagement)
- Exotic edge cases ("what if I unplug the phone mid-scan?") — testers
  won't think of them anyway, and we're not building life-support
- Error injection, fuzzing, browser-compat matrices

If you find something weird while running a case, **note it in the
Comments column** and keep going. Don't go hunting.

## Audience tiers

| Tier       | Who runs it                         | What it covers                                        |
| ---------- | ----------------------------------- | ----------------------------------------------------- |
| `[CLOUD]`  | Anyone with a browser               | sovereignshelf.net admin, designer, storefront        |
| `[MOBILE]` | Tester + Android phone + our APK    | Mobile picker / signage / staff roles, QR binding     |
| `[KIT]`    | Tester + full Guardian kit          | Commander :8080 UI, TUI, POS sync, pick-by-light, beacon |

A tester runs every case relevant to **their** tier and skips the rest
(mark `N-A`). Cloud-only testers will run roughly 30 of ~50 cases;
full-kit testers run all of them.

## Coverage and confidence

Target: **3 cloud-only testers + 1 full-kit tester.** A case is
considered to fail UAT if **two or more independent testers fail it**.
A single fail is a flag for the author to investigate and possibly
re-word the case (testers fail because the case is unclear at least as
often as because the code is broken).

## Test environment

A dedicated UAT org/store on production (`sovereignshelf.net`).
Throwaway data. Real platform — what a customer sees on day one.
Pre-seeded with:

- 1 demo store
- ~20 demo products with prices
- 2-3 demo templates already in the designer
- A handful of demo tags already bound (so tag-update cases don't
  require the tester to set up state from scratch)

Each tester gets their own login under that org so their actions
don't collide.

## The lifecycle of a case

1. Tester reads the **Precondition** line. If they don't have what it
   needs, mark `Blocked` and skip.
2. Tester does each numbered step exactly as written.
3. Tester compares what they saw to **Expected**.
4. Tester writes one sentence in **Actual**, marks `Pass` / `Fail` /
   `Blocked` / `N-A`, and adds a **Notes** comment if anything was
   weird, slow, or confusing — even on a pass.
5. No retries. Move on. The author will reproduce failures during
   triage.

## Severity rubric (for the author, after the fact)

| Sev | Meaning                                                | Examples                                                              |
| --- | ------------------------------------------------------ | --------------------------------------------------------------------- |
| S1  | Broken core promise                                    | Price changes in POS but tag never updates; cannot log in             |
| S2  | Broken secondary feature                               | Bulk CSV import fails; designer crashes on a specific widget          |
| S3  | UX papercut                                            | Confusing label, missing confirmation, layout breaks on small screens |
| S4  | Cosmetic                                               | Typo, slightly-off colour, icon misaligned                            |

Volunteers do not assign severity. The author triages every Fail and
assigns one in [triage.md](triage.md).

## What testers get back

Within ~1 week of submitting results, testers receive a short reply:
"Thanks; here's what we found across all testers, here's what we're
fixing, here's what turned out to be an unclear case on our side."
This keeps volunteers engaged for the next round.
