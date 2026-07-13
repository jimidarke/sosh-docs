---
search:
  exclude: true
---

# Triage (author-facing)

Volunteers don't need to read this. It's the author's process for
turning their results into a punch list.

## Inbox

Each tester sends back `results-<name>.md`. Drop them all in a
working folder for the cycle. Leave them unmodified — they're the
audit trail.

## First pass: classify each Fail

For every `Fail` across all results, label it as one of:

| Label              | Meaning                                                     | Action                                          |
| ------------------ | ----------------------------------------------------------- | ----------------------------------------------- |
| **defect**         | Code does not deliver the documented behaviour              | File an issue, fix in the next sprint           |
| **ux-gap**         | Code works but tester was confused, lost, or surprised      | UX/copy/affordance ticket; often quick fixes    |
| **docs-gap**       | The case itself was unclear; tester was set up to fail      | Reword the case before the next UAT cycle       |
| **out-of-scope**   | Tester hit something we don't promise                       | Note for product roadmap, not for this cycle    |
| **environment**    | Tester's setup was wrong (wrong creds, network down, etc.)  | Fix setup-tester.md, don't blame the product    |

## Severity (after classification)

For everything labelled `defect` or `ux-gap`, assign S1–S4 from the
[strategy.md](strategy.md) rubric. **A case fails UAT only if ≥2
testers independently fail it.** A single fail is suspicious — could
be the case wording, could be a real bug — investigate but don't
over-react.

## Triage output

For each cycle, produce a single short markdown summary:

```
## UAT cycle YYYY-MM-DD

Testers: 4 (3 cloud, 1 kit)
Cases run: 52
Pass rate: NN/52 average

### S1 (must fix before <milestone>)
- UAT-CLD-27: price doesn't propagate when bound product is multi-slot

### S2
- UAT-CLD-29: bulk CSV import silently truncates 8th column

### S3 (UX papercuts)
- ...

### Re-worded for next cycle (docs-gap)
- ...

### Thanks-and-here's-what-we-found-back to testers
- short paragraph, sent within 1 week
```

Triage issues feed the normal sprint backlog.

## What not to do

- Don't dismiss a Fail because "it works on my machine." That's the
  whole point of running UAT.
- Don't add cases mid-cycle. Note them for the next cycle.
- Don't ask testers to retry. They already did the work.
