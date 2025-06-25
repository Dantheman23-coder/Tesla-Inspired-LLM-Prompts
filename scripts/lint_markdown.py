import sys
from pathlib import Path


def check_file(path: Path) -> bool:
    success = True
    for i, line in enumerate(path.read_text().splitlines(), 1):
        if line.rstrip() != line:
            print(f"{path}:{i}: trailing whitespace")
            success = False
    return success


def main():
    files = [Path('README.md')] + list(Path('docs').rglob('*.md'))
    ok = True
    for file in files:
        if not check_file(file):
            ok = False
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
