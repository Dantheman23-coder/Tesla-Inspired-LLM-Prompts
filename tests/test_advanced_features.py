import pytest

from teslamind import (
    DEFAULT_BLOCKED_TERMS,
    EvaluationRecord,
    FeedbackEvent,
    FederatedEvaluationReport,
    RLHFTrainer,
    RefinementHistory,
    RefinementStep,
    SafetyReport,
    SafetyViolation,
    SelfLoopingPromptGenerator,
    TrainingSummary,
    filter_clinical_content,
    run_federated_evaluation,
)

from federated import (  # type: ignore  # legacy import path
    EvaluationRecord as LegacyEvaluationRecord,
    FederatedEvaluationReport as LegacyFederatedEvaluationReport,
    run_federated_evaluation as legacy_run_federated_evaluation,
)
from refinement import (  # type: ignore  # legacy import path
    RefinementHistory as LegacyRefinementHistory,
    RefinementStep as LegacyRefinementStep,
    SelfLoopingPromptGenerator as LegacySelfLoopingPromptGenerator,
)
from rlhf import (  # type: ignore  # legacy import path
    FeedbackEvent as LegacyFeedbackEvent,
    RLHFTrainer as LegacyRLHFTrainer,
    TrainingSummary as LegacyTrainingSummary,
)
from safety import (  # type: ignore  # legacy import path
    DEFAULT_BLOCKED_TERMS as LEGACY_DEFAULT_BLOCKED_TERMS,
    SafetyReport as LegacySafetyReport,
    SafetyViolation as LegacySafetyViolation,
    filter_clinical_content as legacy_filter_clinical_content,
)


def test_self_looping_prompt_generator_tracks_history():
    generator = SelfLoopingPromptGenerator(max_iters=5, min_score_delta=0.1)

    def refine(prompt: str):
        count = prompt.count("done")
        if count >= 2:
            return prompt, False, "complete", float(count)
        return (prompt + " done", True, "continue", float(count + 1))

    final_prompt, history = generator.generate(
        "start", refine, return_history=True
    )
    assert final_prompt == "start done done"
    assert history.iterations == 3  # initial + two improvements + stop step
    assert history.total_improvements == 2
    assert history.prompts()[0] == "start"
    assert history.prompts()[-1] == final_prompt
    assert generator.last_history is history
    assert [step.prompt for step in history.improvements()] == [
        "start done",
        "start done done",
    ]
    assert history.stop_reason == "complete"


def test_run_federated_evaluation_with_metadata():
    prompts = ["a", "bb", "ccc", "dddd"]
    report = run_federated_evaluation(
        prompts,
        len,
        shards=2,
        aggregate=sum,
        with_metadata=True,
    )
    assert report.flatten() == [1, 2, 3, 4]
    assert report.aggregate == 10
    grouped = report.by_shard()
    assert set(grouped) == {0, 1}
    assert [record.prompt for record in grouped[0]] == ["a", "bb"]
    assert len(report) == len(prompts)
    assert report.prompts() == prompts
    assert report.shard_count == 2
    # Convenience mode without metadata still returns flattened results
    no_metadata = run_federated_evaluation(prompts, len, shards=2)
    assert no_metadata == [1, 2, 3, 4]


def test_run_federated_evaluation_handles_empty_prompts():
    def explode(_: list[int]) -> int:
        raise AssertionError("aggregate should not be invoked for empty input")

    report = run_federated_evaluation(
        [],
        len,
        shards=3,
        aggregate=explode,
        aggregate_default=0,
        with_metadata=True,
    )
    assert isinstance(report, FederatedEvaluationReport)
    assert len(report) == 0
    assert report.aggregate == 0
    assert report.flatten() == []


