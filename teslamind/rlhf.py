"""Reinforcement learning with human feedback stubs."""

from __future__ import annotations

from typing import Callable, Iterable, List


class RLHFTrainer:
    """Simple RLHF training loop stub.

    The trainer applies feedback to prompts and keeps those that
    achieve a positive reward.
    """

    def __init__(self, reward_func: Callable[[str, str], float]):
        self.reward_func = reward_func

    def train(
        self, prompts: Iterable[str], feedback_provider: Callable[[str], str]
    ) -> List[str]:
        """Return prompts with positive reward."""
        trained: List[str] = []
        for prompt in prompts:
            feedback = feedback_provider(prompt)
            reward = self.reward_func(prompt, feedback)
            if reward > 0:
                trained.append(prompt)
        return trained
