"""Clinical safety switch utilities."""

from __future__ import annotations

from typing import Iterable, Set

DEFAULT_BLOCKED_TERMS: Set[str] = {"diagnosis", "treatment", "medical advice"}


def filter_clinical_content(
    text: str, blocked_terms: Iterable[str] = DEFAULT_BLOCKED_TERMS
) -> str:
    """Raise :class:`ValueError` if ``text`` contains any blocked term."""
    lowered = text.lower()
    for term in blocked_terms:
        if term in lowered:
            raise ValueError(f"Clinical term '{term}' detected")
    return text
