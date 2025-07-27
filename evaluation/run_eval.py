"""Evaluate prompts using stubbed LLM."""
import json
from pathlib import Path
import sys

THIRD_PARTY = Path(__file__).resolve().parent.parent / "third_party"
if str(THIRD_PARTY) not in sys.path:
    sys.path.append(str(THIRD_PARTY))

from teslamind.prompt import Prompt
from teslamind.metrics import length_score

try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import SystemMessage, HumanMessage
except Exception:  # offline fallback
    class ChatOpenAI:
        def __init__(self, *_, **__):
            pass
        def __call__(self, messages):
            class R:
                def __init__(self):
                    self.content = "stub"
            return R()

    class SystemMessage:
        def __init__(self, content):
            self.content = content
    class HumanMessage(SystemMessage):
        pass

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"
RESULTS_FILE = Path(__file__).resolve().parent / "results.json"


def main() -> None:
    llm = ChatOpenAI()
    results = []
    for prompt_file in PROMPT_DIR.glob("*.txt"):
        prompt = Prompt.from_file(prompt_file)
        messages = [SystemMessage(content=prompt.text), HumanMessage(content="ping")]
        response = llm(messages)
        score = length_score(response.content)
        results.append({"prompt": prompt_file.name, "score": score.value})
    RESULTS_FILE.write_text(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
