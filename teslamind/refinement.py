"""Self-looping prompt refinement utilities."""

from __future__ import annotations

from typing import Callable, List, Tuple


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
        self,
        prompt: str,
        refine_func: Callable[[str], Tuple[str, bool]],
        *,
        return_history: bool = False,
    ) -> str | Tuple[str, List[str]]:
        """Run the self-looping refinement process.

        Parameters
        ----------
        prompt:
            Initial prompt to refine.
        refine_func:
            Function that returns a new prompt and ``True`` if an
            improvement was made.
        return_history:
            When ``True`` the function also returns the list of intermediate
            prompts including the initial one. This can be useful for
            debugging or analysis of the refinement trajectory.
        """

        history: List[str] = [prompt]
        for _ in range(self.max_iters):
            prompt, improved = refine_func(prompt)
            history.append(prompt)
            if not improved:
                break

        if return_history:
            return prompt, history
        return prompt
