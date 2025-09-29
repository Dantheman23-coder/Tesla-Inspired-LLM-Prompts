"""Clinical safety switch utilities."""

from __future__ import annotations

from typing import Iterable, Iterator, Set

DEFAULT_BLOCKED_TERMS: Set[str] = {"diagnosis", "treatment", "medical advice"}


def _iter_matches(text: str, blocked_terms: Iterable[str]) -> Iterator[str]:
    lowered = text.lower()
    for term in blocked_terms:
        if term in lowered:
            yield term


def mask_sensitive_terms(
    text: str,
    blocked_terms: Iterable[str] = DEFAULT_BLOCKED_TERMS,
    *,
    mask: str = "[REDACTED]",
) -> str:
    """Return ``text`` with blocked terms masked."""

    result = text
    for term in _iter_matches(text, blocked_terms):
        result = result.replace(term, mask)
        result = result.replace(term.title(), mask)
    return result


def filter_clinical_content(
    text: str,
    blocked_terms: Iterable[str] = DEFAULT_BLOCKED_TERMS,
    *,
    mask: bool = False,
) -> str:
    """Validate ``text`` against blocked terms.

    When ``mask`` is ``True`` the text is returned with matches masked
    instead of raising an exception.
    """

    matches = list(_iter_matches(text, blocked_terms))
    if not matches:
        return text
    if mask:
        return mask_sensitive_terms(text, blocked_terms)
    raise ValueError(f"Clinical term(s) detected: {', '.join(matches)}")
