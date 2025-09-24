"""Reinforcement learning from human feedback helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List


@dataclass
class RewardRecord:
    """Reward observation captured during RLHF training."""

    prompt: str
    reward: float


@dataclass
class RLHFTrainingResult:
    """Summary of accepted and rejected prompts from RLHF."""

    accepted: List[str]
    rejected: List[str]
    history: List[RewardRecord]


class RLHFTrainer:
    """Filter prompts based on rewards from a feedback provider."""

    def __init__(self, reward_provider: Callable[[str], float], *, reward_threshold: float = 0.0) -> None:
        self._reward_provider = reward_provider
        self._threshold = reward_threshold

    def train(self, prompts: Iterable[str]) -> RLHFTrainingResult:
        accepted: List[str] = []
        rejected: List[str] = []
        history: List[RewardRecord] = []

        for prompt in prompts:
            reward = float(self._reward_provider(prompt))
            history.append(RewardRecord(prompt=prompt, reward=reward))
            if reward >= self._threshold:
                accepted.append(prompt)
            else:
                rejected.append(prompt)

        return RLHFTrainingResult(accepted=accepted, rejected=rejected, history=history)


__all__ = ["RewardRecord", "RLHFTrainer", "RLHFTrainingResult"]
