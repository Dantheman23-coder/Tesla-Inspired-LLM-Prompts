# Advanced Features

TeslaMind includes experimental modules that demonstrate how the prompt
library can be extended with iterative refinement, federated evaluation,
feedback-driven learning, and safety tooling.

## Self-looping refinement
Use `SelfLoopingPromptGenerator` to iteratively refine prompts, enforce
minimum score deltas, and inspect structured `RefinementHistory` data.

```python
from teslamind import SelfLoopingPromptGenerator

def refine(prompt: str):
    score = prompt.count("!")
    if score >= 3:
        return prompt, False, "sufficient emphasis", score
    return prompt + "!", True, "add emphasis", score + 1

final_prompt, history = SelfLoopingPromptGenerator(
    max_iters=5, min_score_delta=0.1
).generate("Plan", refine, return_history=True)
final_prompt  # "Plan!!!"
history.total_improvements  # 3
history.prompts()  # ["Plan", "Plan!", "Plan!!", "Plan!!!", "Plan!!!"]
```

`SelfLoopingPromptGenerator.last_history` stores the most recent
`RefinementHistory` for post-run inspection.

## Federated evaluation
`run_federated_evaluation` evaluates prompts across logical shards and can
return a `FederatedEvaluationReport` with shard metadata and aggregate metrics.

```python
from teslamind import run_federated_evaluation

prompts = ["alpha", "beta", "gamma", "delta"]
report = run_federated_evaluation(
    prompts,
    len,
    shards=2,
    aggregate=sum,
    with_metadata=True,
)
report.aggregate  # 18
report.by_shard()[0][0].prompt  # "alpha"
report.flatten()  # [5, 4, 5, 5]
```

When `with_metadata` is `False` the helper returns only the flattened list of
results for convenience.

## RLHF trainer
`RLHFTrainer` records detailed `FeedbackEvent` metadata, keeps an
append-only history of training runs, and returns a `TrainingSummary` with
accepted prompts and aggregate statistics.

```python
from teslamind import RLHFTrainer

trainer = RLHFTrainer(lambda p, f: 1.0 if f == "keep" else -1.0, threshold=0.5)
summary = trainer.train(
    ["keep this", "drop that"],
    lambda prompt: "keep" if "keep" in prompt else "drop",
    return_summary=True,
)
summary.accepted_prompts  # ["keep this"]
summary.average_reward  # 0.0
trainer.last_rewards  # [1.0, -1.0]
```

## Clinical safety filter
`filter_clinical_content` blocks or masks configurable medical terms and can
return a `SafetyReport` detailing every violation.

```python
from teslamind import filter_clinical_content

report = filter_clinical_content(
    "Diagnosis confirmed; seek treatment immediately.",
    mask=True,
    report=True,
)
report.text  # "********* confirmed; seek ********* immediately."
{v.match for v in report.violations}  # {"Diagnosis", "treatment"}
```

These modules are reference implementations meant for experimentation and can
be expanded into full-featured components as your workflow evolves.
