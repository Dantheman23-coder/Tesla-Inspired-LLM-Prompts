"""Federated prompt evaluation helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, MutableMapping, Sequence


@dataclass
class ShardReport:
    """Evaluation results for a single shard of prompts."""

    shard: str
    prompts: Sequence[str]
    metrics: Mapping[str, float]


@dataclass
class FederatedEvaluation:
    """Aggregated evaluation output across shards."""

    reports: list[ShardReport]
    aggregate: Mapping[str, float]


class FederatedEvaluator:
    """Run prompt evaluation functions across logical shards."""

    def __init__(
        self,
        evaluator: Callable[[Sequence[str]], Mapping[str, float]],
        *,
        aggregator: Callable[[Sequence[ShardReport]], Mapping[str, float]] | None = None,
    ) -> None:
        self._evaluator = evaluator
        self._aggregator = aggregator

    def evaluate(self, shards: Mapping[str, Sequence[str]]) -> FederatedEvaluation:
        reports: list[ShardReport] = []
        for shard, prompts in shards.items():
            metrics = dict(self._evaluator(prompts))
            reports.append(ShardReport(shard=shard, prompts=list(prompts), metrics=metrics))

        aggregate = self._aggregate(reports)
        return FederatedEvaluation(reports=reports, aggregate=aggregate)

    def _aggregate(self, reports: Sequence[ShardReport]) -> Mapping[str, float]:
        if self._aggregator is not None:
            return self._aggregator(reports)

        totals: MutableMapping[str, float] = {}
        counts: MutableMapping[str, int] = {}
        for report in reports:
            for metric, value in report.metrics.items():
                if isinstance(value, (int, float)):
                    totals[metric] = totals.get(metric, 0.0) + float(value)
                    counts[metric] = counts.get(metric, 0) + 1
        return {metric: totals[metric] / counts[metric] for metric in totals}


__all__ = ["FederatedEvaluation", "FederatedEvaluator", "ShardReport"]
