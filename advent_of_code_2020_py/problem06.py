#!/usr/bin/env python

from __future__ import annotations

import functools
from typing import Iterable, Set

from advent_of_code_2020_py import problem


def Part1Batch(group: Iterable[Set[str]]) -> Set[str]:
    return functools.reduce(set.union, group)


def Part2Batch(group: Iterable[Set[str]]) -> Set[str]:
    return functools.reduce(set.intersection, group)


def part1():
    print(sum(len(g) for g in problem.GetBatches(6, set, Part1Batch)))


def part2():
    print(sum(len(g) for g in problem.GetBatches(6, set, Part2Batch)))


if __name__ == "__main__":
    part1()
    part2()
