from teslamind.modes import get_mode, list_modes
from teslamind.persona import get_persona, list_personas


def test_mode_catalog_contains_energy():
    slugs = [mode.slug for mode in list_modes()]
    assert "energy" in slugs
    mode = get_mode("energy")
    assert "Energy Mode" in mode.summary()
    rendered = mode.apply("Stabilize wireless transfer")
    assert rendered.startswith("[Energy Mode] Stabilize wireless transfer")
    assert "Style commitments" in rendered


def test_persona_catalog_contains_curiosity():
    slugs = [persona.slug for persona in list_personas()]
    assert "curious-student" in slugs
    persona = get_persona("curious-student")
    system_prompt = persona.system_prompt()
    assert "Curious Student" in system_prompt
    rendered = persona.apply("Explain resonance")
    assert "Task:" in rendered
    assert "Explain resonance" in rendered
