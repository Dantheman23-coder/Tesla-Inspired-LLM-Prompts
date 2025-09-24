# Advanced Features

TeslaMind includes experimental modules that demonstrate how the prompt
library can be extended with iterative refinement, federated evaluation,
feedback-driven learning, and safety tooling. The helpers are intentionally
small so they can be copied into your own codebase or composed with more
elaborate workflows.

## Self-looping refinement
Use `SelfLoopingPromptGenerator` to iteratively refine prompts, enforce
minimum score deltas, and inspect structured `RefinementHistory` data. The
history object now exposes convenience helpers for diagnostics, such as
`improvements()` and `stop_reason`.

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
`RefinementHistory` for post-run inspection. When you only need the final
prompt, omit `return_history=True` to avoid allocating the history object.

**When to use**

- You want to quantify how much a refinement function improves prompts.
- You need to halt automatically when a scoring metric plateaus.

**Key arguments**

- `max_iters`: Hard limit on refinement passes. The generator appends a
  sentinel step when the limit is reached so the stop reason is explicit.
- `min_score_delta`: Guardrail against tiny improvements. When set, the
  generator stops as soon as the delta between consecutive scores fails to
  reach the threshold.
- `return_history`: Toggles whether a `RefinementHistory` object should be
  returned alongside the final prompt for auditing.

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

**When to use**

- You need deterministic batch boundaries for evaluation results.
- You are planning to swap in a distributed backend later and want a small,
  inspectable shim today.

**Key arguments**

- `shards`/`shard_size`: Control how prompts are partitioned. Setting
  `shard_size` gives you deterministic chunk sizes regardless of the number of
  prompts.
- `aggregate`: Optional reducer applied to the flattened results. Combine it
  with `aggregate_default` to provide a fallback value when no prompts are
  supplied.
- `with_metadata`: Return the full `FederatedEvaluationReport` so you can
  inspect shard-level outcomes via helpers such as `prompts()` and
  `shard_count`.

## RLHF trainer
`RLHFTrainer` records detailed `FeedbackEvent` metadata, keeps an
append-only history of training runs, and returns a `TrainingSummary` with
accepted prompts and aggregate statistics. Summaries expose acceptance rates
and serialized representations for downstream logging.

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
return a `SafetyReport` detailing every violation. Reporting works even when
masking is disabled so you can audit flagged content before deciding how to
handle it. The helper can now run in case-sensitive mode and reports expose a
violation count plus the set of blocked terms detected.

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

**When to use**

- You are experimenting with prompts that might contain sensitive clinical
  language and want a low-friction guardrail.
- You need to log detailed metadata about which terms were masked to justify
  downstream decisions.

**Key arguments**

- `blocked_terms`: Iterable of terms to detect. You can merge the default
  TeslaMind terms with your own domain-specific vocabulary.
- `mask`/`mask_char`: Toggle masking behavior and customize the mask character.
- `report`: Switch between strict validation (raises on violations) and a
  metadata-rich report that can be inspected before enforcing a policy.
- `case_sensitive`: Control whether matching respects the original case of the
  text and blocked terms.

These modules are reference implementations meant for experimentation and can
be expanded into full-featured components as your workflow evolves.
