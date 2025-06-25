import json
from pathlib import Path
import sys

THIRD_PARTY = Path(__file__).resolve().parent.parent / "third_party"
if str(THIRD_PARTY) not in sys.path:
    sys.path.append(str(THIRD_PARTY))
try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import SystemMessage, HumanMessage
except Exception:
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

def main():
    llm = ChatOpenAI(temperature=0)
    results = []
    for prompt_file in PROMPT_DIR.glob("*.txt"):
        system_text = prompt_file.read_text()
        messages = [SystemMessage(content=system_text), HumanMessage(content="ping")]
        response = llm(messages)
        score = len(response.content)
        results.append({"prompt": prompt_file.name, "score": score})
    RESULTS_FILE.write_text(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
