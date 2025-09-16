"""Self-looping prompt refinement utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Tuple, Union


@dataclass
class RefinementStep:
    """Represents a single refinement step.

    Attributes
    ----------
    prompt:
        The prompt text after the refinement step has been applied.
    improved:
        ``True`` when the refinement resulted in an improvement according
        to the refinement strategy.
    feedback:
        Optional feedback describing why the step was taken or why it
        halted.
    score:
        Optional numeric score attached to the prompt after the
        refinement was applied. When provided, the generator can enforce a
        minimum score delta between iterations.
    """

    prompt: str
    improved: bool
    feedback: str | None = None
    score: float | None = None


@dataclass
class RefinementHistory:
    """Structured record of a refinement run."""

    steps: List[RefinementStep]

    @property
    def final_prompt(self) -> str:
        """Return the prompt from the last recorded step."""

        if not self.steps:
            return ""
        return self.steps[-1].prompt

    @property
    def iterations(self) -> int:
        """Return how many refinement iterations were executed."""

        count = max(0, len(self.steps) - 1)
        if self.steps and self.steps[-1].feedback == "maximum iterations reached":
            count = max(0, count - 1)
        return count

    @property
    def total_improvements(self) -> int:
        """Return the number of successful improvements."""

        return sum(1 for step in self.steps if step.improved)

    def prompts(self) -> List[str]:
        """Return the prompt text at each recorded step."""

        return [step.prompt for step in self.steps]


RefinementReturn = Union[
    Tuple[str, bool],
    Tuple[str, bool, str | None],
    Tuple[str, bool, str | None, float | None],
    RefinementStep,
]


class SelfLoopingPromptGenerator:
    """Iteratively refines a prompt using a refinement function.

    The refinement function receives the current prompt and returns a new
    prompt along with metadata describing whether an improvement was
    achieved. Optional scores allow the generator to detect plateaus and
    stop when progress stalls.
    """

    def __init__(self, max_iters: int = 5, *, min_score_delta: float | None = None) -> None:
        if max_iters < 1:
            raise ValueError("max_iters must be positive")
        self.max_iters = max_iters
        self.min_score_delta = min_score_delta
        self.last_history: RefinementHistory | None = None

    def _normalize_step(self, candidate: RefinementReturn) -> RefinementStep:
        if isinstance(candidate, RefinementStep):
            return candidate
        if not isinstance(candidate, tuple):
            raise TypeError("refine_func must return a tuple or RefinementStep")
        length = len(candidate)
        if length == 2:
            prompt, improved = candidate
            feedback = None
            score = None
        elif length == 3:
            prompt, improved, feedback = candidate
            score = None
        elif length == 4:
            prompt, improved, feedback, score = candidate
        else:
            raise TypeError("refine_func returned an unexpected tuple length")
        if not isinstance(prompt, str):
            raise TypeError("refine_func must return prompt text as a string")
        if feedback is not None and not isinstance(feedback, str):
            feedback = str(feedback)
        normalized_score: float | None
        if score is None:
            normalized_score = None
        else:
            try:
                normalized_score = float(score)
            except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
                raise TypeError("score values must be numeric") from exc
        return RefinementStep(
            prompt=prompt,
            improved=bool(improved),
            feedback=feedback,
            score=normalized_score,
        )

    def generate(
        self,
        prompt: str,
        refine_func: Callable[[str], RefinementReturn],
        *,
        return_history: bool = False,
    ) -> str | Tuple[str, RefinementHistory]:
        """Run the self-looping refinement process.

        Parameters
        ----------
        prompt:
            Initial prompt to refine.
        refine_func:
            Callable that receives the current prompt and returns
            :class:`RefinementStep` metadata describing the outcome.
        return_history:
            When ``True`` the method also returns the full
            :class:`RefinementHistory` for post-analysis.
        """

        history = RefinementHistory(steps=[RefinementStep(prompt=prompt, improved=False)])
        previous_step = history.steps[-1]
        for _ in range(self.max_iters):
            step = self._normalize_step(refine_func(previous_step.prompt))
            if (
                self.min_score_delta is not None
                and step.score is not None
                and previous_step.score is not None
                and step.score - previous_step.score < self.min_score_delta
            ):
                if not step.feedback:
                    step.feedback = "minimum score delta not reached"
                step.improved = False
                history.steps.append(step)
                break
            history.steps.append(step)
            if not step.improved:
                break
            previous_step = step
        else:
            # Max iterations reached; record a sentinel step to show termination.
            history.steps.append(
                RefinementStep(
                    prompt=previous_step.prompt,
                    improved=False,
                    feedback="maximum iterations reached",
                    score=previous_step.score,
                )
            )
        self.last_history = history
        final_prompt = history.final_prompt
        if return_history:
            return final_prompt, history
        return final_prompt
