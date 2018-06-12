import functools
import operator

from async_patterns.sorted_generators import SortedGenerators

def test_0():
    print()

    generators = [range(10, 20), range(0, 30, 3)]

    s = SortedGenerators(generators, lambda x: x)

    l0 = list(s) 

    l1 = sorted(functools.reduce(operator.add, [list(_) for _ in generators]))

    assert(l0 == l1)


