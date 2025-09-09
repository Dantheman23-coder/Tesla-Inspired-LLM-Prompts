# Advanced Features

TeslaMind includes experimental modules that demonstrate how the prompt
library can be extended.

## Self-looping refinement
Use `SelfLoopingPromptGenerator` to iteratively refine prompts and inspect
their evolution.

```python
from teslamind import SelfLoopingPromptGenerator

def refine(p: str) -> tuple[str, bool]:
    if "done" in p:
        return p, False
    return p + " done", True

result, history = SelfLoopingPromptGenerator(max_iters=3).generate(
    "start", refine, return_history=True
)
```

## Federated evaluation
`run_federated_evaluation` evaluates prompts across logical shards.

```python
from teslamind import run_federated_evaluation
run_federated_evaluation(["a", "bb", "ccc"], len, shards=2)
```

## RLHF trainer
`RLHFTrainer` keeps only prompts with reward above a configurable threshold
and records the latest reward values.

```python
from teslamind import RLHFTrainer
trainer = RLHFTrainer(lambda p, f: 1.0 if f == "good" else -1.0, threshold=0.5)
trainer.train(["keep this", "drop that"], lambda p: "good")
trainer.last_rewards  # [1.0, -1.0]
```

## Clinical safety filter
`filter_clinical_content` blocks configurable medical terms and can optionally
mask them.

```python
from teslamind import filter_clinical_content
filter_clinical_content("Diagnosis confirmed", mask=True)
```
These modules are simple reference implementations meant for experimentation
and can be expanded into full-featured components.
