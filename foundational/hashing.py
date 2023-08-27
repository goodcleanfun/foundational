import binascii
import hashlib

from foundational.encoding import safe_encode


def crc32_unsigned(value):
    """binascii's crc32 is signed, make it unsigned"""
    return binascii.crc32(safe_encode(value)) & 0xFFFFFFFF


def checksum(filename, hashfunc="md5"):
    if not isinstance(hashfunc, str) or not hasattr(hashlib, hashfunc):
        raise ValueError("hashfunc must be a function specified in hashlib")

    hf = getattr(hashlib, hashfunc)
    h = hf()

    with open(filename, "rb") as f:
        done = False
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()
