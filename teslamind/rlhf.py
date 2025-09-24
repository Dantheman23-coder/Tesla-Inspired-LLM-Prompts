"""Compatibility shim for RLHF helpers."""
from __future__ import annotations

from .advanced import RLHFTrainer, RLHFTrainingResult, RewardRecord

__all__ = [
    "RLHFTrainer",
    "RLHFTrainingResult",
    "RewardRecord",
]
