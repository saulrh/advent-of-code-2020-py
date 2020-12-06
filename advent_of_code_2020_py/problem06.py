#!/usr/bin/env python

from __future__ import annotations

import functools
from typing import Iterable, Set

from advent_of_code_2020_py import problem

LETTERS = {chr(i) for i in range(ord("a"), ord("z") + 1)}


def Part1Batch(group: Iterable[Set[str]]) -> Set[str]:
    return functools.reduce(set.union, group, set())


def Part2Batch(group: Iterable[Set[str]]) -> Set[str]:
    return functools.reduce(set.intersection, group, set(LETTERS))


def part1():
    groups = problem.GetBatches(
        problem_number=6,
        line_transform=set,
        batch_transform=Part1Batch,
    )
    print(sum(len(g) for g in groups))


def part2():
    groups = problem.GetBatches(
        problem_number=6,
        line_transform=set,
        batch_transform=Part2Batch,
    )
    print(sum(len(g) for g in groups))


if __name__ == "__main__":
    part1()
    part2()
