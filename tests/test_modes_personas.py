from teslamind.modes import energy_prompt, visionary_prompt
from teslamind.persona import Persona


def test_energy_prompt_format():
    assert energy_prompt("analyze data").startswith("[Energy Mode]")


def test_persona_dataclass():
    persona = Persona(name="Developer", description="Builds integrations")
    assert persona.name == "Developer"
    assert "integration" in persona.description.lower()


def test_visionary_prompt_suffix():
    prompt = visionary_prompt("chart a roadmap")
    assert "roadmap" in prompt
