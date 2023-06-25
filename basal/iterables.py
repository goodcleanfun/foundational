from collections import deque
from collections.abc import Generator, Iterable, Iterator, Sequence
from itertools import (
    chain,
    combinations,
    count,
    cycle,
    filterfalse,
    islice,
    tee,
)
from typing import List


def is_sequence(obj):
    return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes))


def is_iterable(obj):
    return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))


def iterify(o, empty_list_if_none=True):
    if o is None and empty_list_if_none:
        return []
    return [o] if not is_iterable(o) else o


def listify(o, empty_list_if_none=True):
    if o is None and empty_list_if_none:
        return []
    if isinstance(o, (range, Generator, Iterator)):
        return list(o)

    return [o] if not is_sequence(o) else o


def flatten(obj):
    return chain.from_iterable(iterify(obj))


def flatten_args(*args):
    result = []

    for arg in args:
        if is_sequence(arg):
            result.extend(arg)
        else:
            result.append(arg)

    return result


def combine_lists(*args: List):
    return sum(args, [])


def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def partition(pred, iterable):
    """
    Use a predicate to partition entries into false entries and true entries
    """
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def round_robin(*iterables):
    """
    roundrobin('ABC', 'D', 'EF') --> A D E B F C
    """
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def all_combinations(s):
    result = [tuple(s)]

    q = deque([([], s)])

    while q:
        left, right = q.popleft()

        res = [
            (i, i + k)
            for k in range(2, len(right) + 1)
            for i in range(len(right) - k + 1)
        ]

        for i, j in res:
            new_left = tuple(left) + tuple(right[:i]) + (tuple(right[i:j]),)
            new_right = tuple(right[j:])
            result.append(new_left + new_right)
            q.append((new_left, new_right))

    return result


def batch_iter(iterable, batch_size: int):
    source_iter = iter(iterable)
    while True:
        batch = list(islice(source_iter, batch_size))
        if len(batch) > 0:
            yield batch
        else:
            return


def iter_len(it):
    counter = count()
    deque(zip(it, counter), maxlen=0)
    return next(counter)


def argmax(it):
    return max(range(len(it)), key=it.__getitem__)


def split_index_on_condition(it, condition):
    condition_true = []
    condition_false = []

    for i, r in enumerate(it):
        if condition(r):
            condition_true.append(i)
        else:
            condition_false.append(i)

    return condition_true, condition_false


def split_on_condition(it, condition):
    condition_true = []
    condition_false = []

    for r in it:
        if condition(r):
            condition_true.append(r)
        else:
            condition_false.append(r)

    return condition_true, condition_false


def split_on_indices(it, indices, sort_indices=False):
    if sort_indices:
        indices = sorted(indices)
    elif not is_sequence(indices):
        indices = listify(indices)

    m = len(indices)
    data = listify(it)
    if m == 0:
        return [], data
    elif m == len(data):
        return data, []

    j = 0
    ind = indices[j]

    match = []
    no_match = []

    for i, x in enumerate(data):
        if i < ind:
            no_match.append(x)
        elif i == ind:
            j += 1
            match.append(x)
            if j >= m:
                match.extend(data[i + 1 :])
                break
            ind = indices[j]
    return match, no_match


def merge_values_at_indices(it, indices, values, sort_indices=False):
    if sort_indices:
        indices = sorted(indices)
    elif not is_sequence(indices):
        indices = listify(indices)

    m = len(indices)
    other = listify(values)
    if len(other) != m:
        raise ValueError(
            f"Length of merged sequence ({len(values)}) must be equal to length of indices {m}"
        )

    if m == 0:
        return listify(it)

    result = []

    if is_sequence(it):
        it = iter(it)

    for index, value in zip(indices, values):
        while len(result) < index:
            result.append(next(it))
        result.append(value)
    return result
