"""Compatibility re-export for the refinement helpers.

The canonical implementation lives in :mod:`teslamind.refinement`. This module
remains so legacy imports such as ``import refinement`` or
``from refinement import SelfLoopingPromptGenerator`` keep working after the
package was reorganized under the ``teslamind`` namespace.
"""

from teslamind.refinement import (  # noqa: F401
    RefinementHistory,
    RefinementStep,
    SelfLoopingPromptGenerator,
)

__all__ = [
    "SelfLoopingPromptGenerator",
    "RefinementHistory",
    "RefinementStep",
]
