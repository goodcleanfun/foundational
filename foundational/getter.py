import operator

from foundational.collections import is_mapping
from foundational.iterables import flatten


def key_getter(*attrs):
    attrs = [getattr(a, "key", a) for a in flatten(attrs)]
    itemgetter = operator.itemgetter(*attrs)
    attrgetter = operator.attrgetter(*attrs)

    def getter(obj):
        if not is_mapping(obj):
            return attrgetter(obj)
        else:
            return itemgetter(obj)

    return getter
