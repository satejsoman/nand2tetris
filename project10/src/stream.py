from typing import Iterator, TypeVar
import itertools

class Stream(Iterator[TypeVar('T')]):
    """ implements a peekable iterator of tokens """
    # implementation from https://stackoverflow.com/a/20412546
    def __init__(self, it):
        self.src, = itertools.tee(it, 1)

    def __iter__(self):
        return self.src

    def __next__(self):
        return self.src.__next__()

    def next(self, n = 1):
        return self.__next__() if n == 1 else tuple(self.__next__() for _ in range(n))

    def peek(self):
        return self.src.__copy__().__next__() 