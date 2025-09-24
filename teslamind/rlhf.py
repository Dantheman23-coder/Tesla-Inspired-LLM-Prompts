"""Reinforcement learning with human feedback utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, List


@dataclass
class FeedbackEvent:
    """Single feedback interaction during RLHF training."""

    prompt: str
    feedback: str
    reward: float
    accepted: bool


@dataclass
class TrainingSummary:
    """Summary of an RLHF training run."""

    events: List[FeedbackEvent]
    threshold: float

    @property
    def accepted_prompts(self) -> List[str]:
        return [event.prompt for event in self.events if event.accepted]

    @property
    def rejected_prompts(self) -> List[str]:
        return [event.prompt for event in self.events if not event.accepted]

    @property
    def average_reward(self) -> float:
        if not self.events:
            return 0.0
        return sum(event.reward for event in self.events) / len(self.events)

    @property
    def rewards(self) -> List[float]:
        """Return the raw reward values for each feedback event."""

        return [event.reward for event in self.events]

    @property
    def acceptance_rate(self) -> float:
        """Return the share of prompts that met the acceptance threshold."""

        if not self.events:
            return 0.0
        return len(self.accepted_prompts) / len(self.events)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the summary to a dictionary for reporting."""

        return {
            "threshold": self.threshold,
            "acceptance_rate": self.acceptance_rate,
            "events": [
                {
                    "prompt": event.prompt,
                    "feedback": event.feedback,
                    "reward": event.reward,
                    "accepted": event.accepted,
                }
                for event in self.events
            ],
            "average_reward": self.average_reward,
            "accepted_prompts": self.accepted_prompts,
            "rejected_prompts": self.rejected_prompts,
        }


class RLHFTrainer:
    """Simple RLHF training loop with reward tracking."""

    def __init__(
        self,
        reward_func: Callable[[str, str], float],
        *,
        threshold: float = 0.0,
        inclusive: bool = True,
    ) -> None:
        self.reward_func = reward_func
        self.threshold = threshold
        self.inclusive = inclusive
        self.last_rewards: List[float] = []
        self.history: List[TrainingSummary] = []
        self.last_summary: TrainingSummary | None = None

    def _is_accepted(self, reward: float) -> bool:
        return reward >= self.threshold if self.inclusive else reward > self.threshold

    def train(
        self,
        prompts: Iterable[str],
        feedback_provider: Callable[[str], str],
        *,
        return_summary: bool = False,
    ) -> List[str] | TrainingSummary:
        """Return prompts whose reward meets the threshold.

        When ``return_summary`` is ``True`` a :class:`TrainingSummary` with
        structured feedback metadata is returned instead of the accepted
        prompt list.
        """

        events: List[FeedbackEvent] = []
        for prompt in prompts:
            feedback = feedback_provider(prompt)
            reward = float(self.reward_func(prompt, feedback))
            accepted = self._is_accepted(reward)
            events.append(
                FeedbackEvent(
                    prompt=prompt,
                    feedback=feedback,
                    reward=reward,
                    accepted=accepted,
                )
            )
        summary = TrainingSummary(events=events, threshold=self.threshold)
        self.last_rewards = [event.reward for event in events]
        self.history.append(summary)
        self.last_summary = summary
        if return_summary:
            return summary
        return summary.accepted_prompts
