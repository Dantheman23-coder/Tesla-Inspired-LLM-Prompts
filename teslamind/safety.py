"""Clinical safety filtering helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass
class SafetyViolation:
    """Record of a blocked clinical term found in text."""

    term: str
    start: int
    end: int


@dataclass
class SafetyReport:
    """Result of scanning a prompt for clinical safety terms."""

    original_text: str
    sanitized_text: str
    violations: list[SafetyViolation]

    @property
    def is_clean(self) -> bool:
        return not self.violations


class ClinicalSafetyFilter:
    """Detect and optionally mask blocked medical terms in prompts."""

    def __init__(
        self,
        blocked_terms: Sequence[str],
        *,
        mask: bool = False,
        mask_char: str = "█",
        raise_on_violation: bool = False,
    ) -> None:
        self._blocked_terms = tuple(term for term in blocked_terms if term)
        self._mask = mask
        self._mask_char = mask_char
        self._raise = raise_on_violation

    def scan(self, text: str) -> SafetyReport:
        lowered = text.lower()
        sanitized = list(text)
        violations: list[SafetyViolation] = []

        for term in self._blocked_terms:
            start = 0
            needle = term.lower()
            if not needle:
                continue
            while True:
                index = lowered.find(needle, start)
                if index == -1:
                    break
                end = index + len(term)
                violations.append(SafetyViolation(term=term, start=index, end=end))
                if self._mask:
                    sanitized[index:end] = self._mask_char * (end - index)
                start = end

        report = SafetyReport(
            original_text=text,
            sanitized_text="".join(sanitized),
            violations=violations,
        )
        if self._raise and not report.is_clean:
            raise ValueError("clinical safety violation detected")
        return report


__all__ = ["ClinicalSafetyFilter", "SafetyReport", "SafetyViolation"]
