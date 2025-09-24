"""Prompt management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .modes import Mode, get_mode
from .persona import Persona, get_persona
from .templates import DEFAULT_TEMPLATE


@dataclass
class Prompt:
    """Represents a prompt template."""

    name: str
    text: str

    @classmethod
    def from_file(cls, path: Path) -> "Prompt":
        return cls(name=path.stem, text=path.read_text())

    def save(self, path: Path) -> None:
        path.write_text(self.text)


def _resolve_mode(mode: Mode | str | None) -> Mode | None:
    if mode is None or isinstance(mode, Mode):
        return mode
    return get_mode(mode)


def _resolve_persona(persona: Persona | str | None) -> Persona | None:
    if persona is None or isinstance(persona, Persona):
        return persona
    return get_persona(persona)


def compose_prompt(
    task: str,
    *,
    mode: Mode | str | None = None,
    persona: Persona | str | None = None,
    template: str | None = None,
    name: str | None = None,
) -> Prompt:
    """Compose a prompt that blends personas, templates, and modes.

    Parameters
    ----------
    task:
        The instruction to render.
    mode:
        Optional :class:`~teslamind.modes.catalog.Mode` (or slug) that provides
        stylistic guardrails appended to the prompt.
    persona:
        Optional :class:`~teslamind.persona.Persona` (or slug) that wraps the
        system prompt with character context.
    template:
        Base template. When omitted, :data:`DEFAULT_TEMPLATE` is used.
    name:
        Optional name for the resulting :class:`Prompt`. Defaults to the
        persona or mode slug when available.
    """

    resolved_mode = _resolve_mode(mode)
    resolved_persona = _resolve_persona(persona)
    base_template = template or DEFAULT_TEMPLATE
    normalized_task = task.strip()
    base_prompt = base_template.format(task=normalized_task)

    sections: list[str] = []
    if resolved_persona is not None:
        sections.append(resolved_persona.system_prompt())
    sections.append(base_prompt)
    if resolved_mode is not None:
        sections.append(resolved_mode.apply(normalized_task))

    prompt_name_candidates: Iterable[str | None] = (
        name,
        getattr(resolved_persona, "slug", None),
        getattr(resolved_mode, "slug", None),
    )
    for candidate in prompt_name_candidates:
        if candidate:
            prompt_name = candidate.replace(" ", "-")
            break
    else:  # pragma: no cover - fallback when all candidates are empty
        prompt_name = "composed"

    return Prompt(name=prompt_name, text="\n\n".join(sections))


__all__ = ["Prompt", "compose_prompt"]
