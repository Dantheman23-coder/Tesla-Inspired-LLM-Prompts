from pathlib import Path
from teslamind.prompt import Prompt


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
