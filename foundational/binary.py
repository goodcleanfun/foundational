import base64

from foundational.encoding import safe_decode, safe_encode
from foundational.functions import Pipeline
from foundational.properties import classproperty


def int_to_bytes(x: int, endianness="little"):
    if type(x) != int:
        x = int(x)
    return x.to_bytes((x.bit_length() + 7) // 8, endianness)


def int_from_bytes(x: bytes, endianness="little"):
    return int.from_bytes(x, endianness)


class BinaryEncoder(object):
    @classmethod
    def strip_padding(cls, s):
        return s.rstrip(b"=")

    @classproperty
    def encode(cls):
        return Pipeline(cls.encoder, cls.strip_padding)

    @classmethod
    def add_padding(cls, s):
        return s if len(s) % cls.group_width == 0 else s.ljust(cls.group_width, b"=")

    @classproperty
    def decode(cls):
        return Pipeline(cls.add_padding, cls.decoder)

    @classmethod
    def encode_str(cls, s: str):
        return safe_decode(cls.encode(safe_encode(s)))

    @classmethod
    def encode_int(cls, x: int, endianness: str = "little"):
        return safe_decode(cls.encode(int_to_bytes(x, endianness=endianness)))

    @classmethod
    def decode_str(cls, s: str):
        return safe_decode(cls.decode(safe_encode(s)))

    @classmethod
    def decode_int(cls, s: str, endianness: str = "little"):
        return int_from_bytes(cls.decode(safe_encode(s)), endianness=endianness)


class Base16(BinaryEncoder):
    bits = 16
    group_width = 2
    encoder = base64.b16encode
    decoder = base64.b16decode


class Base32(BinaryEncoder):
    bits = 32
    group_width = 8
    encoder = base64.b32encode
    decoder = base64.b32decode


class Base64(BinaryEncoder):
    bits = 64
    group_width = 8
    encoder = base64.b64encode
    decoder = base64.b64decode


class Base85(BinaryEncoder):
    bits = 85
    encoder = base64.b85encode
    decoder = base64.b85decode

    encode = encoder
    decode = decoder
