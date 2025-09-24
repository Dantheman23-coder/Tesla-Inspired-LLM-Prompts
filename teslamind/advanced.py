"""Advanced prompt tooling inspired by Tesla's experimental workflows."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping, MutableMapping, Sequence

RefineFunction = Callable[[str], "RefineOutput"]
RefineOutput = str | tuple[str, Mapping[str, Any]]


@dataclass
class RefinementStep:
    """Snapshot of a single refinement iteration."""

    iteration: int
    prompt: str
    score: float | None = None
    metadata: Mapping[str, Any] | None = None


class SelfLoopingPromptRefiner:
    """Iteratively improve prompts with a user supplied refinement function."""

    def __init__(
        self,
        refine: RefineFunction,
        *,
        max_iterations: int = 5,
        score_threshold: float | None = None,
    ) -> None:
        if max_iterations <= 0:
            raise ValueError("max_iterations must be positive")
        self._refine = refine
        self._max_iterations = max_iterations
        self._score_threshold = score_threshold

    def refine(self, prompt: str, *, return_history: bool = False) -> str | tuple[str, list[RefinementStep]]:
        """Run the refinement loop.

        Parameters
        ----------
        prompt:
            Starting prompt text.
        return_history:
            When True, return the final prompt alongside the iteration history.
        """

        history: list[RefinementStep] = []
        current = prompt
        for iteration in range(1, self._max_iterations + 1):
            result = self._refine(current)
            if isinstance(result, tuple):
                updated_prompt, metadata = result
            else:
                updated_prompt, metadata = result, {}

            score = None
            if isinstance(metadata, Mapping):
                raw_score = metadata.get("score")
                if isinstance(raw_score, (int, float)):
                    score = float(raw_score)

            history.append(
                RefinementStep(
                    iteration=iteration,
                    prompt=updated_prompt,
                    score=score,
                    metadata=metadata or None,
                )
            )
            current = updated_prompt

            if self._score_threshold is not None and score is not None and score >= self._score_threshold:
                break
            if updated_prompt == prompt:
                break
            prompt = updated_prompt

        if return_history:
            return current, history
        return current


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


@dataclass
class RewardRecord:
    """Reward observation captured during RLHF training."""

    prompt: str
    reward: float


@dataclass
class RLHFTrainingResult:
    """Summary of accepted and rejected prompts from RLHF."""

    accepted: list[str]
    rejected: list[str]
    history: list[RewardRecord]


class RLHFTrainer:
    """Filter prompts based on rewards from a feedback provider."""

    def __init__(self, reward_provider: Callable[[str], float], *, reward_threshold: float = 0.0) -> None:
        self._reward_provider = reward_provider
        self._threshold = reward_threshold

    def train(self, prompts: Iterable[str]) -> RLHFTrainingResult:
        accepted: list[str] = []
        rejected: list[str] = []
        history: list[RewardRecord] = []

        for prompt in prompts:
            reward = float(self._reward_provider(prompt))
            history.append(RewardRecord(prompt=prompt, reward=reward))
            if reward >= self._threshold:
                accepted.append(prompt)
            else:
                rejected.append(prompt)

        return RLHFTrainingResult(accepted=accepted, rejected=rejected, history=history)


@dataclass
class SafetyViolation:
    """Record of a blocked clinical term found in text."""

    term: str
    start: int
    end: int


@dataclass
class SafetyReport:
    """Result of scanning a prompt for clinical safety terms."""

    original_text: str
    sanitized_text: str
    violations: list[SafetyViolation]

    @property
    def is_clean(self) -> bool:
        return not self.violations


class ClinicalSafetyFilter:
    """Detect and optionally mask blocked medical terms in prompts."""

    def __init__(
        self,
        blocked_terms: Sequence[str],
        *,
        mask: bool = False,
        mask_char: str = "█",
        raise_on_violation: bool = False,
    ) -> None:
        self._blocked_terms = tuple(term for term in blocked_terms if term)
        self._mask = mask
        self._mask_char = mask_char
        self._raise = raise_on_violation

    def scan(self, text: str) -> SafetyReport:
        lowered = text.lower()
        sanitized = list(text)
        violations: list[SafetyViolation] = []

        for term in self._blocked_terms:
            start = 0
            needle = term.lower()
            if not needle:
                continue
            while True:
                index = lowered.find(needle, start)
                if index == -1:
                    break
                end = index + len(term)
                violations.append(SafetyViolation(term=term, start=index, end=end))
                if self._mask:
                    sanitized[index:end] = self._mask_char * (end - index)
                start = end

        report = SafetyReport(original_text=text, sanitized_text="".join(sanitized), violations=violations)
        if self._raise and not report.is_clean:
            raise ValueError("clinical safety violation detected")
        return report
