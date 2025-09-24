"""Clinical safety filtering utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Set

DEFAULT_BLOCKED_TERMS: Set[str] = {"diagnosis", "treatment", "medical advice"}


@dataclass
class SafetyViolation:
    """Details about a detected clinical term."""

    term: str
    match: str
    start: int
    end: int

    def span(self) -> tuple[int, int]:
        """Return the start and end offsets of the violation."""

        return self.start, self.end


@dataclass
class SafetyReport:
    """Result of running :func:`filter_clinical_content`."""

    text: str
    violations: list[SafetyViolation]
    masked: bool

    @property
    def blocked_terms(self) -> Set[str]:
        return {violation.term for violation in self.violations}

    @property
    def violation_count(self) -> int:
        """Return how many violations were detected."""

        return len(self.violations)

    def has_violations(self) -> bool:
        """Return ``True`` when at least one violation was recorded."""

        return bool(self.violations)


def _normalize_terms(
    blocked_terms: Iterable[str], *, case_sensitive: bool
) -> list[tuple[str, str]]:
    normalized: list[tuple[str, str]] = []
    for term in blocked_terms:
        if not term:
            continue
        cleaned = term.strip()
        if not cleaned:
            continue
        search_term = cleaned if case_sensitive else cleaned.lower()
        normalized.append((cleaned, search_term))
    return normalized


def filter_clinical_content(
    text: str,
    blocked_terms: Iterable[str] = DEFAULT_BLOCKED_TERMS,
    *,
    mask: bool = False,
    mask_char: str = "*",
    report: bool = False,
    case_sensitive: bool = False,
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

    comparison_text = text if case_sensitive else text.lower()
    violations: list[SafetyViolation] = []
    masked_text = text
    for original_term, search_term in _normalize_terms(
        blocked_terms, case_sensitive=case_sensitive
    ):
        search_start = 0
        while True:
            index = comparison_text.find(search_term, search_start)
            if index == -1:
                break
            end_index = index + len(search_term)
            match_text = masked_text[index:end_index]
            violations.append(
                SafetyViolation(
                    term=original_term,
                    match=match_text,
                    start=index,
                    end=end_index,
                )
            )
            if mask:
                replacement = mask_char * len(match_text)
                masked_text = masked_text[:index] + replacement + masked_text[end_index:]
                comparison_text = masked_text if case_sensitive else masked_text.lower()
                search_start = index + len(replacement)
            else:
                search_start = end_index
        if violations and not mask and not report:
            raise ValueError(f"Clinical term '{original_term}' detected")

    masked = mask and bool(violations)
    if report:
        return SafetyReport(text=masked_text, violations=violations, masked=masked)
    if violations and not mask:
        # A violation was detected but report=False, so raise now.
        raise ValueError("Clinical terms detected")
    return masked_text
