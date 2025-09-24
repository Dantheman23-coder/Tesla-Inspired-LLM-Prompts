"""Invention mode."""

from .catalog import get_mode


def invention_prompt(task: str) -> str:
    """Compatibility wrapper that mirrors :func:`teslamind.modes.invention_prompt`."""

    return get_mode("invention").apply(task)
