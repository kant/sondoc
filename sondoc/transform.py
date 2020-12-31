import re


class Token:
    __slot__ = ("kind", "value", "groups")

    def __init__(self, kind, value, groups):
        self.kind = kind
        self.value = value
        self.groups = groups


def tokenizer(input):
    token_specification = [
        ("REFERENCE_WITH_CONTEXT", r"\b(_\w+_)\{([^\{\}]*)\}"),
        ("DEFINITION_WITH_CONTEXT", r"\b\*(_\w+_)\*\{([^\{\}]*)\}"),
        ("REFERENCE", r"\b(_\w+_)\b"),
        ("DEFINITION", r"\b\*(_\w+_)\*\b"),
        ("TEXT", r"[^_)(}{\[\]]+"),
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, input):
        kind = mo.lastgroup
        value = mo.group()
        groups = mo.groups()
        yield Token(kind, value, groups)
