import functools
import inspect
import itertools
import operator
import re
from collections import deque

from foundational.exceptions import DecoratorIncompatibilityError
from foundational.iterables import iterify
from foundational.nulls import DoesNotExist


def nop(obj):
    return obj


def equal_to(other):
    return functools.partial(operator.eq, other)


def not_equal_to(other):
    return functools.partial(operator.ne, other)


def argmin(a):
    return min(range(len(a)), key=a.__getitem__)


def argmax(a):
    return max(range(len(a)), key=a.__getitem__)


is_none = functools.partial(operator.is_, None)
not_none = functools.partial(operator.is_not, None)


def if_none(default):
    def value(v):
        return v if v is not None else default

    return value


def stop_on_input_values(*vals, default=None):
    if not vals:
        vals = (None,)

    def deco(f):
        @functools.wraps(f)
        def func(v):
            return f(v) if v not in vals else default

        return func

    if len(vals) == 1 and callable(vals[0]):
        f = vals[0]
        vals = (None,)
        return deco(f)
    return deco


call_if_not_null = stop_on_input_values(None)


def stop_on_conditions(*conditions, default=None):
    def deco(f):
        @functools.wraps(f)
        def func(v):
            all_conditions_met = all((c(v) for c in conditions))
            return f(v) if all_conditions_met else default

        return func

    return deco


true_values = {"TRUE", "T", "Y", "YES", "ON", "1"}
false_values = {"FALSE", "F", "N", "NO", "OFF", "0"}


def str_to_bool(value: str):
    value = (value or "").upper()
    if value in true_values:
        return True
    elif value in false_values:
        return False
    else:
        return None


def attr_get(*keys: str, default=None):
    def get_attrs(o):
        return [getattr(o, k, default) for k in keys]

    if len(keys) == 1:
        key = keys[0]

    def get_attr(o):
        return getattr(o, key, default)

    return get_attrs if len(keys) > 1 else get_attr


def item_get(*keys: str, default=None):
    def get_keys(d):
        return [d.get(k, default) for k in keys]

    if len(keys) == 1:
        key = keys[0]

    def get_key(d):
        return d.get(key, default)

    return get_keys if len(keys) > 1 else get_key


def attr_or_key_getter(key, default=DoesNotExist):
    def with_obj(obj):
        val = getattr(obj, key, DoesNotExist)
        if val is DoesNotExist:
            try:
                val = obj[key]
                obj = val
            except (IndexError, TypeError):
                val = default
        else:
            obj = val
        return val

    return with_obj


def has_all_attrs(*attrs: str):
    def attrs_exist(o):
        return all((hasattr(o, a) for a in attrs))

    if len(attrs) == 1:
        attr = attrs[0]

    def attr_exists(o):
        return hasattr(o, attr)

    return attrs_exist if len(attrs) > 1 else attr_exists


def all_attrs_not_none(*attrs: str):
    def attrs_not_none(o):
        return all((getattr(o, a, None) is not None for a in attrs))

    if len(attrs) == 1:
        attr = attrs[0]

    def attr_not_none(o):
        return getattr(o, attr, None) is not None

    return attrs_not_none if len(attrs) > 1 else attr_not_none


def has_all_keys(*keys: str):
    def keys_exist(d):
        return all((k in d for k in keys))

    if len(keys) == 1:
        key = keys[0]

    def key_exists(d):
        return key in d

    return keys_exist if len(keys) > 1 else key_exists


def all_keys_not_none(*keys: str):
    def keys_not_none(d):
        return all((d.get(k, None) is not None for k in keys))

    if len(keys) == 1:
        key = keys[0]

    def key_not_none(d):
        return d.get(key, None) is not None

    return keys_not_none if len(keys) > 1 else key_not_none


def map_values(d: dict):
    def mapped_value(val):
        return d.get(val, val)

    return mapped_value


# Because partials are only specifying the first argument to a function,
# and we're effectively specifying the righthand side up front and then
# running the function on a bunch of inputs, we use the inverse functions
# e.g. less_than(5) will run x < 5 for any x. To make the arguments left-to-right,
# we end up calling the equivalent operator.gt(5, x), or is 5 > x


def less_than(other):
    return functools.partial(operator.gt, other)


def greater_than(other):
    return functools.partial(operator.lt, other)


def less_than_or_equal_to(other):
    return functools.partial(operator.ge, other)


def greater_than_or_equal_to(other):
    return functools.partial(operator.le, other)


def regex_sub(pattern, repl):
    pattern = re.compile(pattern)
    return functools.partial(pattern.sub, repl)


class Pipeline(object):
    def __init__(self, *functions):
        self.functions = functions

    def __repr__(self):
        return "Pipeline: [{}]".format(
            ", ".join((str(func) for func in self.functions))
        )

    def __call__(self, val):
        for f in self.functions:
            val = f(val)
        return val


class FunctionMap(object):
    def __init__(self, *functions, use_tuple=True):
        self.functions = functions
        self.use_tuple = use_tuple

    def __repr__(self):
        return f'{self.__class__.__name__}: [{", ".join((str(func) for func in self.functions))}]'

    def __call__(self, *args, **kw):
        val = [func(*args, **kw) for func in self.functions]
        if self.use_tuple:
            return tuple(val)
        else:
            return val


class FunctionZipMap(FunctionMap):
    def __call__(self, vals, **kw):
        val = [func(arg, **kw) for func, arg in zip(self.functions, vals)]

        if self.use_tuple:
            return tuple(val)
        else:
            return val


class FunctionStarMap(object):
    def __init__(self, function, use_tuple=True):
        self.function = function
        self.use_tuple = use_tuple

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.function}"

    def __call__(self, *args, **kw):
        val = list(
            itertools.chain(*itertools.starmap(self.function, itertools.chain(*args)))
        )
        if self.use_tuple:
            return tuple(val)
        else:
            return val

        return ()


class VectorFunction(object):
    def __init__(self, function):
        self.function = function

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.function}"

    def __call__(self, values):
        return list(map(self.function, values))


class ChainedFunction(object):
    def __init__(self, function):
        self.function = function

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.function}"

    def __call__(self, values):
        return list(itertools.chain(*(map(self.function, iterify(v)) for v in values)))


class hybridmethod(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        self_or_cls = owner if instance is None else instance

        @functools.wraps(self.func)
        def call_hybrid(*args, **kwargs):
            return self.func(self_or_cls, *args, **kwargs)

        return call_hybrid


def get_innermost_argspec(method):
    """When passed a method/function, drill through all layers of decorators to get the inner argspec."""

    orig_method = method
    q = deque([orig_method])
    while q:
        method = q.popleft()
        if hasattr(method, "__func__"):
            method = method.__func__
        elif hasattr(method, "func"):
            method = method.func

        argspec = inspect.getfullargspec(method)
        args = argspec.args

        if args and args[0] in ("self", "cls"):
            return argspec
        if not hasattr(method, "__closure__") or method.__closure__ is None:
            raise DecoratorIncompatibilityError(
                "Decorator has no closure: {}".format(method)
            )

        closure = method.__closure__

        for cell in closure:
            inner_method = cell.cell_contents
            if inner_method is method:
                continue
            if not inspect.isfunction(inner_method) and not inspect.ismethod(
                inner_method
            ):
                continue
            q.append(inner_method)
