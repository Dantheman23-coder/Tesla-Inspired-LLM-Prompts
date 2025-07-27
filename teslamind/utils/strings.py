"""String helpers."""
import re

def slugify(text: str) -> str:
    return re.sub(r"\W+", "-", text).strip("-").lower()
