#!/usr/bin/env python

from __future__ import annotations

import more_itertools

from advent_of_code_2020_py import problem


def SeatID(s: str) -> int:
    trans = str.maketrans({"F": "0", "B": "1", "L": "0", "R": "1"})
    return int(s.translate(trans), 2)


def part1():
    print(max(problem.Get(5, lambda s: SeatID(s))))


def part2():
    seats = list(sorted(problem.Get(5, lambda s: SeatID(s))))
    print(next(s for s in more_itertools.pairwise(seats) if s[1] - s[0] != 1))


if __name__ == "__main__":
    part1()
    part2()
