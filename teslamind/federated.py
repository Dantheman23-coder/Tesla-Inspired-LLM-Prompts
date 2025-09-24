"""Federated evaluation framework utilities."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Sequence


@dataclass
class EvaluationRecord:
    """Result from evaluating a single prompt on a shard."""

    prompt: str
    shard_id: int
    result: Any


@dataclass
class FederatedEvaluationReport:
    """Collection of evaluation records with optional aggregate data."""

    records: list[EvaluationRecord]
    aggregate: Any | None = None

    def __len__(self) -> int:
        """Return how many evaluation records are stored."""

        return len(self.records)

    def flatten(self) -> list[Any]:
        """Return just the evaluation results, preserving input order."""

        return [record.result for record in self.records]

    def prompts(self) -> list[str]:
        """Return prompts in the order they were evaluated."""

        return [record.prompt for record in self.records]

    def by_shard(self) -> dict[int, list[EvaluationRecord]]:
        """Group evaluation records by shard identifier."""

        grouped: dict[int, list[EvaluationRecord]] = {}
        for record in self.records:
            grouped.setdefault(record.shard_id, []).append(record)
        return grouped

    @property
    def shard_count(self) -> int:
        """Return how many shards contributed to the report."""

        return len(self.by_shard())


def run_federated_evaluation(
    prompts: Iterable[str],
    evaluate: Callable[[str], Any],
    *,
    shards: int = 1,
    shard_size: int | None = None,
    aggregate: Callable[[Sequence[Any]], Any] | None = None,
    aggregate_default: Any | None = None,
    with_metadata: bool = False,
) -> list[Any] | FederatedEvaluationReport:
    """Run evaluations across logical shards.

    Parameters
    ----------
    prompts:
        Iterable of prompt strings to evaluate.
    evaluate:
        Callable applied to each prompt.
    shards:
        Target number of logical shards. The function still executes
        sequentially but respects sharding boundaries for reproducible
        batching.
    shard_size:
        Optional explicit shard size. When omitted, it is derived from the
        number of prompts and the requested ``shards``.
    aggregate:
        Optional callable receiving the flattened evaluation results and
        returning an aggregate metric (e.g., an average score).
    aggregate_default:
        Value returned when ``aggregate`` is provided but no prompts were
        evaluated. This avoids calling reducers that expect at least one
        result.
    with_metadata:
        When ``True`` a :class:`FederatedEvaluationReport` containing shard
        metadata is returned. Otherwise only the flattened results are
        produced for convenience.
    """

    prompt_list = list(prompts)
    if shards < 1:
        raise ValueError("shards must be positive")
    if shard_size is not None and shard_size < 1:
        raise ValueError("shard_size must be positive when provided")
    if not prompt_list:
        records: list[EvaluationRecord] = []
    else:
        effective_shard_size = shard_size or math.ceil(len(prompt_list) / shards)
        if effective_shard_size < 1:
            effective_shard_size = 1
        records: list[EvaluationRecord] = []
        shard_index = 0
        for start in range(0, len(prompt_list), effective_shard_size):
            shard_prompts = prompt_list[start : start + effective_shard_size]
            for prompt in shard_prompts:
                records.append(
                    EvaluationRecord(
                        prompt=prompt,
                        shard_id=shard_index,
                        result=evaluate(prompt),
                    )
                )
            shard_index += 1
    flattened = [record.result for record in records]
    if aggregate:
        aggregate_value = aggregate(flattened) if flattened else aggregate_default
    else:
        aggregate_value = None
    if with_metadata:
        return FederatedEvaluationReport(records=records, aggregate=aggregate_value)
    return flattened