def test_rlhf_trainer_summary_and_history():
    def reward(prompt: str, feedback: str) -> float:
        return 1.0 if feedback == "keep" else -1.0

    def feedback_provider(prompt: str) -> str:
        return "keep" if "keep" in prompt else "drop"

    trainer = RLHFTrainer(reward_func=reward, threshold=0.5)
    summary = trainer.train(
        ["keep this", "drop that", "keep too"],
        feedback_provider,
        return_summary=True,
    )
    assert summary.accepted_prompts == ["keep this", "keep too"]
    assert summary.rejected_prompts == ["drop that"]
    assert pytest.approx(summary.average_reward, rel=1e-6) == (1 - 1 + 1) / 3
    assert trainer.last_rewards == [1.0, -1.0, 1.0]
    assert trainer.history[-1] is summary
    summary_dict = summary.to_dict()
    assert summary_dict["average_reward"] == pytest.approx(summary.average_reward)
    assert len(summary_dict["events"]) == 3
    assert summary.rewards == [1.0, -1.0, 1.0]
    assert pytest.approx(summary.acceptance_rate, rel=1e-6) == 2 / 3
    assert summary_dict["acceptance_rate"] == summary.acceptance_rate
    assert summary_dict["accepted_prompts"] == summary.accepted_prompts
    assert summary_dict["rejected_prompts"] == summary.rejected_prompts
    assert trainer.last_summary is summary


def test_filter_clinical_content_reports_multiple_matches():
    with pytest.raises(ValueError):
        filter_clinical_content("This is medical advice.")
    report = filter_clinical_content(
        "Diagnosis confirmed. Another diagnosis requires treatment.",
        mask=True,
        report=True,
    )
    assert report.masked is True
    assert report.text.lower().count("diagnosis") == 0
    assert report.text.lower().count("treatment") == 0
    assert len(report.violations) == 3
    assert report.violation_count == 3
    assert report.has_violations() is True
    assert report.blocked_terms == {"diagnosis", "treatment"}
    assert any(violation.span()[0] == 0 for violation in report.violations)
    assert filter_clinical_content("General guidance") == "General guidance"


def test_filter_clinical_content_reports_without_masking():
    report = filter_clinical_content(
        "Seek treatment before offering diagnosis.",
        mask=False,
        report=True,
    )
    assert report.masked is False
    assert report.text == "Seek treatment before offering diagnosis."
    assert {violation.term for violation in report.violations} == {
        "treatment",
        "diagnosis",
    }
    assert report.violation_count == 2


def test_filter_clinical_content_case_sensitive_toggle():
    assert "diagnosis" in DEFAULT_BLOCKED_TERMS
    insensitive = filter_clinical_content(
        "diagnosis requires treatment.",
        blocked_terms=["Diagnosis"],
        report=True,
    )
    assert insensitive.violation_count == 1

    case_sensitive_none = filter_clinical_content(
        "diagnosis requires treatment.",
        blocked_terms=["Diagnosis"],
        report=True,
        case_sensitive=True,
    )
    assert case_sensitive_none.violation_count == 0

    case_sensitive_match = filter_clinical_content(
        "Diagnosis requires treatment.",
        blocked_terms=["Diagnosis"],
        report=True,
        case_sensitive=True,
    )
    assert case_sensitive_match.violation_count == 1
    assert case_sensitive_match.violations[0].match == "Diagnosis"


def test_legacy_imports_resolve_to_package_implementations():
    assert LegacySelfLoopingPromptGenerator is SelfLoopingPromptGenerator
    assert LegacyRefinementHistory is RefinementHistory
    assert LegacyRefinementStep is RefinementStep

    assert legacy_run_federated_evaluation is run_federated_evaluation
    assert LegacyFederatedEvaluationReport is FederatedEvaluationReport
    assert LegacyEvaluationRecord is EvaluationRecord

    assert LegacyRLHFTrainer is RLHFTrainer
    assert LegacyFeedbackEvent is FeedbackEvent
    assert LegacyTrainingSummary is TrainingSummary

    assert legacy_filter_clinical_content is filter_clinical_content
    assert LEGACY_DEFAULT_BLOCKED_TERMS is DEFAULT_BLOCKED_TERMS
    assert LegacySafetyReport is SafetyReport
    assert LegacySafetyViolation is SafetyViolation
