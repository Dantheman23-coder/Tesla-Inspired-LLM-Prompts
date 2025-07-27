"""Prompt management utilities."""
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Prompt:
    """Represents a prompt template."""

    name: str
    text: str

    @classmethod
    def from_file(cls, path: Path) -> "Prompt":
        return cls(name=path.stem, text=path.read_text())

    def save(self, path: Path) -> None:
        path.write_text(self.text)
