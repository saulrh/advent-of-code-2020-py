#!/usr/bin/env python

from __future__ import annotations

from typing import Iterable, Set

from advent_of_code_2020_py import problem


def ParseFilePart1(lines: Iterable[str]) -> Iterable[Set[str]]:
    working = set()
    for line in lines:
        line = line.strip()
        if not line:
            yield working
            working = set()
        working.update(line)
    yield working


def ParseFilePart2(lines: Iterable[str]) -> Iterable[Set[str]]:
    working = None
    for line in lines:
        line = line.strip()
        if not line:
            yield working or set()
            working = None
        elif working is None:
            working = set(line)
        else:
            working &= set(line)
    yield working or set()


def part1():
    print(sum(len(s) for s in ParseFilePart1(problem.Get(6))))


def part2():
    print(sum(len(s) for s in ParseFilePart2(problem.Get(6))))


if __name__ == "__main__":
    part1()
    part2()
