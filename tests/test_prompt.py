from pathlib import Path

import pytest

from teslamind.prompt import Prompt, compose_prompt


def test_from_file(tmp_path: Path):
    path = tmp_path / "p.txt"
    path.write_text("hi")
    p = Prompt.from_file(path)
    assert p.text == "hi"


def test_save(tmp_path: Path):
    p = Prompt(name="x", text="data")
    out = tmp_path / "x.txt"
    p.save(out)
    assert out.read_text() == "data"


def test_compose_prompt_with_mode_and_persona():
    prompt = compose_prompt(
        "Draft the inspection plan",
        persona="practical-engineer",
        mode="energy",
    )
    assert "You are the Practical Engineer" in prompt.text
    assert "[Energy Mode] Draft the inspection plan" in prompt.text
    assert prompt.name == "practical-engineer"


def test_compose_prompt_with_custom_template_and_name():
    template = "Operate with relentless clarity: {task}."
    prompt = compose_prompt(
        "Diagnose oscillations",
        mode="hyperscience",
        template=template,
        name="custom",
    )
    assert "Operate with relentless clarity: Diagnose oscillations." in prompt.text
    assert "[Hyperscience Mode] Diagnose oscillations" in prompt.text
    assert prompt.name == "custom"


def test_compose_prompt_invalid_mode(monkeypatch):
    with pytest.raises(KeyError):
        compose_prompt("Task", mode="unknown-mode")
