import os


BASE_DIR = os.path.dirname(__file__)


def load_prompt(filename: str) -> str:
    path = os.path.join(BASE_DIR, "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(filename: str, values: dict) -> str:
    template = load_prompt(filename)
    for key, value in values.items():
        template = template.replace("{" + key + "}", str(value))
    return template
