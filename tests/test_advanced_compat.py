from teslamind.advanced import (
    FederatedShardResult,
    RLHFResult,
    RLHFTrainer,
    RefinementHistory,
    SelfLoopingPromptGenerator,
    filter_clinical_content,
    mask_sensitive_terms,
    run_federated_evaluation,
)


def test_advanced_reexports():
    assert SelfLoopingPromptGenerator.__module__ == "teslamind.refinement"
    assert RLHFTrainer.__module__ == "teslamind.rlhf"
    assert filter_clinical_content.__module__ == "teslamind.safety"
    assert mask_sensitive_terms.__module__ == "teslamind.safety"
    assert run_federated_evaluation.__module__ == "teslamind.federated"
    assert RefinementHistory.__module__ == "teslamind.refinement"
    assert FederatedShardResult.__module__ == "teslamind.federated"
    assert RLHFResult.__module__ == "teslamind.rlhf"
