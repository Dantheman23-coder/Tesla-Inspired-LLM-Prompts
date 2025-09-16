import pytest

from teslamind import (
    SelfLoopingPromptGenerator,
    run_federated_evaluation,
    RLHFTrainer,
    filter_clinical_content,
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
    # Convenience mode without metadata still returns flattened results
    no_metadata = run_federated_evaluation(prompts, len, shards=2)
    assert no_metadata == [1, 2, 3, 4]


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
    assert report.blocked_terms == {"diagnosis", "treatment"}
    assert filter_clinical_content("General guidance") == "General guidance"
