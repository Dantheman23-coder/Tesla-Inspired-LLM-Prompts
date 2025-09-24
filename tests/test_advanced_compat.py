from teslamind import (
    ClinicalSafetyFilter,
    FederatedEvaluator,
    RLHFTrainer,
    SelfLoopingPromptRefiner,
)
from teslamind.federated import FederatedEvaluation, ShardReport
from teslamind.refinement import RefineFunction, RefineOutput, RefinementStep
from teslamind.rlhf import RLHFTrainingResult, RewardRecord
from teslamind.safety import SafetyReport, SafetyViolation


def test_legacy_modules_reexport_helpers():
    assert RefineFunction
    assert RefineOutput
    assert RefinementStep
    assert isinstance(ShardReport(shard="lab", prompts=[], metrics={}), ShardReport)
    assert isinstance(FederatedEvaluation(reports=[], aggregate={}), FederatedEvaluation)
    assert isinstance(RLHFTrainingResult(accepted=[], rejected=[], history=[]), RLHFTrainingResult)
    assert isinstance(RewardRecord(prompt="", reward=0.0), RewardRecord)
    assert isinstance(SafetyViolation(term="x", start=0, end=1), SafetyViolation)
    assert isinstance(SafetyReport(original_text="", sanitized_text="", violations=[]), SafetyReport)
    # Access top-level exports to ensure __all__ wiring stays intact.
    assert ClinicalSafetyFilter
    assert FederatedEvaluator
    assert RLHFTrainer
    assert SelfLoopingPromptRefiner
