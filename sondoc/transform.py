import re
from typing import Generator, Optional, Sequence, cast


class Token:
    __slot__ = ("kind", "value", "groups")

    def __init__(self, kind: str, value: Optional[str], groups: Sequence[str]):
        self.kind = kind
        self.value = value
        self.groups = groups


def tokenizer(input: str) -> Generator[Token, None, None]:
    token_specification = [
        ("REFERENCE_WITH_CONTEXT", r"\b(_\w+_)\{([^}{]+)\}"),
        ("DEFINITION_WITH_CONTEXT", r"\*(_\w+_)\*\{([^}{]+)\}"),
        ("REFERENCE", r"\b(_\w+_)\b"),
        ("DEFINITION", r"\*(_\w+_)\*"),
        ("IMAGE", r"!\[[^\[\]]+\]\([^)(]+\)"),
        ("TEXT", r"[^_)(}{\[\]!\*]+"),
        ("CHAR", r"."),
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, input):
        kind = cast(str, mo.lastgroup)
        value = mo.group()
        groups = [x for x in mo.groups() if x is not None]
        yield Token(kind, value, groups)
