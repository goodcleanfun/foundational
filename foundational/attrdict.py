class AttrDict(dict):
    """
    A dictionary that allows using the dot operator to get and set keys.
    """

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]

    def __repr__(self):
        return f"{self.__class__.__name__}({dict.__repr__(self)})"
