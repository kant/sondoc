from hypothesis import given
from hypothesis.strategies import text

from sondoc.transform import html_crossref, tokenizer

mixed = """
*_sc__Situation_*{Situation}

_sc__Situation_{We have no more water!}

Just a reference _sc__Situation_.

asdf *_definition_* asdf

![cosmic](~global/img/cosmic.jpg)

left!
"""

snapshot = """
<span class="symbol" title="_sc__Situation_" id="_sc__Situation_">Situation</span>

<a title="_sc__Situation_" href="#_sc__Situation_">We have no more water!</a>

Just a reference <a title="_sc__Situation_" href="#_sc__Situation_"><sup>ref</sup></a>.

asdf <span class="symbol" title="_definition_" id="_definition_"></span> asdf

![cosmic](~global/img/cosmic.webp)

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


@given(text())
def test_tokenizer_reproduce_hyp(text):
    tokens = list(tokenizer(text))
    result = "".join([x.value for x in tokens])
    assert result == text


def test_tokenizer_values():
    tokens = list(tokenizer(mixed))
    result = set([x.value for x in tokens if x.kind not in ("TEXT", "CHAR")])
    assert values == result


def test_tokenizer_symbols():
    tokens = list(tokenizer(mixed))
    result = set(
        [x.groups[1] for x in tokens if x.kind not in ("TEXT", "CHAR", "IMAGE")]
    )
    assert result == {"_definition_", "_sc__Situation_"}


def test_crossref():
    result = html_crossref(mixed)
    print(result)
    assert result.strip() == snapshot.strip()


@given(text())
def test_crossref_hyp_fuzz(text):
    html_crossref(text)
