"""Catalog of TeslaMind prompt modes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class Mode:
    """Represents a stylistic prompt mode.

    Attributes
    ----------
    slug:
        Identifier used in the CLI and API. Stored in ``lowercase-with-dashes``
        so it can be typed quickly.
    title:
        Human-readable title shown in documentation.
    description:
        Short summary of when the mode should be used.
    voice:
        High-level guidance for the tone the mode should adopt.
    prefix:
        Tagline prepended to the task when :meth:`apply` is invoked.
    commitments:
        Style guardrails enumerated for readers. They are rendered as a bullet
        list when composing prompts.
    """

    slug: str
    title: str
    description: str
    voice: str
    prefix: str
    commitments: Tuple[str, ...] = ()

    def apply(self, task: str) -> str:
        """Render the task inside the stylistic wrapper."""

        normalized = " ".join(task.strip().split())
        prompt = f"{self.prefix} {normalized}"
        if not self.commitments:
            return prompt
        bullets = "\n".join(f"- {commitment}" for commitment in self.commitments)
        return f"{prompt}\n\nStyle commitments:\n{bullets}"

    def summary(self) -> str:
        """Return a detailed, human-readable description."""

        lines = [self.title, "", self.description, "", f"Voice: {self.voice}"]
        if self.commitments:
            lines.append("Style commitments:")
            lines.extend(f"- {commitment}" for commitment in self.commitments)
        return "\n".join(lines)


_MODE_CATALOG: Dict[str, Mode] = {
    "energy": Mode(
        slug="energy",
        title="Energy Mode",
        description="Enthusiastic, action-focused output for rapid execution.",
        voice="High-voltage direction with decisive verbs and measurable wins.",
        prefix="[Energy Mode]",
        commitments=(
            "Lead with momentum and clearly defined next steps.",
            "Quantify energetic impact and efficiency gains whenever possible.",
            "Translate insights into execution-ready checklists.",
        ),
    ),
    "patent": Mode(
        slug="patent",
        title="Patent Mode",
        description="Formal technical tone suited for defensible disclosures.",
        voice="Precise, reference-heavy prose with legal-ready clarity.",
        prefix="[Patent Mode]",
        commitments=(
            "Define claims, embodiments, and novelty explicitly.",
            "Cite supporting mechanisms and instrumentation rigorously.",
            "Flag prior art considerations and validation evidence.",
        ),
    ),
    "invention": Mode(
        slug="invention",
        title="Invention Mode",
        description="Divergent brainstorming channeling Tesla's experimental flair.",
        voice="Playful but technical ideation with rapid prototyping hooks.",
        prefix="[Invention Mode]",
        commitments=(
            "Surface multiple concept variations with feasibility signals.",
            "Propose instrumentation or experiments for each leap.",
            "Highlight risks and possible adjacent breakthroughs.",
        ),
    ),
    "visionary": Mode(
        slug="visionary",
        title="Visionary Mode",
        description="Futuristic narratives that align bold visions with delivery.",
        voice="Inspiring storytelling grounded in systems thinking.",
        prefix="[Visionary Mode]",
        commitments=(
            "Connect present decisions to long-horizon outcomes.",
            "Balance inspiration with credible technical scaffolding.",
            "Surface societal or ecosystem-level reverberations.",
        ),
    ),
    "hyperscience": Mode(
        slug="hyperscience",
        title="Hyperscience Mode",
        description="Deep scientific exposition for complex phenomena.",
        voice="Lab-grade precision with references to theory and experiment.",
        prefix="[Hyperscience Mode]",
        commitments=(
            "Explain mechanisms with stepwise derivations or models.",
            "Call out measurement apparatus, tolerances, and assumptions.",
            "Contrast competing hypotheses and justify chosen approaches.",
        ),
    ),
    "coop": Mode(
        slug="coop",
        title="Cooperative Mode",
        description="Collaborative tone optimized for cross-functional teams.",
        voice="Inclusive facilitation that keeps stakeholders aligned.",
        prefix="[Cooperative Mode]",
        commitments=(
            "Invite feedback loops and surface shared objectives.",
            "Map decision points to accountable owners and timelines.",
            "Celebrate progress while identifying support requests.",
        ),
    ),
}


def list_modes() -> Iterable[Mode]:
    """Return the built-in TeslaMind modes in definition order."""

    return _MODE_CATALOG.values()


def get_mode(slug: str) -> Mode:
    """Return a single mode by its slug."""

    normalized = slug.lower().replace(" ", "-")
    try:
        return _MODE_CATALOG[normalized]
    except KeyError as exc:  # pragma: no cover - defensive
        known = ", ".join(_MODE_CATALOG)
        raise KeyError(f"Unknown mode '{slug}'. Known modes: {known}") from exc


__all__ = ["Mode", "list_modes", "get_mode"]

