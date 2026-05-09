---
search:
  exclude: true
---

# User Acceptance Testing (UAT)

This is the volunteer-tester pack for Sosh. It is written for friends and
family who are willing to push every button and tell us what broke or
confused them. They are not engineers. The docs assume nothing.

## Read in this order

1. **[strategy.md](strategy.md)** — what we're testing, why, how results
   come back. Read this once, before you start.
2. **[setup-tester.md](setup-tester.md)** — what each tester needs before
   case 1: account, URLs, app install, hardware they happen to have.
3. **[test-script.md](test-script.md)** — the actual cases. ~50 of them,
   numbered, with steps and expected results.
4. **[result-template.md](result-template.md)** — copy this, fill in your
   results as you go, send it back when done.
5. **[triage.md](triage.md)** — what happens to your results after you
   send them. Mostly for the author; testers don't need to read it.

## Tester tiers

- **`[CLOUD]`** — anyone with a browser. Most of the test pack.
- **`[MOBILE]`** — has an Android phone, willing to install our APK.
- **`[KIT]`** — has a physical Guardian kit (Commander, beacon, tags).
  A handful of testers, max.

Each case is tagged. Skip the ones you can't run; mark them `N-A` and
move on. Don't break a case just because the previous one failed —
treat them as independent.

## Tip — sortable tables

The index at the top of [test-script.md](test-script.md) and the grid
in [result-template.md](result-template.md) are both **sortable** —
click any column header to sort, click again to reverse. Sort by
**Tier** to group all cases relevant to your kit.
