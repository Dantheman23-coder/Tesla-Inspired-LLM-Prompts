import pytest

from teslamind.advanced import (
    ClinicalSafetyFilter,
    FederatedEvaluator,
    RLHFTrainer,
    SelfLoopingPromptRefiner,
)


def test_self_looping_prompt_refiner_tracks_history():
    def refine(prompt: str):
        return prompt + "!", {"score": len(prompt)}

    refiner = SelfLoopingPromptRefiner(refine, max_iterations=5, score_threshold=5)
    final_prompt, history = refiner.refine("go", return_history=True)

    assert final_prompt.endswith("!")
    assert history[-1].score is not None
    assert history[-1].score >= 5
    assert len(history) <= 5


def test_federated_evaluator_averages_numeric_metrics():
    def evaluator(prompts):
        return {"avg_length": sum(len(p) for p in prompts) / len(prompts)}

    evaluator_instance = FederatedEvaluator(evaluator)
    result = evaluator_instance.evaluate({
        "lab": ["coil", "transformer"],
        "field": ["resonance"],
    })

    assert result.aggregate["avg_length"] == pytest.approx(
        (
            (len("coil") + len("transformer")) / 2
            + len("resonance")
        )
        / 2
    )
    assert len(result.reports) == 2


def test_rlhf_trainer_filters_prompts_by_reward():
    trainer = RLHFTrainer(lambda prompt: 1.0 if "⚡" in prompt else 0.0, reward_threshold=0.5)
    prompts = ["coil", "coil ⚡"]

    result = trainer.train(prompts)

    assert result.accepted == ["coil ⚡"]
    assert result.rejected == ["coil"]
    assert [record.prompt for record in result.history] == prompts


def test_clinical_safety_filter_masks_terms():
    filter_ = ClinicalSafetyFilter(["diagnosis"], mask=True, mask_char="*")
    report = filter_.scan("Initial diagnosis pending")

    assert not report.is_clean
    assert report.sanitized_text.startswith("Initial ")
    assert "******" in report.sanitized_text


def test_clinical_safety_filter_can_raise_on_violation():
    filter_ = ClinicalSafetyFilter(["diagnosis"], raise_on_violation=True)

    with pytest.raises(ValueError):
        filter_.scan("Initial diagnosis pending")
