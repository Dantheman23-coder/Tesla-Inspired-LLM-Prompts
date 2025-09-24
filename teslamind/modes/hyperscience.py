"""Hyperscience mode."""

from .catalog import get_mode


def hyperscience_prompt(task: str) -> str:
    """Compatibility wrapper matching :func:`teslamind.modes.hyperscience_prompt`."""

    return get_mode("hyperscience").apply(task)
