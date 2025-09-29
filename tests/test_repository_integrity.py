from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _iter_project_files():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        yield path, text


def test_repository_contains_no_conflict_markers():
    conflict_markers = []
    conflict_strings = {"<" * 7, ">" * 7}
    for path, text in _iter_project_files():
        if any(marker in text for marker in conflict_strings):
            conflict_markers.append(path.relative_to(REPO_ROOT))
    assert not conflict_markers, f"Conflict markers present in: {conflict_markers}"


def test_no_legacy_advanced_module_duplicates():
    legacy_paths = {
        Path(name)
        for name in ("refinement.py", "federated.py", "rlhf.py", "safety.py")
    }
    top_level_files = {path.name for path in REPO_ROOT.glob("*.py")}
    duplicates = legacy_paths.intersection(top_level_files)
    assert not duplicates, f"Legacy helper files should not exist at repo root: {sorted(duplicates)}"
