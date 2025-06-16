import json
from pathlib import Path
import sys

REQUIRED_FIELDS = {"title", "version", "license", "prompt_path"}

def main():
    meta_dir = Path('metadata')
    success = True
    for path in meta_dir.glob('*.json'):
        if path.name == 'schema.json':
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            print(f"{path}: JSON decode error: {e}")
            success = False
            continue
        missing = REQUIRED_FIELDS - data.keys()
        if missing:
            print(f"{path}: missing fields: {', '.join(sorted(missing))}")
            success = False
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
