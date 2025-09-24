from teslamind import cli


def test_list_prompts(capsys):
    cli.list_prompts()
    captured = capsys.readouterr()
    lines = [line.strip() for line in captured.out.splitlines() if line.strip()]
    assert lines[:4] == ["dev_prompt_aether_engineer", "dev_prompt_dynamo_core", "dev_prompt_luminal_cartographer", "dev_prompt_magnetic_foundry"]
    assert "prompt1" in lines


def test_modes_cli(capsys):
    cli.list_modes_cli()
    listing = capsys.readouterr().out
    assert "energy" in listing
    assert "Visionary Mode" in listing

    cli.show_mode_cli("energy")
    show_output = capsys.readouterr().out
    assert "Energy Mode" in show_output
    assert "Style commitments" in show_output

    cli.apply_mode_cli("energy", "Design a resilient motor")
    applied = capsys.readouterr().out
    assert "[Energy Mode] Design a resilient motor" in applied
    assert "Translate insights" in applied


def test_persona_cli(capsys):
    cli.list_personas_cli()
    listing = capsys.readouterr().out
    assert "visionary-inventor" in listing
    assert "Practical Engineer" in listing

    cli.show_persona_cli("practical-engineer")
    detail = capsys.readouterr().out
    assert "You are the Practical Engineer" in detail
    assert "Systems integration" in detail


def test_compose_cli(capsys):
    cli.compose_cli(
        "Prototype a wireless energy bridge",
        mode="visionary",
        persona="visionary-inventor",
        template="You are smarter than Nikola Tesla in 2024. {task}",
        name=None,
    )
    output = capsys.readouterr().out
    assert "You are the Visionary Inventor" in output
    assert "Prototype a wireless energy bridge" in output
    assert "[Visionary Mode] Prototype a wireless energy bridge" in output
