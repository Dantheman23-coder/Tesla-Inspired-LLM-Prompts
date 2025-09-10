"""Reinforcement learning with human feedback stubs."""

from __future__ import annotations

from typing import Callable, Iterable, List


class RLHFTrainer:
    """Simple RLHF training loop stub.

    The trainer applies feedback to prompts and keeps those that
    achieve a reward above a threshold.
    """

    def __init__(self, reward_func: Callable[[str, str], float], *, threshold: float = 0.0):
        self.reward_func = reward_func
        self.threshold = threshold
        self.last_rewards: List[float] = []

    def train(
        self, prompts: Iterable[str], feedback_provider: Callable[[str], str]
    ) -> List[str]:
        """Return prompts whose reward exceeds ``threshold``.

        The rewards from the last training run are stored on the instance
        in ``last_rewards`` for inspection or analysis.
        """
        trained: List[str] = []
        rewards: List[float] = []
        for prompt in prompts:
            feedback = feedback_provider(prompt)
            reward = self.reward_func(prompt, feedback)
            rewards.append(reward)
            if reward > self.threshold:
                trained.append(prompt)
        self.last_rewards = rewards
        return trained
