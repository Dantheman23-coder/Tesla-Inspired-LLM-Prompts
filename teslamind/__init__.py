"""TeslaMind core package.

This module re-exports the public APIs used throughout the documentation so
consumers can rely on a single import location. Advanced helpers such as
self-looping refinement, federated evaluation, RLHF training, and clinical
safety filtering are exposed alongside the core prompt abstractions.
"""

from .version import __version__
from .prompt import Prompt, compose_prompt
from .persona import Persona, get_persona, list_personas
from .refinement import (
    SelfLoopingPromptGenerator,
    RefinementHistory,
    RefinementStep,
)
from .federated import (
    run_federated_evaluation,
    FederatedEvaluationReport,
    EvaluationRecord,
)
from .modes import (
    Mode,
    get_mode,
    list_modes,
    coop_prompt,
    energy_prompt,
    hyperscience_prompt,
    invention_prompt,
    patent_prompt,
    visionary_prompt,
)
from .rlhf import RLHFTrainer, FeedbackEvent, TrainingSummary
from .safety import (
    DEFAULT_BLOCKED_TERMS,
    filter_clinical_content,
    SafetyReport,
    SafetyViolation,
)

__all__ = [
    "Prompt",
    "Persona",
    "__version__",
    "compose_prompt",
    "list_personas",
    "get_persona",
    "Mode",
    "list_modes",
    "get_mode",
    "energy_prompt",
    "patent_prompt",
    "invention_prompt",
    "visionary_prompt",
    "hyperscience_prompt",
    "coop_prompt",
    "SelfLoopingPromptGenerator",
    "RefinementHistory",
    "RefinementStep",
    "run_federated_evaluation",
    "FederatedEvaluationReport",
    "EvaluationRecord",
    "RLHFTrainer",
    "FeedbackEvent",
    "TrainingSummary",
    "filter_clinical_content",
    "SafetyReport",
    "SafetyViolation",
    "DEFAULT_BLOCKED_TERMS",
]
