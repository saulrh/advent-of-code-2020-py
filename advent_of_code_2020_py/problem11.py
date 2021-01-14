#!/usr/bin/env python

from __future__ import annotations

import dataclasses
from typing import Callable, Iterable, Mapping, Optional

from advent_of_code_2020_py import linalg
from advent_of_code_2020_py import problem


def Neighbors(g: Grid, pt: linalg.Point) -> Iterable[str]:
    raw = [g.data.get(pt + d) for d in _DIRECTIONS]
    return [p for p in raw if p]


def AllVisible(g: Grid, pt: linalg.Point) -> Iterable[str]:
    raw = (g.Visible(pt, d) for d in _DIRECTIONS)
    return [p for p in raw if p]


@dataclasses.dataclass(frozen=True)
class Grid(object):
    data: Mapping[linalg.Point, str]

    @property
    def height(self) -> int:
        return max(pt.row for pt in self.data.keys())

    @property
    def width(self) -> int:
        return max(pt.col for pt in self.data.keys())

    def __str__(self):
        output = ""
        for row in range(0, self.height + 1):
            for col in range(0, self.width + 1):
                output += self.data.get(linalg.Point(row=row, col=col), " ")
            output += "\n"
        return output

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        return self.data == other.data

    def Step(
        self,
        get_neighbors: Callable[
            [Grid, linalg.Point], Iterable[str]
        ] = Neighbors,
        leave_threshold: int = 4,
    ) -> Grid:
        result = {}
        for pt, cell in self.data.items():
            filled_neighbor_count = sum(
                n == "#" for n in get_neighbors(self, pt)
            )
            # If a seat is empty (L) and there are no occupied seats
            # adjacent to it, the seat becomes occupied.
            if cell == "L":
                if filled_neighbor_count == 0:
                    result[pt] = "#"
                else:
                    result[pt] = "L"

            # If a seat is occupied (#) and four or more seats adjacent to
            # it are also occupied, the seat becomes empty.
            elif cell == "#":
                if filled_neighbor_count >= leave_threshold:
                    result[pt] = "L"
                else:
                    result[pt] = "#"

            # Otherwise, the seat's state does not change.
            else:
                result[pt] = cell

        return Grid(result)

    def RunToConvergence(
        self,
        get_neighbors: Callable[
            [Grid, linalg.Point], Iterable[str]
        ] = Neighbors,
        leave_threshold: int = 4,
    ) -> Grid:
        g = self
        while True:
            nextgrid = g.Step(
                get_neighbors=get_neighbors, leave_threshold=leave_threshold
            )
            if g == nextgrid:
                return nextgrid
            else:
                g = nextgrid

    def Visible(
        self, pt: linalg.Point, direction: linalg.Point
    ) -> Optional[str]:
        next_point = pt
        while True:
            next_point += direction
            next_cell = self.data.get(next_point)
            if next_cell != ".":
                return next_cell


_DIRECTIONS = [
    linalg.Point(0, 1),
    linalg.Point(0, -1),
    linalg.Point(1, 1),
    linalg.Point(1, 0),
    linalg.Point(1, -1),
    linalg.Point(-1, 1),
    linalg.Point(-1, 0),
    linalg.Point(-1, -1),
]


def ParseInput(inp: str) -> Grid:
    result = {}
    for row_idx, row in enumerate(inp.splitlines()):
        for col_idx, char in enumerate(row.strip()):
            result[linalg.Point(row=row_idx, col=col_idx)] = char
    return Grid(result)


def part1():
    grid = ParseInput(problem.GetRaw(11))
    converged = grid.RunToConvergence()
    print(sum(cell == "#" for cell in converged.data.values()))


def part2():
    grid = ParseInput(problem.GetRaw(11))
    converged = grid.RunToConvergence(
        get_neighbors=AllVisible, leave_threshold=5
    )
    print(sum(cell == "#" for cell in converged.data.values()))


if __name__ == "__main__":
    part1()
    part2()
