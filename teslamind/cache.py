"""Simple in-memory cache."""
from typing import Dict

_CACHE: Dict[str, str] = {}


def get(key: str) -> str | None:
    return _CACHE.get(key)


def set(key: str, value: str) -> None:
    _CACHE[key] = value
