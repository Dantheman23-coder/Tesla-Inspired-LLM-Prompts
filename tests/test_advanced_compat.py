from importlib import import_module

import pytest

LEGACY_PATHS = [
    ("teslamind.refinement", "SelfLoopingPromptRefiner"),
    ("teslamind.federated", "FederatedEvaluator"),
    ("teslamind.rlhf", "RLHFTrainer"),
    ("teslamind.safety", "ClinicalSafetyFilter"),
]

ROOT_PATHS = [
    ("refinement", "SelfLoopingPromptRefiner"),
    ("federated", "FederatedEvaluator"),
    ("rlhf", "RLHFTrainer"),
    ("safety", "ClinicalSafetyFilter"),
]


@pytest.mark.parametrize("module_path, symbol", LEGACY_PATHS)
def test_package_level_compatibility(module_path, symbol):
    advanced = import_module("teslamind.advanced")
    legacy_module = import_module(module_path)

    assert getattr(legacy_module, symbol) is getattr(advanced, symbol)


@pytest.mark.parametrize("module_path, symbol", ROOT_PATHS)
def test_repository_root_shims(module_path, symbol):
    package_module = import_module(f"teslamind.{module_path}")
    root_module = import_module(module_path)

    assert getattr(root_module, symbol) is getattr(package_module, symbol)
