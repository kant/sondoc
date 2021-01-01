import re
from pathlib import Path
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
        ("IMAGE", r"!\[([^\[\]]+)\]\(([^)(]+\))"),
        ("TEXT", r"[^_)(}{\[\]!\*]+"),
        ("CHAR", r"."),
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, input):
        kind = cast(str, mo.lastgroup)
        value = mo.group()
        groups = [x for x in mo.groups() if x is not None]
        yield Token(kind, value, groups)


def html_crossref(input: str, directory: str = "./") -> str:
    result = []
    for token in tokenizer(input):
        kind = token.kind
        groups = token.groups
        reference = kind.startswith("REFERENCE")
        definition = kind.startswith("DEFINITION")
        if reference or definition:
            symbol = groups[1]
            context = ""
            if len(groups) > 2:
                context = groups[2]
            if reference:
                html = f'<div id="{symbol}">{context}</div>'
            else:
                if not context:
                    context = "<sup>ref</sup>"
                html = f'<a href="#{symbol}">{context}</a>'
            result.append(html)
        else:
            if kind == "IMAGE":
                text = groups[1]
                link = groups[2]
                abs_link = Path(directory, link)
                md = f"![{text}]({abs_link})"
                result.append(md)
            else:
                result.append(token.value)
    return "".join(result)
