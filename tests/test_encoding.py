from crucial.encoding import safe_decode, safe_encode


def test_safe_encode_ascii():
    assert safe_encode("bueno") == b"bueno"


def test_safe_encode_unicode():
    assert safe_encode("Ojalá") == b"Ojal\xc3\xa1"


def test_safe_decode_ascii():
    assert safe_decode(b"bueno") == "bueno"


def test_safe_decode_unicode():
    assert safe_decode(b"Ojal\xc3\xa1") == "Ojalá"


def test_safe_encode_unicode_with_encoding():
    assert safe_encode("Ojalá", encoding="latin-1") == b"Ojal\xe1"


def test_safe_decode_unicode_with_encoding():
    assert safe_decode(b"Ojal\xe1", encoding="latin-1") == "Ojalá"
