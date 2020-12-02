#!/usr/bin/env python

import functools
import itertools as it
import operator
from typing import Iterable, Tuple

from advent_of_code_2020_py import problem


def get_point(
    data: Iterable[int], target: int, length: int
) -> Tuple[int, ...]:
    return next(p for p in it.combinations(data, length) if sum(p) == target)


def get_result(point: Iterable[int]) -> int:
    return functools.reduce(operator.mul, point, 1)


def part1():
    print(get_result(get_point(problem.Get(1, int), 2020, 2)))


def part2():
    print(get_result(get_point(problem.Get(1, int), 2020, 3)))


if __name__ == "__main__":
    part1()
    part2()
