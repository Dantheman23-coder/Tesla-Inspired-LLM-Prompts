"""Score model."""
from dataclasses import dataclass

@dataclass
class Score:
    value: float
    rubric: str
