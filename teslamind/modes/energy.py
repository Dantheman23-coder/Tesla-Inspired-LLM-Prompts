"""Energy mode prompts."""

from .catalog import get_mode


def energy_prompt(task: str) -> str:
    """Compatibility wrapper that mirrors :func:`teslamind.modes.energy_prompt`."""

    return get_mode("energy").apply(task)
