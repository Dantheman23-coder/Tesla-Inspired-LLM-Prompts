"""Command line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from .modes import get_mode, list_modes
from .persona import get_persona, list_personas
from .prompt import compose_prompt

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def list_prompts() -> None:
    for p in sorted(PROMPT_DIR.glob("*.txt")):
        print(p.stem)


def show_prompt(name: str) -> None:
    path = PROMPT_DIR / f"{name}.txt"
    if not path.exists():
        raise SystemExit(f"Prompt '{name}' not found")
    print(path.read_text())


def list_modes_cli() -> None:
    for mode in list_modes():
        print(f"{mode.slug}\t{mode.title} — {mode.description}")


def show_mode_cli(slug: str) -> None:
    mode = get_mode(slug)
    print(mode.summary())


def apply_mode_cli(slug: str, task: str) -> None:
    mode = get_mode(slug)
    print(mode.apply(task))


def list_personas_cli() -> None:
    for persona in list_personas():
        slug = persona.slug or persona.name.lower().replace(" ", "-")
        print(f"{slug}\t{persona.name} — {persona.description}")


def show_persona_cli(slug: str) -> None:
    persona = get_persona(slug)
    print(persona.system_prompt())


def compose_cli(
    task: str,
    *,
    mode: str | None,
    persona: str | None,
    template: str | None,
    name: str | None,
) -> None:
    prompt = compose_prompt(
        task,
        mode=mode,
        persona=persona,
        template=template,
        name=name,
    )
    print(prompt.text)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="teslamind")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List available prompts")
    show = sub.add_parser("show", help="Show a prompt")
    show.add_argument("name")

    modes = sub.add_parser("modes", help="Explore stylistic modes")
    modes_sub = modes.add_subparsers(dest="action", required=True)
    modes_sub.add_parser("list", help="List modes")
    modes_show = modes_sub.add_parser("show", help="Show mode details")
    modes_show.add_argument("slug")
    modes_apply = modes_sub.add_parser("apply", help="Apply a mode to a task")
    modes_apply.add_argument("slug")
    modes_apply.add_argument("task", nargs="+", help="Task description")

    personas = sub.add_parser("personas", help="Explore personas")
    personas_sub = personas.add_subparsers(dest="action", required=True)
    personas_sub.add_parser("list", help="List personas")
    personas_show = personas_sub.add_parser("show", help="Show persona details")
    personas_show.add_argument("slug")

    compose = sub.add_parser(
        "compose",
        help="Compose a prompt using optional persona and mode",
    )
    compose.add_argument("task", nargs="+", help="Task to render inside the prompt")
    compose.add_argument("--mode", help="Mode slug to append guidance")
    compose.add_argument("--persona", help="Persona slug for system context")
    compose.add_argument(
        "--template",
        help="Optional base template (should include '{task}')",
    )
    compose.add_argument("--name", help="Name for the composed prompt")

    args = parser.parse_args(argv)

    if args.cmd == "list":
        list_prompts()
    elif args.cmd == "show":
        show_prompt(args.name)
    elif args.cmd == "modes":
        if args.action == "list":
            list_modes_cli()
        elif args.action == "show":
            show_mode_cli(args.slug)
        elif args.action == "apply":
            apply_mode_cli(args.slug, " ".join(args.task))
    elif args.cmd == "personas":
        if args.action == "list":
            list_personas_cli()
        elif args.action == "show":
            show_persona_cli(args.slug)
    elif args.cmd == "compose":
        compose_cli(
            " ".join(args.task),
            mode=args.mode,
            persona=args.persona,
            template=args.template,
            name=args.name,
        )


if __name__ == "__main__":
    main()
