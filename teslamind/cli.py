"""Command line interface."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"
DEVELOPER_DIR = PROMPT_DIR / "developer"


def _iter_prompts(directory: Path) -> Iterable[Path]:
    if not directory.exists():
        return []
    return sorted(p for p in directory.glob("*.txt") if p.is_file())


def list_prompts(*, developer: bool = False) -> None:
    directory = DEVELOPER_DIR if developer else PROMPT_DIR
    for prompt in _iter_prompts(directory):
        print(prompt.stem)


def show_prompt(name: str, *, developer: bool = False) -> None:
    directory = DEVELOPER_DIR if developer else PROMPT_DIR
    path = directory / f"{name}.txt"
    if not path.exists():
        category = "developer" if developer else "user"
        raise SystemExit(f"Prompt '{name}' not found in {category} catalog")
    print(path.read_text())


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="teslamind")
    sub = parser.add_subparsers(dest="cmd", required=True)
    list_parser = sub.add_parser("list", help="List available prompts")
    list_parser.add_argument(
        "--developer",
        action="store_true",
        help="List prompts from the developer catalog",
    )
    show = sub.add_parser("show", help="Show a prompt")
    show.add_argument("name")
    show.add_argument(
        "--developer",
        action="store_true",
        help="Look up the prompt in the developer catalog",
    )
    args = parser.parse_args(argv)
    if args.cmd == "list":
        list_prompts(developer=args.developer)
    elif args.cmd == "show":
        show_prompt(args.name, developer=args.developer)

if __name__ == "__main__":
    main()
