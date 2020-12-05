#!/usr/bin/env python

from __future__ import annotations

import more_itertools

from advent_of_code_2020_py import linalg
from advent_of_code_2020_py import problem


def ToRowColumn(s: str) -> linalg.Point:
    row_part = s[:7].translate(str.maketrans({"F": "0", "B": "1"}))
    col_part = s[7:].translate(str.maketrans({"L": "0", "R": "1"}))
    return linalg.Point(
        row=int(row_part, 2),
        col=int(col_part, 2),
    )


def SeatID(seat: linalg.Point) -> int:
    return seat.row * 8 + seat.col


def part1():
    print(max(problem.Get(5, lambda s: SeatID(ToRowColumn(s)))))


def part2():
    seats = list(sorted(problem.Get(5, lambda s: SeatID(ToRowColumn(s)))))
    print(next(s for s in more_itertools.pairwise(seats) if s[1] - s[0] != 1))


if __name__ == "__main__":
    part1()
    part2()
