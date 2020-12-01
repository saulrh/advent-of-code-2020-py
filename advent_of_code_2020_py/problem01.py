#!/usr/bin/env python

from typing import Optional, Tuple, Iterable, List

import prettyprinter
import csv
import itertools
import functools
import operator


def get_point(
    data: Iterable[int], target: int, length: int
) -> Optional[Tuple[int, ...]]:
    for point in itertools.combinations(data, length):
        if sum(point) == target:
            return point
    return None


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
