class _Omitted:
    def __bool__(self):
        return False

    def __repr__(self):
        return "Omitted"


_Omitted.__nonzero__ = _Omitted.__bool__

Omitted = _Omitted()


class _DoesNotExist:
    def __bool__(self):
        return False

    def __repr__(self):
        return "DoesNotExist"


_DoesNotExist.__nonzero__ = _DoesNotExist.__bool__

DoesNotExist = _DoesNotExist()


class NotInSet:
    pass


def obj_or_none(obj):
    return obj or None
