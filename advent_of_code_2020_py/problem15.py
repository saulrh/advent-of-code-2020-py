#!/usr/bin/env python

import itertools
from typing import Iterator, List, Sequence


def Parse(starting: str) -> List[int]:
    return [int(x) for x in starting.split(",")]


def Memory(starting: Sequence[int]) -> Iterator[int]:
    yield from starting

    last = starting[-1]
    positions = {val: idx + 1 for idx, val in enumerate(starting)}

    for idx in itertools.count(len(positions)):
        if last not in positions:
            result = 0
        else:
            result = idx - positions[last]
        positions[last] = idx
        last = result
        yield result


def part1():
    starting = Parse("15,12,0,14,3,1")
    print(list(itertools.islice(Memory(starting), 2019, 2020)))


def part2():
    starting = Parse("15,12,0,14,3,1")
    print(list(itertools.islice(Memory(starting), 30000000 - 1, 30000000)))


if __name__ == "__main__":
    part1()
    part2()
