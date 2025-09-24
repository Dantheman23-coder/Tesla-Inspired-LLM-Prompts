# Personas

Personas provide perspective for prompts. Each persona wraps tasks with a
distinct voice, priorities, and guardrails.

## Quick reference

| Persona slug | Persona | Perspective |
| --- | --- | --- |
| `visionary-inventor` | Visionary Inventor | Ambitious moonshot storytelling grounded in Tesla’s ethos |
| `practical-engineer` | Practical Engineer | Constraint-aware builder obsessed with instrumentation |
| `curious-student` | Curious Student | Inquisitive learner who unpacks concepts in layers |

## CLI usage

- `teslamind personas list` — List available personas.
- `teslamind personas show curious-student` — Print the persona system prompt.

## Python usage

```python
from teslamind.persona import get_persona

persona = get_persona("practical-engineer")
print(persona.system_prompt())
print(persona.apply("Draft the integration plan"))
```

Combine personas with stylistic modes using `teslamind compose` or the
`compose_prompt` helper described in the README.
