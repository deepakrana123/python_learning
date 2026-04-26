import re


def normalize(text: str) -> str:
    return text.lower().strip()


def extract_days(text: str):
    match = re.search(r"(\d+)\s*days?", normalize(text))
    return int(match.group(1)) if match else None


def extract_repeat_count(text: str):
    text = normalize(text)

    if "twice" in text:
        return 2

    if "thrice" in text:
        return 3

    match = re.search(r"(\d+)\s*times?", text)
    return int(match.group(1)) if match else None


def extract_amount_threshold(text: str):
    match = re.search(r"amount\s*[>]=?\s*(\d+)", normalize(text))
    return int(match.group(1)) if match else None


def extract_flags(text: str):
    text = normalize(text)

    return {
        "vip": "vip" in text,
        "premium": "premium" in text,
        "urgent": "urgent" in text,
    }


def extract_all(text: str):
    return {
        "days": extract_days(text),
        "repeat_count": extract_repeat_count(text),
        "amount_threshold": extract_amount_threshold(text),
        "flags": extract_flags(text),
    }
