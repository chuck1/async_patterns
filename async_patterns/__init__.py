__version__ = '0.3b14'

from .callbacks import *
from .coro_queue import *
from . import callbacks
from . import coro_queue

__all__ = callbacks.__all__ + coro_queue.__all__ + ['protocol']

async def aenumerate(aiterable):
    i = 0
    async for x in aiterable:
        yield i, x
        i += 1

async def aislice(aiterable, *args):
    s = slice(*args)
    it = iter(range(s.start or 0, s.stop or sys.maxsize, s.step or 1))
    try:
        nexti = next(it)
    except StopIteration:
        return
    async for i, element in aenumerate(aiterable):
        if i == nexti:
            yield element
            try:
                nexti = next(it)
            except StopIteration:
                return

