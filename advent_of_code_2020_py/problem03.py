#!/usr/bin/env python

from __future__ import annotations

import enum
import functools
import operator
from typing import Mapping

import attr

from advent_of_code_2020_py import problem


class Tile(enum.Enum):
    SNOW = enum.auto()
    TREE = enum.auto()

    @classmethod
    def FromChar(cls, char: str) -> Tile:
        if char == ".":
            return Tile.SNOW
        elif char == "#":
            return Tile.TREE
        else:
            raise ValueError(f"Invalid character {char} in map")


@attr.s(auto_attribs=True, frozen=True)
class Point(object):
    row: int
    col: int

    def __add__(self, other) -> Point:
        if isinstance(other, Point):
            return Point(
                row=self.row + other.row,
                col=self.col + other.col,
            )
        elif isinstance(other, Slope):
            return Point(
                row=self.row + other.down,
                col=self.col + other.over,
            )
        else:
            raise NotImplementedError(
                f"__add__ not implemented for Point and {type(other).name}"
            )


@attr.s(auto_attribs=True, frozen=True)
class Slope(object):
    over: int
    down: int


@attr.s(auto_attribs=True, frozen=True)
class Map(object):
    tiles: Mapping[Point, Tile]
    cols: int
    rows: int

    def Get(self, coord: Point) -> Tile:
        if coord.row >= self.rows:
            raise ValueError("row idx out of range")
        normalized = Point(
            row=coord.row,
            col=coord.col % self.cols,
        )
        return self.tiles[normalized]

    @classmethod
    def FromString(cls, inp: str) -> Map:
        data = dict()
        cols = 0
        rows = 0
        for row_idx, line in enumerate(inp.splitlines()):
            rows += 1
            for col_idx, char in enumerate(line):
                cols = max(cols, col_idx + 1)
                data[Point(row=row_idx, col=col_idx)] = Tile.FromChar(char)
        return Map(tiles=data, rows=rows, cols=cols)


def CountTrees(hill: Map, slope: Slope) -> int:
    trees_hit = 0
    pt = Point(0, 0)
    while pt.row < hill.rows:
        if hill.Get(pt) == Tile.TREE:
            trees_hit += 1
        pt += slope
    return trees_hit


def part1():
    hill = problem.GetRaw(3, Map.FromString)
    print(CountTrees(hill, Slope(over=3, down=1)))


def part2():
    hill = problem.GetRaw(3, Map.FromString)
    slopes = [
        Slope(over=1, down=1),
        Slope(over=3, down=1),
        Slope(over=5, down=1),
        Slope(over=7, down=1),
        Slope(over=1, down=2),
    ]
    print(
        functools.reduce(
            operator.mul, (CountTrees(hill, s) for s in slopes), 1
        )
    )


if __name__ == "__main__":
    part1()
    part2()
