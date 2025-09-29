"""Reinforcement learning with human feedback stubs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List, Tuple


@dataclass
class RLHFResult:
    """Container for the outcome of a single RLHF step."""

    prompt: str
    feedback: str
    reward: float


class RLHFTrainer:
    """Simple RLHF training loop stub with thresholding."""

    def __init__(self, reward_func: Callable[[str, str], float], threshold: float = 0.0):
        self.reward_func = reward_func
        self.threshold = threshold

    def train(
        self,
        prompts: Iterable[str],
        feedback_provider: Callable[[str], str],
        *,
        return_history: bool = False,
    ) -> List[str] | Tuple[List[str], List[RLHFResult]]:
        """Return prompts that meet the reward threshold.

        When ``return_history`` is true, returns both the filtered prompts
        and the per-example :class:`RLHFResult` records.
        """

        kept: List[str] = []
        history: List[RLHFResult] = []
        for prompt in prompts:
            feedback = feedback_provider(prompt)
            reward = self.reward_func(prompt, feedback)
            history.append(RLHFResult(prompt=prompt, feedback=feedback, reward=reward))
            if reward >= self.threshold:
                kept.append(prompt)

        if return_history:
            return kept, history
        return kept
