from sondoc.transform import tokenizer

mixed = """
*_sc__Situation_*{Situation}

_sc__Situation_{We have no more water.}

Just a reference _sc__Situation_.

![cosmic](~global/img/cosmic.jpg)
"""


def test_tokenizer():
    kinds = [x.kind for x in tokenizer(mixed)]
    __import__("pdb").set_trace()
    pass
