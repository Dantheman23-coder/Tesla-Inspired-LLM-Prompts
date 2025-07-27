"""Persona definitions."""
from dataclasses import dataclass

@dataclass
class Persona:
    """A simple persona with a name and description."""

    name: str
    description: str
