import re


def extract_days(text: str):
    m = re.search(r"(\d+)\s*days", text.lower())
    return int(m.group(1)) if m else None


def extract_repeat_count(text: str):
    text = text.lower()

    if "twice" in text:
        return 2
    if "thrice" in text:
        return 3
    m = re.search(r"(\d+s)\s*times?", text.lower())
    return int(m.group(1)) if m else None


def extract_amount_threshold(text: str):
    m = re.search(r"amount\s*>\s*(\d+)", text.lower())
    return int(m.group(1)) if m else None

