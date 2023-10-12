import copy
import operator
from collections import deque

from foundational.collections import is_mapping
from foundational.functions import attr_or_key_getter
from foundational.iterables import is_sequence, iterify
from foundational.nulls import DoesNotExist, Omitted


def deep_merge(d, *others, overwrite=True):
    result = copy.deepcopy(d)

    queue = deque([(d_i, ()) for d_i in others])
    while queue:
        d, path = queue.popleft()
        d_res = nested_get(result, path)
        if not d_res:
            d_res = {}
            nested_set(result, path, d_res)

        for k, v in d.items():
            if is_mapping(v):
                queue.append((v, path + (k,)))
            elif overwrite or k not in d_res:
                d_res[k] = v

    return result


def nested_diff(orig, other):
    result = {}

    queue = deque([(other, ())])
    while queue:
        d, path = queue.popleft()
        d_res = nested_get(orig, path)
        if not d_res:
            d_res = {}
            nested_set(result, path, d_res)

        for k, v in d.items():
            if is_mapping(v):
                queue.append((v, path + (k,)))
            elif k not in d_res:
                d_res[k] = v

    return result


def nested_getattr(obj, keys, default=None):
    use_map = False

    if isinstance(keys, str):
        keys = keys.split(".")

    for key in keys:
        is_string = isinstance(key, str)
        is_digit = is_string and key.isdigit()
        is_star = key == "*"

        if is_string and not is_digit and not is_star:
            func = attr_or_key_getter(key)
            if not use_map:
                val = func(obj)
                obj = val
            else:
                val = list(map(func, obj))
                obj = val
        elif is_sequence(obj) and (isinstance(key, int) or is_digit):
            try:
                val = obj[int(key)]
                obj = val
            except (IndexError, TypeError):
                obj = DoesNotExist
        elif is_sequence(obj) and is_star:
            use_map = True
        else:
            raise ValueError("Paths must be string attributes or int indexes")
        if obj is DoesNotExist or obj is None:
            return default
    return obj


def nested_get(obj, keys, default=DoesNotExist):
    if isinstance(keys, str):
        keys = keys.split(".")

    # For source_data fields, just return the whole document
    if len(keys) == 0:
        return obj

    use_map = False

    try:
        for key in keys:
            is_string = isinstance(key, str)
            is_digit = is_string and key.isdigit()
            is_star = key == "*"

            if is_string and not is_digit and not is_star:
                if is_mapping(obj) and not use_map:
                    val = obj.get(key, default)
                    obj = val
                elif is_sequence(obj) and use_map:
                    val = list(map(operator.itemgetter(key), obj))
                    obj = val
            elif is_sequence(obj) and (
                isinstance(key, int) or (isinstance(key, str) and key.isdigit())
            ):
                try:
                    val = obj[int(key)]
                    obj = val
                except IndexError:
                    return default
            elif is_sequence(obj) and is_star:
                use_map = True
            else:
                return default
        if obj is DoesNotExist or obj is None:
            return default
        return obj
    except AttributeError:
        return default


def nested_getter(default=DoesNotExist):
    base_default = default

    def _nested_get_with_default(obj, keys, default=Omitted):
        default = default if default is not Omitted else base_default
        return nested_get(obj, keys, default=default)

    return _nested_get_with_default


def nested_exists(d, key):
    keys = iterify(key)
    obj = nested_get(d, keys[:-1], default=DoesNotExist)

    last_key = keys[-1]

    if is_mapping(obj):
        return last_key in obj
    elif is_sequence(obj) and (
        isinstance(last_key, int) or (isinstance(last_key, str) and last_key.isdigit())
    ):
        return len(obj) > int(last_key)

    return False


def nested_set(d, keys, value):
    level = d

    key_pairs = list(zip(keys, keys[1:]))
    for key, next_key in key_pairs:
        key_is_string = isinstance(key, str)
        key_is_digit = isinstance(key, int) or (key_is_string and key.isdigit())

        next_key_is_string = isinstance(next_key, str)
        next_key_is_digit = isinstance(next_key, int) or (
            next_key_is_string and next_key.isdigit()
        )

        next_level = None

        if key_is_string:
            next_level = level.get(key, None)
            if next_level is None:
                if next_key_is_string:
                    level[key] = {}
                    next_level = level[key]
                elif next_key_is_digit:
                    next_key = int(next_key)
                    level[key] = [None] * next_key
                next_level = level[key]
        elif key_is_digit:
            key = int(key)
            if len(level) > key:
                next_level = level[key]
            else:
                if len(level) > 0:
                    level.extend([None] * (key + 1 - len(level)))
                else:
                    level.extend([None] * (key + 1))

            if next_level is None:
                if next_key_is_string:
                    level[key] = {}
                    next_level = level[key]
                elif next_key_is_digit:
                    next_key = int(next_key)
                    level[key] = [None] * next_key
                next_level = level[key]

        level = next_level

    last_key = keys[-1]
    if isinstance(last_key, int) or (isinstance(last_key, str) and last_key.isdigit()):
        last_key = int(last_key)
        if len(level) <= last_key:
            if len(level) > 0:
                level.extend([None] * (last_key + 1 - len(level)))
            else:
                level.extend([None] * (last_key + 1))
    level[last_key] = value


def nested_setattr(obj, keys, value):
    if len(keys) > 0:
        obj = nested_getattr(obj, keys[:-1])
        last_key = keys[-1]
        is_string = isinstance(last_key, str)
        is_digit = isinstance(last_key, int) or (is_string and last_key.isdigit())
        if is_string and not is_digit:
            setattr(obj, last_key, value)
        elif isinstance(last_key, int) or (is_string and is_digit):
            obj[int(last_key)] = value


def nested_del(d, keys):
    level = d
    for key in keys[:-1]:
        next_level = level.get(key, None)
        if next_level is None:
            return
        level = next_level
    del level[keys[-1]]


def nested_delattr(obj, keys):
    if len(keys) > 0:
        for key in keys[:-1]:
            obj = getattr(obj, key)
        delattr(obj, keys[-1])


class Path(object):
    def __init__(self, path, separator="."):
        if isinstance(path, Path):
            self.path = path.path
        else:
            self.path = path
        self.separator = separator

    @property
    def parts(self):
        return self.path.split(self.separator)

    def __iter__(self):
        for part in self.parts:
            yield part

    def __len__(self):
        return len(self.parts)

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.path)

    def index(self, element):
        return self.parts.index(element)

    def __getitem__(self, slice):
        result = self.parts[slice]
        if isinstance(result, list):
            return self.__class__(self.separator.join(result), separator=self.separator)
        return result

    def __eq__(self, other):
        return self.path == other.path and self.separator == other.separator

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.path
