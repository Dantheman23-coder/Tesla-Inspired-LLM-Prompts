"""Federated evaluation framework stubs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Sequence, Tuple


@dataclass
class FederatedShardResult:
    """Represents the evaluation results for a shard."""

    shard_index: int
    prompts: Sequence[str]
    outputs: Sequence[Any]


def _partition(prompts: Sequence[str], shards: int) -> List[List[Tuple[int, str]]]:
    buckets: List[List[Tuple[int, str]]] = [[] for _ in range(shards)]
    for idx, prompt in enumerate(prompts):
        buckets[idx % shards].append((idx, prompt))
    return buckets


def run_federated_evaluation(
    prompts: Iterable[str],
    evaluate: Callable[[str], Any],
    shards: int = 1,
    *,
    return_shard_results: bool = False,
) -> List[Any] | Tuple[List[Any], List[FederatedShardResult]]:
    """Run evaluations across logical shards.

    When ``return_shard_results`` is true, returns both the aggregated
    results and a list of :class:`FederatedShardResult` records for
    transparency.
    """

    prompts = list(prompts)
    if shards < 1:
        raise ValueError("shards must be positive")

    partitions = _partition(prompts, shards)
    aggregated_with_index: List[Tuple[int, Any]] = []
    shard_results: List[FederatedShardResult] = []
    for shard_index, shard_prompts in enumerate(partitions):
        outputs: List[Any] = []
        raw_prompts: List[str] = []
        for original_index, prompt in shard_prompts:
            output = evaluate(prompt)
            outputs.append(output)
            raw_prompts.append(prompt)
            aggregated_with_index.append((original_index, output))
        shard_results.append(
            FederatedShardResult(
                shard_index=shard_index,
                prompts=tuple(raw_prompts),
                outputs=tuple(outputs),
            )
        )

    aggregated = [output for _, output in sorted(aggregated_with_index, key=lambda item: item[0])]
    if return_shard_results:
        return aggregated, shard_results
    return aggregated
