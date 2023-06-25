from time import time

from foundational.nulls import DoesNotExist


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class cached_classproperty(classproperty):
    def __init__(self, getter):
        super().__init__(getter)
        self.cache = {}

    def __get__(self, instance, owner):
        if owner not in self.cache:
            self.cache[owner] = self.getter(owner)
        return self.cache[owner]


class cached_property(object):
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Setting the ttl to a number expresses how long
    the property will last before being timed out (meaning it will be recomputed.)
    """

    def __init__(self, ttl=None, keep_cached_on_error=True):
        if callable(ttl):
            func = ttl
            ttl = None
        else:
            func = None
        self.ttl = ttl
        self.keep_cached_on_error = keep_cached_on_error
        self._prepare_func(func)

    def __call__(self, func):
        self._prepare_func(func)
        return self

    def __get__(self, obj, cls):
        if obj is None:
            return self

        now = time()
        obj_dict = obj.__dict__
        name = self.__name__
        ttl_expired = False
        value = DoesNotExist

        try:
            value, last_updated = obj_dict[name]
        except KeyError:
            pass
        else:
            ttl_expired = self.ttl and self.ttl < now - last_updated
            if not ttl_expired:
                return value

        try:
            value = self.func(obj)
        except Exception:
            if self.keep_cached_on_error and ttl_expired and value is not DoesNotExist:
                return value
            else:
                raise
        obj_dict[name] = (value, now)
        return value

    def __delete__(self, obj):
        obj.__dict__.pop(self.__name__, None)

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = (value, time())

    def _prepare_func(self, func):
        self.func = func
        if func:
            self.__doc__ = func.__doc__
            self.__name__ = func.__name__
            self.__module__ = func.__module__
