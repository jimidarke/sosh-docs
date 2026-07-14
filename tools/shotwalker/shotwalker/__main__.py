"""Shotwalker CLI.

    python -m shotwalker --check                    coverage only, no browser
    python -m shotwalker --all                      both surfaces
    python -m shotwalker --surface console          one surface
    python -m shotwalker --only <target.png>        re-shoot a single image
    python -m shotwalker --smoke-only               test, capture nothing

Exits non-zero when a page is unhealthy or a shot fails, so it can be dropped
into CI unchanged the day there is one.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import capture, config, guard, known_issues, manifest, recipes, report, session
from .capture import ShotResult
from .smoke import PageHealth, visit


def _run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def _sweep_console(page, run_dir: Path) -> tuple[list[PageHealth], str]:
    """Enumerate the nav live, then visit and check every page it names."""
    from .walk_console import HIDDEN_ROUTES, commander_version, enumerate_nav, url

    nav = enumerate_nav(page)
    print(f"  discovered {len(nav)} nav links")

    version = commander_version(page)
    print(f"  Commander build {version}")

    targets = [(n.label, n.href, n.slug) for n in nav]
    targets += [
        (label, href, href.strip("/").replace("/", "-")) for label, href in HIDDEN_ROUTES
    ]

    health: list[PageHealth] = []
    baselines = run_dir / "baseline" / "console"

    for label, href, slug in targets:
        h = visit(page, url(href), label)
        health.append(h)
        mark = "ok " if h.ok else "FAIL"
        print(f"  [{mark}] {label:<22} {href:<24} {h.summary()}")
        try:
            capture.baseline(page, baselines, slug, path_hint=href)
        except Exception as exc:
            print(f"         (baseline capture failed: {exc})")

    return health, version


def _out_dir(target: str, run_dir: Path, publish: bool) -> Path:
    held = known_issues.is_held(target)
    return (
        config.DOCS_DIR / Path(target).parent
        if publish and not held
        else run_dir / "held"
    )


def _shoot_app(device, reg, run_dir: Path, publish: bool) -> ShotResult:
    """Run one handheld recipe. No guards apply here -- see adb.py."""
    out_dir = _out_dir(reg.target, run_dir, publish)
    shooter = capture.AppShooter(device, reg.target, out_dir)
    try:
        reg.fn(device, shooter)
    except Exception as exc:
        return ShotResult(reg.target, out_dir / Path(reg.target).name, ok=False, error=str(exc))

    result = shooter.result
    if result is None:
        return ShotResult(
            reg.target,
            out_dir / Path(reg.target).name,
            ok=False,
            error="recipe never called shoot()",
        )
    if known_issues.is_held(reg.target):
        result.held = True
        result.note = known_issues.reason(reg.target)
    return result


def _shoot(page, reg, run_dir: Path, publish: bool) -> ShotResult:
    """Run one recipe. Held shots land in artifacts only, never in docs/."""
    held = known_issues.is_held(reg.target)
    out_dir = _out_dir(reg.target, run_dir, publish)

    shooter = capture.Shooter(page, reg.target, out_dir)
    try:
        reg.fn(page, shooter)
    except Exception as exc:
        return ShotResult(reg.target, out_dir / Path(reg.target).name, ok=False, error=str(exc))

    result = shooter.result
    if result is None:
        return ShotResult(
            reg.target,
            out_dir / Path(reg.target).name,
            ok=False,
            error="recipe never called shoot()",
        )

    result.blocked_clicks = guard.drain_blocked_clicks(page)
    if held:
        result.held = True
        result.note = known_issues.reason(reg.target)
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="shotwalker")
    p.add_argument("--all", action="store_true", help="walk every surface")
    p.add_argument("--surface", choices=["console", "designer", "app"])
    p.add_argument("--only", metavar="TARGET", help="re-shoot one target, e.g. assets/designer/icon-picker.png")
    p.add_argument("--check", action="store_true", help="coverage report only; no browser")
    p.add_argument("--smoke-only", action="store_true", help="health checks; capture nothing")
    p.add_argument("--no-publish", action="store_true", help="write shots to artifacts/, not docs/")
    p.add_argument(
        "--wire",
        action="store_true",
        help="replace fulfilled `!!! screenshot` placeholders with image refs",
    )
    p.add_argument("--dry-run", action="store_true", help="with --wire: show, don't write")
    args = p.parse_args(argv)

    specs = manifest.load()
    registry = recipes.all_recipes()
    cov = report.coverage(specs, set(registry))

    if args.check:
        report.print_check(cov)
        return 1 if cov["gaps"] or cov["stale"] else 0

    if args.wire:
        from . import wire

        done = wire.run(apply=not args.dry_run)
        verb = "would wire" if args.dry_run else "wired"
        for w in done:
            print(f"  {verb}: {w.target}\n      -> {w.page}")
        remaining = [s for s in manifest.capturable(specs) if not s.exists]
        print(f"\n{verb} {len(done)} image(s); {len(remaining)} placeholder(s) still open")
        for s in remaining:
            print(f"  still open: {s.target}")
        return 0

    if not (args.all or args.surface or args.only or args.smoke_only):
        p.error("pick one of --all, --surface, --only, --smoke-only, or --check")

    run_dir = config.ARTIFACTS_DIR / _run_id()
    run_dir.mkdir(parents=True, exist_ok=True)
    publish = not args.no_publish

    surfaces: list[str] = []
    if args.all:
        surfaces = ["console", "designer", "app"]
    elif args.surface:
        surfaces = [args.surface]
    elif args.only:
        reg = registry.get(args.only)
        if not reg:
            print(f"no recipe for {args.only!r}", file=sys.stderr)
            print("known targets:", file=sys.stderr)
            for t in sorted(registry):
                print(f"  {t}", file=sys.stderr)
            return 2
        surfaces = [reg.surface]
    elif args.smoke_only:
        surfaces = ["console"]

    shots: list[ShotResult] = []
    health: list[PageHealth] = []
    version = "unknown"

    with session.browser() as b:
        if "console" in surfaces:
            print(f"\nConsole — {config.console_url()}")
            with session.page_for(b, authenticated=True) as page:
                if not args.only:
                    health, version = _sweep_console(page, run_dir)

                if not args.smoke_only:
                    todo = (
                        {args.only: registry[args.only]}
                        if args.only
                        else recipes.for_surface("console")
                    )
                    for target, reg in sorted(todo.items()):
                        r = _shoot(page, reg, run_dir, publish)
                        shots.append(r)
                        state = "held" if r.held else ("ok" if r.ok else "FAIL")
                        print(f"  [{state:>4}] {target}" + (f" — {r.error}" if not r.ok else ""))

        if "designer" in surfaces and not args.smoke_only:
            print(f"\nDesigner — {config.designer_url()}")
            with session.page_for(b, authenticated=False) as page:
                todo = (
                    {args.only: registry[args.only]}
                    if args.only
                    else recipes.for_surface("designer")
                )
                for target, reg in sorted(todo.items()):
                    r = _shoot(page, reg, run_dir, publish)
                    shots.append(r)
                    state = "held" if r.held else ("ok" if r.ok else "FAIL")
                    print(f"  [{state:>4}] {target}" + (f" — {r.error}" if not r.ok else ""))

    # The handheld, outside the browser context entirely. A missing phone is not a
    # failed run: the other two surfaces are the ones with a device-independent
    # contract, and a laptop with no phone plugged in should still be able to refresh
    # the console images.
    if "app" in surfaces and not args.smoke_only:
        from . import adb

        todo = (
            {args.only: registry[args.only]}
            if args.only
            else recipes.for_surface("app")
        )
        try:
            device = adb.Device()
        except adb.AdbError as exc:
            print(f"\nHandheld — skipped: {exc}")
            device = None

        if device is not None:
            print(f"\nHandheld — {device.serial}")
            device.wake()
            for target, reg in sorted(todo.items()):
                r = _shoot_app(device, reg, run_dir, publish)
                shots.append(r)
                state = "held" if r.held else ("ok" if r.ok else "FAIL")
                print(f"  [{state:>4}] {target}" + (f" — {r.error}" if not r.ok else ""))

    path = report.write(
        run_dir,
        cov=cov,
        shots=shots,
        health=health,
        commander_version=version,
        blocked_requests=guard.blocked_requests,
    )

    failed = [s for s in shots if not s.ok]
    unhealthy = [h for h in health if not h.ok]
    published = [s for s in shots if s.ok and not s.held]
    held = [s for s in shots if s.held]

    print(f"\n{'-' * 60}")
    print(f"published : {len(published)}")
    print(f"held      : {len(held)}")
    print(f"failed    : {len(failed)}")
    if health:
        print(f"pages ok  : {len(health) - len(unhealthy)}/{len(health)}")
    if guard.blocked_requests:
        print(f"guard     : blocked {len(set(guard.blocked_requests))} write request(s)")
    print(f"report    : {path}")

    return 1 if (failed or unhealthy) else 0


if __name__ == "__main__":
    raise SystemExit(main())
