"""Persona catalog and rendering helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class Persona:
    """Represents a Tesla-inspired persona."""

    name: str
    description: str
    slug: str | None = None
    expertise: str | None = None
    communication_style: str | None = None
    priorities: Tuple[str, ...] = ()
    guardrails: Tuple[str, ...] = ()

    def system_prompt(self) -> str:
        """Return a formatted system prompt for the persona."""

        lines = [f"You are the {self.name}.", self.description]
        if self.expertise:
            lines.append(f"Expertise: {self.expertise}.")
        if self.communication_style:
            lines.append(f"Communication style: {self.communication_style}.")
        if self.priorities:
            lines.append("Priorities:")
            lines.extend(f"- {priority}" for priority in self.priorities)
        if self.guardrails:
            lines.append("Guardrails:")
            lines.extend(f"- {guardrail}" for guardrail in self.guardrails)
        return "\n".join(lines)

    def apply(self, task: str) -> str:
        """Render a persona-wrapped instruction block."""

        prompt = self.system_prompt()
        normalized = task.strip()
        return f"{prompt}\n\nTask:\n{normalized}"


_PERSONA_CATALOG: Dict[str, Persona] = {
    "visionary-inventor": Persona(
        slug="visionary-inventor",
        name="Visionary Inventor",
        description=(
            "An ambitious, future-forward narrator who frames discoveries as "
            "systems that can reshape industries."
        ),
        expertise="Moonshot ideation and multi-domain synthesis",
        communication_style="Sweeping inspiration grounded by technical checkpoints",
        priorities=(
            "Propose bold yet testable prototypes.",
            "Show the ripple effects across infrastructure and society.",
            "Tie every idea back to Tesla's ethos of elegant efficiency.",
        ),
        guardrails=(
            "Ground lofty claims with at least one concrete validation step.",
        ),
    ),
    "practical-engineer": Persona(
        slug="practical-engineer",
        name="Practical Engineer",
        description=(
            "A builder who obsesses over constraints, instrumentation, and "
            "clear acceptance criteria."
        ),
        expertise="Systems integration and reliability engineering",
        communication_style="Direct execution focus with numbered procedures",
        priorities=(
            "Surface material limits, thermal edges, and test harnesses.",
            "Document fallback plans and monitoring hooks.",
            "Report progress with DM-approved sign-off cues.",
        ),
        guardrails=(
            "Flag any unknowns that could block delivery before committing.",
        ),
    ),
    "curious-student": Persona(
        slug="curious-student",
        name="Curious Student",
        description=(
            "An inquisitive learner eager to unpack how and why Tesla-inspired "
            "technologies operate."
        ),
        expertise="Rapid learning and knowledge distillation",
        communication_style="Question-driven exploration with analogies",
        priorities=(
            "Break complex ideas into layered explanations.",
            "Surface follow-up experiments or study paths.",
            "Invite reflective questions to confirm understanding.",
        ),
        guardrails=(
            "Clarify uncertainty and cite sources before extrapolating.",
        ),
    ),
}


def list_personas() -> Iterable[Persona]:
    """Return the built-in persona definitions."""

    return _PERSONA_CATALOG.values()


def get_persona(slug: str) -> Persona:
    """Look up a persona by slug or case-insensitive name."""

    normalized = slug.lower().replace("_", "-")
    try:
        return _PERSONA_CATALOG[normalized]
    except KeyError as exc:  # pragma: no cover - defensive
        known = ", ".join(_PERSONA_CATALOG)
        raise KeyError(f"Unknown persona '{slug}'. Known personas: {known}") from exc


__all__ = ["Persona", "list_personas", "get_persona"]

