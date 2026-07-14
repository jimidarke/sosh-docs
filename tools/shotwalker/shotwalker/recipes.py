"""The recipe registry.

A recipe knows how to reach one screenshot: which URL, what to click to reveal
the element, and which locator to shoot. Recipes are keyed by the same target
filename the docs use, so the manifest and the registry can be diffed directly
-- that diff is what tells us which shots nobody has taught the walker to take.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

Recipe = Callable[..., None]


@dataclass(frozen=True)
class RegisteredRecipe:
    target: str
    surface: str
    fn: Recipe


_REGISTRY: dict[str, RegisteredRecipe] = {}


def recipe(target: str, surface: str) -> Callable[[Recipe], Recipe]:
    """Register `fn` as the way to capture `target`."""

    def decorate(fn: Recipe) -> Recipe:
        if target in _REGISTRY:
            raise ValueError(f"duplicate recipe for {target}")
        _REGISTRY[target] = RegisteredRecipe(target=target, surface=surface, fn=fn)
        return fn

    return decorate


def all_recipes() -> dict[str, RegisteredRecipe]:
    # Import for side effects: the decorators populate the registry.
    from . import walk_app, walk_console, walk_designer  # noqa: F401

    return dict(_REGISTRY)


def for_surface(surface: str) -> dict[str, RegisteredRecipe]:
    return {t: r for t, r in all_recipes().items() if r.surface == surface}
