"""Collaboration mode."""

from .catalog import get_mode


def coop_prompt(task: str) -> str:
    """Compatibility wrapper matching :func:`teslamind.modes.coop_prompt`."""

    return get_mode("coop").apply(task)
