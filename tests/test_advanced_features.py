import pytest

from teslamind import (
    FederatedShardResult,
    RLHFTrainer,
    RLHFResult,
    RefinementHistory,
    SelfLoopingPromptGenerator,
    filter_clinical_content,
    mask_sensitive_terms,
    run_federated_evaluation,
)


def test_self_looping_prompt_generator_history():
    gen = SelfLoopingPromptGenerator(max_iters=3)

    def refine(prompt: str):
        if prompt.count("done") >= 2:
            return prompt, False
        return prompt + " done", True

    result, history = gen.generate("start", refine, return_history=True)
    assert isinstance(history, RefinementHistory)
    assert history.iterations == 3
    assert history.stopped_reason == "no_improvement"
    assert result.endswith("done done")
    assert history.steps[-1] == result


def test_run_federated_evaluation_with_history():
    prompts = ["a", "bb", "ccc"]
    results, shard_results = run_federated_evaluation(
        prompts,
        lambda p: len(p),
        shards=2,
        return_shard_results=True,
    )
    assert results == [1, 2, 3]
    assert all(isinstance(record, FederatedShardResult) for record in shard_results)
    assert sum(len(r.prompts) for r in shard_results) == len(prompts)


def test_rlhf_trainer():
    def reward(prompt: str, feedback: str) -> float:
        return 1.0 if feedback == "good" else -1.0

    def feedback_provider(prompt: str) -> str:
        return "good" if "keep" in prompt else "bad"

    trainer = RLHFTrainer(reward_func=reward, threshold=0.5)
    trained, history = trainer.train(
        ["keep this", "drop that"], feedback_provider, return_history=True
    )
    assert trained == ["keep this"]
    assert all(isinstance(entry, RLHFResult) for entry in history)
    assert history[0].reward == 1.0


def test_filter_clinical_content():
    with pytest.raises(ValueError):
        filter_clinical_content("This is medical advice.")
    masked = filter_clinical_content("Seek medical advice", mask=True)
    assert "[REDACTED]" in masked
    assert mask_sensitive_terms("treatment plan") == "[REDACTED] plan"
