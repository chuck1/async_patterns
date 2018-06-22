import functools
import operator

import pytest

from async_patterns.sorted_generators import SortedGenerators, AsyncSortedGenerators

def test_0():
    print()

    generators = [range(10, 20), range(0, 30, 3)]

    s = SortedGenerators(generators, lambda x: x)

    l0 = list(s) 

    l1 = sorted(functools.reduce(operator.add, [list(_) for _ in generators]))

    assert(l0 == l1)

def test_1():
    print()

    generators = [range(0), range(0, 30, 3)]

    s = SortedGenerators(generators, lambda x: x, reverse=True)

    l0 = list(s) 

    l1 = sorted(functools.reduce(operator.add, [list(_) for _ in generators]))

    assert(l0 == l1)

@pytest.mark.asyncio
async def test_2():

    async def _f0():
        for i in range(10, 20):
            yield i

    async def _f1():
        for i in range(0, 30, 3):
            yield i

    s = AsyncSortedGenerators([_f0(), _f1()], lambda x: x)

    l0 = [x async for x in s]

    async def _y():
        for _ in [_f0(), _f1()]:
            async for x in _: yield x

    l1 = sorted([x async for x in _y()])

    print(l0)
    print(l1)

    assert(l0 == l1)
   

