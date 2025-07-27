"""File helpers."""
from pathlib import Path

def read_file(path: Path) -> str:
    return path.read_text()
