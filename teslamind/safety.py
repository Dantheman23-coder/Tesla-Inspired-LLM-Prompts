"""Clinical safety switch utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Set

DEFAULT_BLOCKED_TERMS: Set[str] = {"diagnosis", "treatment", "medical advice"}


@dataclass
class SafetyViolation:
    """Details about a detected clinical term."""

    term: str
    match: str
    start: int
    end: int


@dataclass
class SafetyReport:
    """Result of running :func:`filter_clinical_content`."""

    text: str
    violations: List[SafetyViolation]
    masked: bool

    @property
    def blocked_terms(self) -> Set[str]:
        return {violation.term for violation in self.violations}


def _normalize_terms(blocked_terms: Iterable[str]) -> List[str]:
    normalized: List[str] = []
    for term in blocked_terms:
        if not term:
            continue
        normalized.append(term.lower())
    return normalized


def filter_clinical_content(
    text: str,
    blocked_terms: Iterable[str] = DEFAULT_BLOCKED_TERMS,
    *,
    mask: bool = False,
    mask_char: str = "*",
    report: bool = False,
) -> str | SafetyReport:
    """Validate or mask clinical terms in ``text``.

    When ``mask`` is ``False`` the function raises :class:`ValueError` if a
    blocked term is encountered. When ``mask`` is ``True`` the offending
    terms are replaced with ``mask_char`` and the modified text is returned.

    Setting ``report`` to ``True`` returns a :class:`SafetyReport` containing
    the masked text and detailed violation metadata.
    """

    if mask and not mask_char:
        raise ValueError("mask_char must be provided when masking")

    lowered = text.lower()
    violations: List[SafetyViolation] = []
    masked_text = text
    for term in _normalize_terms(blocked_terms):
        search_start = 0
        while True:
            index = lowered.find(term, search_start)
            if index == -1:
                break
            match_text = masked_text[index : index + len(term)]
            violations.append(
                SafetyViolation(term=term, match=match_text, start=index, end=index + len(term))
            )
            if mask:
                replacement = mask_char * len(term)
                masked_text = masked_text[:index] + replacement + masked_text[index + len(term) :]
                lowered = masked_text.lower()
                search_start = index + len(replacement)
            else:
                search_start = index + len(term)
        if violations and not mask and not report:
            raise ValueError(f"Clinical term '{term}' detected")

    masked = mask and bool(violations)
    if report:
        return SafetyReport(text=masked_text, violations=violations, masked=masked)
    if violations and not mask:
        # A violation was detected but report=False, so raise now.
        raise ValueError("Clinical terms detected")
    return masked_text
