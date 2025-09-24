"""Visionary mode."""

from .catalog import get_mode


def visionary_prompt(task: str) -> str:
    """Compatibility wrapper mirroring :func:`teslamind.modes.visionary_prompt`."""

    return get_mode("visionary").apply(task)
