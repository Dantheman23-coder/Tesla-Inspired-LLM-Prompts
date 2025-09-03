"""Self-looping prompt refinement utilities."""

from __future__ import annotations

from typing import Callable, Tuple


class SelfLoopingPromptGenerator:
    """Iteratively refines a prompt using a refinement function.

    The refinement function receives the current prompt and returns a tuple
    of the new prompt and a boolean indicating whether an improvement was
    made. The generator stops when no improvement is reported or the
    maximum number of iterations is reached.
    """

    def __init__(self, max_iters: int = 5) -> None:
        self.max_iters = max_iters

    def generate(
        self, prompt: str, refine_func: Callable[[str], Tuple[str, bool]]
    ) -> str:
        """Run the self-looping refinement process."""
        for _ in range(self.max_iters):
            prompt, improved = refine_func(prompt)
            if not improved:
                break
        return prompt
