from teslamind import cli


def test_list_prompts(capsys):
    cli.list_prompts()
    captured = capsys.readouterr()
    assert "prompt1" in captured.out
    assert "prompt2" in captured.out
    assert "prompt3" in captured.out
    assert "prompt4" in captured.out
