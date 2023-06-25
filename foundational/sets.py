class NullSet(object):
    def __contains__(self, item):
        return False


class UniversalSet(object):
    def __contains__(self, item):
        return True
