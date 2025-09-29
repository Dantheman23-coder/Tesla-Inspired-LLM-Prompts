from pathlib import Path

import pytest

from teslamind import cli


def test_list_prompts(capsys):
    cli.list_prompts()
    captured = capsys.readouterr()
    assert "prompt1" in captured.out
    assert "prompt2" in captured.out


def test_list_developer_prompts(capsys):
    cli.list_prompts(developer=True)
    captured = capsys.readouterr()
    assert "reward_audit" in captured.out
    assert "safety_review" in captured.out


def test_show_prompt_user(tmp_path: Path, monkeypatch, capsys):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    (prompt_dir / "demo.txt").write_text("demo")
    monkeypatch.setattr(cli, "PROMPT_DIR", prompt_dir)
    monkeypatch.setattr(cli, "DEVELOPER_DIR", prompt_dir / "developer")
    cli.show_prompt("demo")
    captured = capsys.readouterr()
    assert captured.out.strip() == "demo"


def test_show_prompt_missing(monkeypatch):
    monkeypatch.setattr(cli, "PROMPT_DIR", Path("/nonexistent"))
    monkeypatch.setattr(cli, "DEVELOPER_DIR", Path("/nonexistent"))
    with pytest.raises(SystemExit):
        cli.show_prompt("unknown")
