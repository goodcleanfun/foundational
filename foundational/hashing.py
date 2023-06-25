import binascii

from foundational.encoding import safe_encode


def crc32_unsigned(value):
    """binascii's crc32 is signed, make it unsigned"""
    return binascii.crc32(safe_encode(value)) & 0xFFFFFFFF
