import pytest

from teslamind import (
    SelfLoopingPromptGenerator,
    run_federated_evaluation,
    RLHFTrainer,
    filter_clinical_content,
)


def test_self_looping_prompt_generator():
    gen = SelfLoopingPromptGenerator(max_iters=3)

    def refine(prompt: str):
        if prompt.count("done") >= 3:
            return prompt, False
        return prompt + " done", True

    result, history = gen.generate("start", refine, return_history=True)
    assert result == "start done done done"
    assert history[0] == "start" and history[-1] == result


def test_run_federated_evaluation():
    prompts = ["a", "bb", "ccc"]
    results = run_federated_evaluation(prompts, lambda p: len(p), shards=2)
    assert results == [1, 2, 3]


def test_rlhf_trainer():
    def reward(prompt: str, feedback: str) -> float:
        return 1.0 if feedback == "good" else -1.0

    def feedback_provider(prompt: str) -> str:
        return "good" if "keep" in prompt else "bad"

    trainer = RLHFTrainer(reward_func=reward, threshold=0.5)
    trained = trainer.train(["keep this", "drop that"], feedback_provider)
    assert trained == ["keep this"]
    assert trainer.last_rewards == [1.0, -1.0]


def test_filter_clinical_content():
    with pytest.raises(ValueError):
        filter_clinical_content("This is medical advice.")
    masked = filter_clinical_content("Diagnosis confirmed", mask=True)
    assert "diagnosis" not in masked.lower()
    assert filter_clinical_content("General guidance") == "General guidance"

