from typing import Iterator, TypeVar
import itertools

T = TypeVar('T')
class Stream(Iterator[T]):
    """ implements a peekable iterator of tokens """
    # implementation from https://stackoverflow.com/a/20412546
    def __init__(self, it):
        self.src, = itertools.tee(it, 1)

    def __iter__(self):
        return self.src

    def __next__(self):
        return self.src.__next__()

    def next(self, n = 1):
        if n == 1:
            return self.__next__()
        return tuple(self.__next__() for _ in range(n))

    def peek(self):
        try:
            return self.src.__copy__().__next__() 
        except StopIteration:
            return None

def peek(s: Stream):
    return s.peek()