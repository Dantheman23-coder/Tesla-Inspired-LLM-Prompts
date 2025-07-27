"""Simple scoring utilities."""
from .models.score import Score


def length_score(text: str) -> Score:
    return Score(value=len(text), rubric="length")
