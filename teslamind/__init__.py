"""TeslaMind core package."""

from .version import __version__
from .prompt import Prompt
from .persona import Persona

__all__ = ["Prompt", "Persona", "__version__"]
