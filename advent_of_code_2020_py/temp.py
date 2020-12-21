import functools
import itertools
import math
from typing import Iterator, Tuple


@functools.lru_cache
def Positions(size: int) -> Tuple[int]:
    w = int(math.sqrt(size))

    def _Inner() -> Iterator[int]:
        x1 = 0
        x2 = 0
        while True:
            yield (x1 * w) + x2
            x1 -= 1
            x2 += 1
            if x2 == w:
                x2 = x1 + 2
                x1 = w - 1
            elif x1 == -1:
                x1 = x2
                x2 = 0

    return tuple(itertools.islice(_Inner(), size))
