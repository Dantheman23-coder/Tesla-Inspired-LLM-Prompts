"""Prompt refinement helpers inspired by Tesla's iterative experiments."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

RefineFunction = Callable[[str], "RefineOutput"]
RefineOutput = str | tuple[str, Mapping[str, Any]]


@dataclass
class RefinementStep:
    """Snapshot of a single refinement iteration."""

    iteration: int
    prompt: str
    score: float | None = None
    metadata: Mapping[str, Any] | None = None


class SelfLoopingPromptRefiner:
    """Iteratively improve prompts with a user supplied refinement function."""

    def __init__(
        self,
        refine: RefineFunction,
        *,
        max_iterations: int = 5,
        score_threshold: float | None = None,
    ) -> None:
        if max_iterations <= 0:
            raise ValueError("max_iterations must be positive")
        self._refine = refine
        self._max_iterations = max_iterations
        self._score_threshold = score_threshold

    def refine(
        self,
        prompt: str,
        *,
        return_history: bool = False,
    ) -> str | tuple[str, list[RefinementStep]]:
        """Run the refinement loop.

        Parameters
        ----------
        prompt:
            Starting prompt text.
        return_history:
            When True, return the final prompt alongside the iteration history.
        """

        history: list[RefinementStep] = []
        current = prompt
        for iteration in range(1, self._max_iterations + 1):
            result = self._refine(current)
            if isinstance(result, tuple):
                updated_prompt, metadata = result
            else:
                updated_prompt, metadata = result, {}

            score = None
            if isinstance(metadata, Mapping):
                raw_score = metadata.get("score")
                if isinstance(raw_score, (int, float)):
                    score = float(raw_score)

            history.append(
                RefinementStep(
                    iteration=iteration,
                    prompt=updated_prompt,
                    score=score,
                    metadata=metadata or None,
                )
            )
            current = updated_prompt

            if (
                self._score_threshold is not None
                and score is not None
                and score >= self._score_threshold
            ):
                break
            if updated_prompt == prompt:
                break
            prompt = updated_prompt

        if return_history:
            return current, history
        return current


__all__ = [
    "RefineFunction",
    "RefineOutput",
    "RefinementStep",
    "SelfLoopingPromptRefiner",
]
