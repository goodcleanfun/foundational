from collections import OrderedDict
from collections.abc import Hashable, Mapping


def unique_list(values):
    """Produces a unique list while preserving input order"""
    return list(OrderedDict.fromkeys(values))


def is_mapping(val):
    return isinstance(val, Mapping)


def is_hashable(val):
    return isinstance(val, Hashable)
