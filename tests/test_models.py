from teslamind.models import PromptMeta, Score


def test_score():
    s = Score(value=1.0, rubric="clarity")
    assert s.value == 1.0


def test_prompt_meta():
    pm = PromptMeta(title="t", version="1", prompt_path="x")
    assert pm.title == "t"
