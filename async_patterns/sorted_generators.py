import enum
import itertools
import datetime
import re
import pprint
import traceback

def breakpoint(): import pdb;pdb.set_trace();

class SortedGenerator:
    def __init__(self, generator, sort_key, reverse=False):
        self.__generator = generator
        self.sort_key = sort_key
        self.reverse = reverse

    def __iter__(self):
        return SortedGeneratorIterator(iter(self.__generator), self.sort_key)
      
class SortedGeneratorIterator:
    def __init__(self, iterator, sort_key, reverse=False):
        self.__iterator = iterator
        self._stop = False
        self.sort_key = sort_key
        self.reverse = reverse

        try:
            self.__next = next(self.__iterator)
        except StopIteration:
            self._stop = True

    def peek(self):
        return self.__next

    def peek_sort_key(self):
        
        return self.sort_key(self.__next)

    def __next__(self):
        if self._stop: raise StopIteration()
        
        _ = self.__next

        try:
            self.__next = next(self.__iterator)
        except StopIteration:
            self._stop = True

        return _

    def __eq__(self, other):
        if self._stop != other._stop: return False
        return self.peek_sort_key() == other.peek_sort_key()

    def __lt__(self, other):
        if self._stop and other._stop: return False
        if self._stop == other._stop:
            return self.peek_sort_key() < other.peek_sort_key()
        if self._stop:
            return True
        else:
            return False

    def __le__(self, other):
        if self._stop and other._stop: return True

        if self._stop == other._stop:
            return self.peek_sort_key() <= other.peek_sort_key()
        if self._stop:
            return True
        else:
            return False

    def __gt__(self, other):
        if self._stop and other._stop: return False

        if self._stop == other._stop:
            return self.peek_sort_key() > other.peek_sort_key()
        if self._stop:
            return False
        else:
            return True
        
    def __ge__(self, other):
        if self._stop and other._stop: return True

        if self._stop == other._stop:
            return self.peek_sort_key() >= other.peek_sort_key()
        if self._stop:
            return False
        else:
            return True

class SortedGenerators:
    def __init__(self, generators, sort_key, reverse=False):
        self.generators = [SortedGenerator(_, sort_key) for _ in generators]

        self.sort_key = lambda it: sort_key(it.peek())
        self.reverse = reverse

    def __iter__(self):
        return SortedGeneratorsIterator(
                [iter(_) for _ in self.generators],
                self.reverse)

class SortedGeneratorsIterator:
    def __init__(self, iterators, reverse=False):
        self.__iterators = iterators
        self.reverse = reverse

    def __next__(self):
        self.__iterators = sorted(self.__iterators, reverse=self.reverse)

        while self.__iterators and self.__iterators[0]._stop:
            self.__iterators.pop(0)

        if not self.__iterators: raise StopIteration()

        return self.__iterators[0].__next__()

#######################################################################


class AsyncSortedGenerator:
    def __init__(self, generator, sort_key, reverse=False):
        self.__generator = generator
        self.sort_key = sort_key
        self.reverse = reverse

    def __aiter__(self):
        return AsyncSortedGeneratorIterator(self.__generator.__aiter__(), self.sort_key)
 
class AsyncSortedGeneratorIterator:
    def __init__(self, iterator, sort_key, reverse=False):
        self.__iterator = iterator

        self._ready = False
        self._stop = False
        
        self.sort_key = sort_key
        self.reverse = reverse


    def peek(self):
        assert self._ready
        return self.__next

    def peek_sort_key(self):
        assert self._ready
        return self.sort_key(self.__next)

    async def _first(self):
        if self._ready: return
        
        try:
            self.__next = await self.__iterator.__anext__()
        except StopAsyncIteration:
            self._stop = True

        self._ready = True

    async def __anext__(self):
        if self._stop: raise StopAsyncIteration()
        
        _ = self.__next

        try:
            self.__next = await self.__iterator.__anext__()
        except StopAsyncIteration:
            self._stop = True

        return _

    def __eq__(self, other):
        if self._stop != other._stop: return False
        return self.peek_sort_key() == other.peek_sort_key()

    def __lt__(self, other):
        if self._stop and other._stop: return False
        if self._stop == other._stop:
            return self.peek_sort_key() < other.peek_sort_key()
        if self._stop:
            return True
        else:
            return False

    def __le__(self, other):
        if self._stop and other._stop: return True

        if self._stop == other._stop:
            return self.peek_sort_key() <= other.peek_sort_key()
        if self._stop:
            return True
        else:
            return False

    def __gt__(self, other):
        if self._stop and other._stop: return False

        if self._stop == other._stop:
            return self.peek_sort_key() > other.peek_sort_key()
        if self._stop:
            return False
        else:
            return True
        
    def __ge__(self, other):
        if self._stop and other._stop: return True

        if self._stop == other._stop:
            return self.peek_sort_key() >= other.peek_sort_key()
        if self._stop:
            return False
        else:
            return True

class AsyncSortedGenerators:
    def __init__(self, generators, sort_key, reverse=False):
        self.generators = [AsyncSortedGenerator(_, sort_key) for _ in generators]

        self.sort_key = lambda it: sort_key(it.peek())
        self.reverse = reverse

    def __aiter__(self):
        return AsyncSortedGeneratorsIterator(
                [_.__aiter__() for _ in self.generators],
                self.reverse)

class AsyncSortedGeneratorsIterator:
    def __init__(self, iterators, reverse=False):
        self.__iterators = iterators
        self.reverse = reverse

    async def __anext__(self):
        for i in self.__iterators:
            await i._first()

        self.__iterators = sorted(self.__iterators, reverse=self.reverse)

        while self.__iterators and self.__iterators[0]._stop:
            self.__iterators.pop(0)

        if not self.__iterators: raise StopAsyncIteration()

        return await self.__iterators[0].__anext__()






