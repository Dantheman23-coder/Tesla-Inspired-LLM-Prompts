"""Patent mode."""

from .catalog import get_mode


def patent_prompt(task: str) -> str:
    """Compatibility wrapper that mirrors :func:`teslamind.modes.patent_prompt`."""

    return get_mode("patent").apply(task)
