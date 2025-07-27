"""Prompt metadata model."""
from dataclasses import dataclass

@dataclass
class PromptMeta:
    title: str
    version: str
    prompt_path: str
    domain: str | None = None
    length_tokens: int | None = None
    license: str | None = None
    description: str | None = None
