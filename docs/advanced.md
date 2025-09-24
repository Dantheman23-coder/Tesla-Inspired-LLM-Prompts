# Advanced Workflows

TeslaMind includes a set of experimental helpers that mirror the way Tesla
relentlessly iterated on ideas. They are focused on rapid experimentation rather
than production deployments.

## Self-looping refinement

`SelfLoopingPromptRefiner` repeatedly calls a refinement function and stores each
iteration. Provide a callable that returns a new prompt (optionally with a
metadata dictionary containing a `score`).

```python
from teslamind.advanced import SelfLoopingPromptRefiner

refiner = SelfLoopingPromptRefiner(
    lambda prompt: (prompt + " ⚡", {"score": len(prompt)})
)
final_prompt, history = refiner.refine("Prototype", return_history=True)
```

## Federated evaluation

`FederatedEvaluator` coordinates evaluation across logical shards. Pass a
function that scores a collection of prompts and receive shard level metrics plus
an aggregate view.

```python
from teslamind.advanced import FederatedEvaluator

def evaluate(prompts):
    return {"avg_length": sum(len(p) for p in prompts) / len(prompts)}

evaluator = FederatedEvaluator(evaluate)
result = evaluator.evaluate({"lab": ["coil", "transformer"]})
```

## RLHF training stub

`RLHFTrainer` applies reward signals from human feedback or heuristics to decide
which prompts to keep. Rewards above the configured threshold are accepted; all
observations are stored for later analysis.

```python
from teslamind.advanced import RLHFTrainer

trainer = RLHFTrainer(lambda prompt: 1.0 if "⚡" in prompt else 0.0, reward_threshold=0.5)
rlhf_result = trainer.train(["coil", "coil ⚡"])
```

## Clinical safety filter

`ClinicalSafetyFilter` detects potentially sensitive medical terminology. It can
optionally mask matched phrases or raise an error when a term appears.

## Legacy import paths

Earlier versions exposed each helper from dedicated modules (for example,
`teslamind.refinement` or a repository-root `refinement.py`). Those entry points
are still available as thin wrappers around `teslamind.advanced` so existing
automation continues to function. New development should prefer importing from
`teslamind.advanced` directly.

```python
from teslamind.advanced import ClinicalSafetyFilter

filter_ = ClinicalSafetyFilter(["diagnosis"], mask=True)
report = filter_.scan("Initial diagnosis pending")
```
