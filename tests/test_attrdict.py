from basic.attrdict import AttrDict


def test_attrdict():
    a = AttrDict()
    a.key = "value"
    assert a.key == "value"
    assert a["key"] == "value"

    del a.key
    assert "key" not in a
