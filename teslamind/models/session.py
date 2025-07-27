"""Session model."""
from dataclasses import dataclass

@dataclass
class Session:
    id: str
    user_id: str
