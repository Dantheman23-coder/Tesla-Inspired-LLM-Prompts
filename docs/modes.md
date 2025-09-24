# Modes

TeslaMind includes several stylistic modes for prompts. Each mode wraps a task
with a Tesla-inspired tone and explicit guardrails.

## Quick reference

| Mode slug | Title | Summary |
| --- | --- | --- |
| `energy` | Energy Mode | High-voltage execution with measurable impact |
| `patent` | Patent Mode | Formal disclosures with claim-ready precision |
| `invention` | Invention Mode | Divergent brainstorming with prototyping cues |
| `visionary` | Visionary Mode | Futuristic narratives tied to credible delivery |
| `hyperscience` | Hyperscience Mode | Laboratory-grade exposition and theory |
| `coop` | Cooperative Mode | Inclusive facilitation for cross-functional teams |

## CLI usage

- `teslamind modes list` — List available modes and their summaries.
- `teslamind modes show hyperscience` — Print detailed guidance.
- `teslamind modes apply energy "Stabilize wireless transfer"` — Preview the
  rendered style block.

## Python usage

```python
from teslamind.modes import get_mode

mode = get_mode("visionary")
print(mode.summary())
print(mode.apply("Design a lunar power lattice"))
```

The :class:`~teslamind.modes.catalog.Mode` object exposes `apply()` and
`summary()` helpers so you can incorporate modes in automated tooling.
