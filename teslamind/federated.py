"""Federated evaluation framework stubs."""

from __future__ import annotations

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
    results: List[Any] = []
    for prompt in prompts:
        results.append(evaluate(prompt))
    return results
