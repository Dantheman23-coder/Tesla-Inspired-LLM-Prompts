"""Self-looping prompt refinement utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Tuple


@dataclass
class RefinementHistory:
    """History of a refinement run."""

    steps: List[str]
    iterations: int
    stopped_reason: str


class SelfLoopingPromptGenerator:
    """Iteratively refines a prompt using a refinement function.

    The generator records intermediate prompts so that callers can
    inspect how a prompt evolved over time.
    """

    def __init__(self, max_iters: int = 5) -> None:
        self.max_iters = max_iters

    def generate(
        self,
        prompt: str,
        refine_func: Callable[[str], Tuple[str, bool]],
        *,
        return_history: bool = False,
    ) -> str | Tuple[str, RefinementHistory]:
        """Run the self-looping refinement process.

        Parameters
        ----------
        prompt:
            Starting prompt text.
        refine_func:
            Callable returning the next prompt and a boolean indicating
            if the iteration produced an improvement.
        return_history:
            When true, return a :class:`RefinementHistory` alongside the
            final prompt.
        """

        steps = [prompt]
        last_reason = "max_iters"
        for iteration in range(1, self.max_iters + 1):
            prompt, improved = refine_func(prompt)
            steps.append(prompt)
            if not improved:
                last_reason = "no_improvement"
                break
        else:
            iteration = self.max_iters

        if return_history:
            history = RefinementHistory(
                steps=steps,
                iterations=iteration,
                stopped_reason=last_reason,
            )
            return prompt, history
        return prompt
