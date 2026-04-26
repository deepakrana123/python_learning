def build_prompt(template: str, values: dict):
    for key, value in values.items():
        template = template.replace("{" + key + "}", str(value))
    return template
