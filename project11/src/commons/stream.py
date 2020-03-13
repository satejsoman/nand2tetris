import itertools
from typing import Generic, Iterator, Tuple, TypeVar, Union

T = TypeVar('T')
class Stream(Iterator[T], Generic[T]):
    """ implements a peekable iterator of tokens """
    # implementation from https://stackoverflow.com/a/20412546
    def __init__(self, it: Iterator[T]):
        self.src, = itertools.tee(it, 1)

    def __iter__(self) -> Iterator[T]:
        return self.src

    def __next__(self) -> T:
        return self.src.__next__()

    def next(self, n = 1) -> Union[T, Tuple[T]]:
        return self.__next__() if n == 1 else tuple(self.__next__() for _ in range(n))

    def peek(self) -> T:
        return self.src.__copy__().__next__() 
