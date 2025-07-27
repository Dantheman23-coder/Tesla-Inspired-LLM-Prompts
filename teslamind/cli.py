"""Command line interface."""
from __future__ import annotations
import argparse
from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def list_prompts() -> None:
    for p in PROMPT_DIR.glob("*.txt"):
        print(p.stem)


def show_prompt(name: str) -> None:
    path = PROMPT_DIR / f"{name}.txt"
    if not path.exists():
        raise SystemExit(f"Prompt '{name}' not found")
    print(path.read_text())


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="teslamind")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="List available prompts")
    show = sub.add_parser("show", help="Show a prompt")
    show.add_argument("name")
    args = parser.parse_args(argv)
    if args.cmd == "list":
        list_prompts()
    elif args.cmd == "show":
        show_prompt(args.name)

if __name__ == "__main__":
    main()
