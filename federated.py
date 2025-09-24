"""Compatibility re-export for the federated evaluation helpers."""

from teslamind.federated import (  # noqa: F401
    EvaluationRecord,
    FederatedEvaluationReport,
    run_federated_evaluation,
)

__all__ = [
    "run_federated_evaluation",
    "FederatedEvaluationReport",
    "EvaluationRecord",
]
