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
        if self._stop == other._stop:
            return self.peek_sort_key() < other.peek_sort_key()
        if self._stop:
            return True
        else:
            return False

    def __le__(self, other):
        if self._stop == other._stop:
            return self.peek_sort_key() <= other.peek_sort_key()
        if self._stop:
            return True
        else:
            return False

    def __gt__(self, other):
        if self._stop == other._stop:
            return self.peek_sort_key() > other.peek_sort_key()
        if self._stop:
            return False
        else:
            return True
        
    def __ge__(self, other):
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






