#!/usr/bin/env python

from __future__ import annotations

import collections
import itertools
from typing import List, Tuple

from advent_of_code_2020_py import problem


def Valid(n: int, stream: collections.Counter[int]) -> bool:
    return any(
        v1 != v2 and v1 + v2 == n
        for (v1, v2) in itertools.product(stream, repeat=2)
    )


def FindFirstInvalidIdx(stream: List[int], window: int) -> int:
    counter = collections.Counter(stream[:window])
    for idx in range(window, len(stream)):
        next_value = stream[idx]
        if not Valid(next_value, counter):
            return idx
        out_of_window = stream[idx - window]
        counter[out_of_window] -= 1
        if not counter[out_of_window]:
            del counter[out_of_window]
        counter[next_value] += 1
    raise ValueError("Did not find any invalid values")


def FindRangeWithSum(data: List[int], target: int) -> Tuple[int, int]:
    for lower_idx in range(len(data)):
        for upper_idx in range(lower_idx + 1, len(data)):
            if sum(data[lower_idx : upper_idx + 1]) == target:
                return lower_idx, upper_idx
    raise ValueError("Did not find a range with the target sum")


def MinMaxSum(data: List[int]) -> int:
    return min(data) + max(data)


def part1():
    data = list(problem.Get(9, int))
    print(data[FindFirstInvalidIdx(data, 25)])


def part2():
    data = list(problem.Get(9, int))
    first_bad_value = data[FindFirstInvalidIdx(data, 25)]
    lower, upper = FindRangeWithSum(data, first_bad_value)
    print(MinMaxSum(data[lower : upper + 1]))


if __name__ == "__main__":
    part1()
    part2()
