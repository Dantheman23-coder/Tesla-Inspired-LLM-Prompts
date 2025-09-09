"""Clinical safety switch utilities."""

from __future__ import annotations

from typing import Iterable, Set

DEFAULT_BLOCKED_TERMS: Set[str] = {"diagnosis", "treatment", "medical advice"}


def filter_clinical_content(
    text: str,
    blocked_terms: Iterable[str] = DEFAULT_BLOCKED_TERMS,
    *,
    mask: bool = False,
    mask_char: str = "*",
) -> str:
    """Validate or mask clinical terms in ``text``.

    Parameters
    ----------
    text:
        Text to inspect.
    blocked_terms:
        Iterable of terms that trigger validation.
    mask:
        If ``True`` occurrences of blocked terms are replaced with
        ``mask_char`` rather than raising an error.
    mask_char:
        Character used to mask blocked terms when ``mask`` is enabled.
    """

    lowered = text.lower()
    for term in blocked_terms:
        index = lowered.find(term)
        if index != -1:
            if mask:
                text = (
                    text[:index]
                    + mask_char * len(term)
                    + text[index + len(term) :]
                )
                lowered = text.lower()
                continue
            raise ValueError(f"Clinical term '{term}' detected")
    return text
