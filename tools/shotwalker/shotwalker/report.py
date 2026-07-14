"""What the run found: coverage, health, and what's still missing.

Coverage is a three-way diff between what the docs ask for (the manifest), what
the walker knows how to take (the recipe registry), and what actually landed on
disk. Each disagreement means something different and gets its own name:

  gap      the docs want a shot nobody has written a recipe for
  stale    a recipe whose target no longer appears in any doc -- delete it
  failed   a recipe that ran and produced nothing
  held     captured, but withheld from the docs on purpose (a known UI bug)
  blocked  no recipe is *possible* -- the shot's subject is a masked secret, or
           reaching it would need a write. Distinct from a gap on purpose: a gap
           is a to-do, and a to-do list that can never reach zero stops being read.

Keeping those distinct is the point. "27 of 29" tells you nothing; "2 gaps, 0
stale, 0 failed" tells you exactly what to do next.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from . import config, known_issues, manifest
from .capture import ShotResult
from .smoke import PageHealth


def _git_sha() -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(config.REPO_ROOT), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return "unknown"


def coverage(specs: list[manifest.ShotSpec], recipe_targets: set[str]) -> dict:
    """The three-way diff. Needs no browser and no device.

    "What the docs want" is both the open placeholders *and* the images already
    wired in -- a fulfilled shot is still wanted, it's just no longer missing.
    """
    open_specs = manifest.capturable(specs)
    pending = {s.target for s in open_specs}
    live = {
        t
        for t in manifest.referenced()
        if t.split("/")[1] in manifest.AUTOMATABLE_SURFACES
    }
    wanted = pending | live

    # A blocked shot has no recipe and never will, so it is not a gap. Subtracting
    # it keeps `gaps` meaning "write this recipe" -- the number that should reach
    # zero -- instead of a list with a permanent floor in it.
    blocked = {t for t in wanted if known_issues.is_blocked(t)}

    return {
        "placeholders_open": len(specs),
        "wired": sorted(live),
        "hardware_only": [s.target for s in specs if s.surface == "hardware"],
        "capturable": sorted(wanted),
        "covered": sorted(wanted & recipe_targets),
        "pending": sorted(pending),
        "gaps": sorted(wanted - recipe_targets - blocked),
        "blocked": sorted(blocked),
        "stale": sorted(recipe_targets - wanted),
        "held": sorted(t for t in wanted if known_issues.is_held(t)),
        "orphans": [f"{p}:{ln}" for p, ln in manifest.orphans()],
    }


def write(
    out_dir: Path,
    *,
    cov: dict,
    shots: list[ShotResult],
    health: list[PageHealth],
    commander_version: str = "unknown",
    blocked_requests: list[str] | None = None,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    blocked_requests = blocked_requests or []
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    published = [s for s in shots if s.ok and not s.held]
    held = [s for s in shots if s.held]
    failed = [s for s in shots if not s.ok]
    unhealthy = [h for h in health if not h.ok]

    (out_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_at": stamp,
                "commander_version": commander_version,
                "docs_git_sha": _git_sha(),
                "console_url": config.console_url(),
                "designer_url": config.designer_url(),
                "coverage": cov,
                "shots": [asdict(s) | {"path": str(s.path)} for s in shots],
                "pages": [asdict(h) for h in health],
                "blocked_requests": blocked_requests,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    L: list[str] = []
    L.append("# Shotwalker run\n")
    L.append(f"- **When:** {stamp}")
    L.append(f"- **Commander build:** `{commander_version}`")
    L.append(f"- **Docs commit:** `{_git_sha()}`")
    L.append(f"- **Console:** {config.console_url()}")
    L.append(f"- **Designer:** {config.designer_url()}\n")

    L.append("## Health\n")
    if health:
        passed = len(health) - len(unhealthy)
        L.append(f"**{passed}/{len(health)} pages healthy.**\n")
        L.append("| Page | URL | Result |")
        L.append("| --- | --- | --- |")
        for h in sorted(health, key=lambda x: x.ok):
            mark = "ok" if h.ok else "**FAIL**"
            L.append(f"| {h.label} | `{h.url}` | {mark} — {h.summary()} |")
        L.append("")
        for h in unhealthy:
            L.append(f"### {h.label} — {h.url}\n")
            for e in h.page_errors:
                L.append(f"- JS exception: `{e}`")
            for e in h.console_errors:
                L.append(f"- console error: `{e}`")
            for e in h.failed_requests:
                L.append(f"- failed request: `{e}`")
            for e in h.broken_images:
                L.append(f"- broken image: `{e}`")
            L.append("")

        media = [h for h in health if h.missing_media]
        if media:
            L.append("### Unrendered images (not failures)\n")
            L.append(
                "Tags that have never been pushed have no rendered image, and "
                "templates without a thumbnail have none; the console requests "
                "them anyway, 404s, and draws a broken `<img>`. Real device "
                "state, reproducible with curl outside this harness — not a "
                "regression. Arguably the console should show a placeholder.\n"
            )
            for h in media:
                L.append(f"- **{h.label}** — {len(h.missing_media)} unrendered")
            L.append("")
    else:
        L.append("_No pages swept._\n")

    L.append("## Screenshot coverage\n")
    L.append(f"- Shots the docs want: **{len(cov['capturable'])}**")
    L.append(f"- Already wired into a page: **{len(cov['wired'])}**")
    L.append(f"- Still open placeholders: **{len(cov['pending'])}**")
    L.append(f"- Covered by a recipe: **{len(cov['covered'])}**")
    L.append(f"- Published this run: **{len(published)}**")
    L.append(f"- Held (known UI bug): **{len(held)}**")
    L.append(f"- Failed: **{len(failed)}**")
    L.append(f"- Gaps (no recipe): **{len(cov['gaps'])}**")
    L.append(f"- Blocked (no recipe possible): **{len(cov['blocked'])}**")
    L.append(f"- Stale (recipe, no placeholder): **{len(cov['stale'])}**")
    L.append(f"- Hardware photos (not automatable): **{len(cov['hardware_only'])}**\n")

    if cov["gaps"]:
        L.append("### Gaps — the docs ask for these, no recipe exists\n")
        for t in cov["gaps"]:
            L.append(f"- `{t}`")
        L.append("")
    if cov["blocked"]:
        L.append("### Blocked — no recipe is possible\n")
        L.append(
            "The docs ask for these and always will, but the walker cannot take them: "
            "the subject is a masked secret, or reaching it needs a write. They are "
            "listed apart from gaps so the gap list stays a to-do list. Re-spec the "
            "placeholder, or shoot it by hand.\n"
        )
        for t in cov["blocked"]:
            L.append(f"- `{t}` — {known_issues.blocked_reason(t)}")
        L.append("")
    if cov["stale"]:
        L.append("### Stale — recipe exists, no doc asks for it\n")
        for t in cov["stale"]:
            L.append(f"- `{t}`")
        L.append("")
    if failed:
        L.append("### Failed\n")
        for s in failed:
            L.append(f"- `{s.target}` — {s.error}")
        L.append("")
    if held:
        L.append("### Held back from the docs\n")
        L.append(
            "Captured into this run's artifacts, but deliberately not published. "
            "A known-bad image in permanent docs is worse than a placeholder that "
            "tells the truth. Re-shoot with `--only <target>` once fixed.\n"
        )
        for s in held:
            L.append(f"- `{s.target}` — {s.note}")
        L.append("")

    L.append("## Known UI defects\n")
    for t, why in known_issues.HELD.items():
        L.append(f"- **`{t}`** — {why}")
    for note in known_issues.NOTED:
        L.append(f"- {note}")
    L.append("")

    if blocked_requests:
        L.append("## Blocked by the guard\n")
        L.append(
            "Reveal-only: these non-GET requests were aborted before reaching the "
            "device. Anything here means a recipe touched a control it shouldn't "
            "have.\n"
        )
        for r in sorted(set(blocked_requests)):
            L.append(f"- `{r}`")
        L.append("")

    path = out_dir / "report.md"
    path.write_text("\n".join(L), encoding="utf-8")
    return path


def print_check(cov: dict) -> None:
    """The --check summary: coverage without touching a browser."""
    print(f"shots the docs want  : {len(cov['capturable'])}")
    print(f"  already wired in   : {len(cov['wired'])}")
    print(f"  still placeholders : {len(cov['pending'])}")
    print(f"covered by a recipe  : {len(cov['covered'])}")
    print(f"hardware photos      : {len(cov['hardware_only'])}")
    print(f"gaps                 : {len(cov['gaps'])}")
    print(f"blocked (can't shoot): {len(cov['blocked'])}")
    print(f"stale                : {len(cov['stale'])}")
    print(f"held (known UI bug)  : {len(cov['held'])}")
    print(f"orphan placeholders  : {len(cov['orphans'])}")

    if cov["gaps"]:
        print("\nGAPS — docs ask for these, no recipe:")
        for t in cov["gaps"]:
            print(f"  {t}")
    if cov["blocked"]:
        print("\nBLOCKED — no recipe is possible; re-spec or hand-shoot:")
        for t in cov["blocked"]:
            print(f"  {t}")
            print(f"      {known_issues.blocked_reason(t).split(' -- ')[0]}")
    if cov["stale"]:
        print("\nSTALE — recipe exists, no doc asks for it:")
        for t in cov["stale"]:
            print(f"  {t}")
    if cov["orphans"]:
        print("\nORPHANS — '!!! screenshot' with no 'To capture:' line, so no")
        print("file is named and nothing can ever fulfil it:")
        for o in cov["orphans"]:
            print(f"  {o}")
    if not cov["gaps"] and not cov["stale"]:
        print("\nEvery capturable placeholder has a recipe, and no recipe is orphaned.")
        if cov["blocked"]:
            print(
                f"({len(cov['blocked'])} blocked shot(s) remain, by design — "
                "they need a re-spec or a hand-shot, not a recipe.)"
            )
