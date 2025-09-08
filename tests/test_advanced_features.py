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

    result = gen.generate("start", refine)
    assert result == "start done done done"


def test_run_federated_evaluation():
    prompts = ["a", "bb", "ccc"]
    results = run_federated_evaluation(prompts, lambda p: len(p), shards=2)
    assert results == [1, 2, 3]


def test_rlhf_trainer():
    def reward(prompt: str, feedback: str) -> float:
        return 1.0 if feedback == "good" else -1.0

    def feedback_provider(prompt: str) -> str:
        return "good" if "keep" in prompt else "bad"

    trainer = RLHFTrainer(reward_func=reward)
    trained = trainer.train(["keep this", "drop that"], feedback_provider)
    assert trained == ["keep this"]


def test_filter_clinical_content():
    with pytest.raises(ValueError):
        filter_clinical_content("This is medical advice.")
    assert filter_clinical_content("General guidance") == "General guidance"
