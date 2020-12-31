from sondoc.transform import tokenizer

mixed = """
*_sc__Situation_*{Situation}

_sc__Situation_{We have no more water!}

Just a reference _sc__Situation_.

asdf *_definition_* asdf

![cosmic](~global/img/cosmic.jpg)

left!
"""

values = set(
    [
        "*_sc__Situation_*{Situation}",
        "_sc__Situation_{We have no more water!}",
        "_sc__Situation_",
        "![cosmic](~global/img/cosmic.jpg)",
        "*_definition_*",
    ]
)


def test_tokenizer_reproduce():
    tokens = list(tokenizer(mixed))
    result = "".join([x.value for x in tokens])
    assert result == mixed


def test_tokenizer_values():
    tokens = list(tokenizer(mixed))
    result = set([x.value for x in tokens if x.kind not in ("TEXT", "CHAR")])
    assert values == result
