"""Configuration handling."""
from dataclasses import dataclass

@dataclass
class Config:
    cache_enabled: bool = True
