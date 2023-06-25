from basics.binary import Base16, Base32, Base64, Base85, int_from_bytes, int_to_bytes

def test_int_bytes():
    assert int_from_bytes(int_to_bytes(12345)) == 12345


def test_base16():
    assert Base16.decode_str(Base16.encode_str("hello")) == "hello"
    for x in (1, 12, 123, 1234, 12345, 123456):
        assert Base16.decode_int(Base16.encode_int(x)) == x


def test_base32():
    assert Base32.decode_str(Base32.encode_str("hello")) == "hello"
    for x in (1, 12, 123, 1234, 12345, 123456, 1234567, 12345678, 123456789):
        assert Base32.decode_int(Base32.encode_int(x)) == x


def test_base64():
    assert Base64.decode_str(Base64.encode_str("hello")) == "hello"
    for x in (1, 12, 123, 1234, 12345, 123456, 1234567, 12345678, 123456789):
        assert Base64.decode_int(Base64.encode_int(x)) == x


def test_base85():
    assert Base85.decode_str(Base85.encode_str("hello")) == "hello"
    for x in (1, 12, 123, 1234, 12345, 123456, 1234567, 12345678, 123456789):
        assert Base85.decode_int(Base85.encode_int(x)) == x
