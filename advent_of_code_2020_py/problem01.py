#!/usr/bin/env python

import csv
import functools
import itertools as it
import operator
from typing import Iterable, List, Tuple

import prettyprinter


def get_point(
    data: Iterable[int], target: int, length: int
) -> Tuple[int, ...]:
    return next(p for p in it.combinations(data, length) if sum(p) == target)


def get_result(point: Iterable[int]) -> int:
    return functools.reduce(operator.mul, point, 1)


def get_data() -> List[int]:
    with open("inputs/problem01.part1.csv", "r") as f:
        reader = csv.DictReader(f)
        return [int(line["Value"]) for line in reader]


def part1():
    data = get_data()
    point = get_point(data, 2020, 2)
    prettyprinter.cpprint(point)
    prettyprinter.cpprint(get_result(point))


def part2():
    data = get_data()
    point = get_point(data, 2020, 3)
    prettyprinter.cpprint(point)
    prettyprinter.cpprint(get_result(point))


if __name__ == "__main__":
    part1()
    part2()
