#!/usr/bin/env python

from __future__ import annotations

import functools
import operator

from advent_of_code_2020_py import grid
from advent_of_code_2020_py import linalg
from advent_of_code_2020_py import problem


def CountTrees(hill: grid.Grid, slope: linalg.Slope) -> int:
    trees_hit = 0
    pt = linalg.Point(0, 0)
    while pt.row < hill.rows:
        if hill.Get(pt) == grid.Tile.TREE:
            trees_hit += 1
        pt += slope
    return trees_hit


def part1():
    hill = problem.GetRaw(3, grid.Grid.FromString)
    print(CountTrees(hill, linalg.Slope(over=3, down=1)))


def part2():
    hill = problem.GetRaw(3, grid.Grid.FromString)
    slopes = [
        linalg.Slope(over=1, down=1),
        linalg.Slope(over=3, down=1),
        linalg.Slope(over=5, down=1),
        linalg.Slope(over=7, down=1),
        linalg.Slope(over=1, down=2),
    ]
    print(
        functools.reduce(
            operator.mul, (CountTrees(hill, s) for s in slopes), 1
        )
    )


if __name__ == "__main__":
    part1()
    part2()
