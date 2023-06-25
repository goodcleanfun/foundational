import binascii
from uuid import uuid4


def random_guid():
    return str(uuid4().hex)


def random_guid_binary():
    g = random_guid()
    return binascii.a2b_hex(g)
