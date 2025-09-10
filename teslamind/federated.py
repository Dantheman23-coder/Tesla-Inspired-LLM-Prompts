"""Federated evaluation framework stubs."""

from __future__ import annotations

from itertools import islice
from typing import Any, Callable, Iterable, List


def run_federated_evaluation(
    prompts: Iterable[str], evaluate: Callable[[str], Any], shards: int = 1
) -> List[Any]:
    """Run evaluations across logical shards.

    Parameters
    ----------
    prompts:
        Iterable of prompt strings.
    evaluate:
        Function applied to each prompt.
    shards:
        Number of logical shards to split the work into. The function
        currently executes sequentially but preserves the interface for
        future distributed backends.
    """
    prompts = list(prompts)
    if shards < 1:
        raise ValueError("shards must be positive")

    shard_size = max(1, len(prompts) // shards)

    def shard_iterable(it: Iterable[str], size: int):
        iterator = iter(it)
        while True:
            chunk = list(islice(iterator, size))
            if not chunk:
                break
            yield chunk

    results: List[Any] = []
    for shard in shard_iterable(prompts, shard_size):
        shard_results = [evaluate(p) for p in shard]
        results.extend(shard_results)
    return results
