# Advanced Features

TeslaMind includes experimental modules that demonstrate how the prompt library
can be extended. All helpers are re-exported from `teslamind.advanced` and from
the package root for convenience.

## Self-looping refinement

Use `SelfLoopingPromptGenerator` to iteratively refine prompts. Set
`return_history=True` to capture iteration metadata for debugging.

```python
from teslamind import SelfLoopingPromptGenerator

def refine(p: str) -> tuple[str, bool]:
    return p + " done", len(p.split()) < 4

final_prompt, history = SelfLoopingPromptGenerator(max_iters=3).generate(
    "start", refine, return_history=True
)
print(final_prompt)
print(history.steps)
```

## Federated evaluation

`run_federated_evaluation` evaluates prompts across logical shards and can
return structured `FederatedShardResult` records to surface shard-level
outcomes.

```python
from teslamind import run_federated_evaluation

results, shard_history = run_federated_evaluation(
    ["a", "bb", "ccc"], len, shards=2, return_shard_results=True
)
```

## RLHF trainer

`RLHFTrainer` keeps prompts whose reward meets a configurable threshold and can
return a sequence of `RLHFResult` entries for offline analysis.

```python
from teslamind import RLHFTrainer

def reward(prompt: str, feedback: str) -> float:
    return 1.0 if feedback == "keep" else -1.0

trainer = RLHFTrainer(reward, threshold=0.5)
kept, history = trainer.train(
    ["keep this", "drop that"],
    lambda prompt: "keep" if "keep" in prompt else "drop",
    return_history=True,
)
```

## Clinical safety filter

`filter_clinical_content` blocks configurable medical terms. To retain the
content with redactions, pass `mask=True` or call `mask_sensitive_terms`
directly.

```python
from teslamind import filter_clinical_content, mask_sensitive_terms

filter_clinical_content("This is general guidance")
mask_sensitive_terms("Seek medical advice")
```

These modules are stubs intended for experimentation and can be expanded into
full-featured implementations.
