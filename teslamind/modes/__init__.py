"""Convenience helpers for TeslaMind prompt modes."""

from __future__ import annotations

from .catalog import Mode, get_mode, list_modes


def energy_prompt(task: str) -> str:
    """Render ``task`` in the built-in energy mode."""

    return get_mode("energy").apply(task)


def patent_prompt(task: str) -> str:
    """Render ``task`` in the patent tone."""

    return get_mode("patent").apply(task)


def invention_prompt(task: str) -> str:
    """Render ``task`` in the invention ideation style."""

    return get_mode("invention").apply(task)


def visionary_prompt(task: str) -> str:
    """Render ``task`` in the visionary storytelling style."""

    return get_mode("visionary").apply(task)


def hyperscience_prompt(task: str) -> str:
    """Render ``task`` in the hyperscience exposition style."""

    return get_mode("hyperscience").apply(task)


def coop_prompt(task: str) -> str:
    """Render ``task`` in the cooperative facilitation style."""

    return get_mode("coop").apply(task)


__all__ = [
    "Mode",
    "list_modes",
    "get_mode",
    "energy_prompt",
    "patent_prompt",
    "invention_prompt",
    "visionary_prompt",
    "hyperscience_prompt",
    "coop_prompt",
]

