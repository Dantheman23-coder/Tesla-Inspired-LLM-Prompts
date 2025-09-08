# Advanced Features

TeslaMind includes experimental modules that demonstrate how the prompt
library can be extended.

## Self-looping refinement
Use `SelfLoopingPromptGenerator` to iteratively refine prompts.

```python
from teslamind import SelfLoopingPromptGenerator

def refine(p: str) -> tuple[str, bool]:
    return p + " done", False

SelfLoopingPromptGenerator(max_iters=3).generate("start", refine)
```

## Federated evaluation
`run_federated_evaluation` evaluates prompts across logical shards.

```python
from teslamind import run_federated_evaluation
run_federated_evaluation(["a", "bb"], len, shards=2)
```

## RLHF trainer
`RLHFTrainer` keeps only prompts with positive reward.

```python
from teslamind import RLHFTrainer
trainer = RLHFTrainer(lambda p, f: 1.0 if f == "good" else -1.0)
trainer.train(["keep this", "drop that"], lambda p: "good")
```

## Clinical safety filter
`filter_clinical_content` blocks configurable medical terms.

```python
from teslamind import filter_clinical_content
filter_clinical_content("General guidance")
```

These modules are stubs intended for experimentation and can be expanded
into full-featured implementations.
