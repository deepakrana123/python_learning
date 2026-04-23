import re


def normalize(text: str) -> str:
    return text.lower().strip()


def extract_days(text: str):
    text = normalize(text)
    match = re.search(r"(\d+)\s*days?", text)
    if match:
        return int(match.group(1))
    return None


def extract_repeat_count(text: str):
    text = normalize(text)
    if "twice" in text:
        return 2
    if "thrice" in text:
        return 3
    match = re.search(r"(\d+)\s*times?", text)
    if match:
        return int(match.group(1))
    return None


def extract_amount_threshold(text: str):
    text = normalize(text)
    match = re.search(r"amount\s*[>]=?\s*(\d+)", text)
    if match:
        return int(match.group(1))
    return None


def extract_flags(text: str):
    text = normalize(text)
    flags = {
        "vip": "vip" in text,
        "premium": "premium" in text,
        "urgent": "urgent" in text,
    }
    return flags


def extract_all(text: str):
    return {
        "days": extract_days(text),
        "repeat_count": extract_repeat_count(text),
        "amount_threshold": extract_amount_threshold(text),
        "flags": extract_flags(text),
    }


print(extract_all("Send reminder after 10 days"))
