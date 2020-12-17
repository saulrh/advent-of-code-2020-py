#!/usr/bin/env python

from __future__ import annotations

import functools
import itertools
from typing import Set, Tuple

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem

Point = Tuple[int, ...]


def Add(p1: Point, p2: Point) -> Point:
    return tuple(a + b for a, b in zip(p1, p2))


def Parse(
    inp: str,
    dimension: int,
) -> Set[Point]:
    data = set()
    extra_dims = [0] * (dimension - 2)
    for x1, line in enumerate(inp.splitlines()):
        for x2, char in enumerate(line):
            if char == "#":
                data.add(tuple([x1, x2, *extra_dims]))
    return data


def Step(state: Set[Point]) -> Set[Point]:
    dimension = len(next(iter(state)))
    live_cells = set(
        Add(n, p) for n, p in itertools.product(state, Neighborhood(dimension))
    )
    new = set()
    for cell in live_cells:
        active = cell in state
        ns = {Add(cell, n) for n in Neighbors(dimension)}
        active_neighbors = len(state & ns)
        if active and active_neighbors in [2, 3]:
            new.add(cell)
        elif not active and active_neighbors == 3:
            new.add(cell)
    return new


@functools.lru_cache
def Neighborhood(dimension: int) -> Set[Point]:
    return {
        tuple(xs) for xs in itertools.product([-1, 0, 1], repeat=dimension)
    }


def Neighbors(dimension: int) -> Set[Point]:
    zero = tuple([0] * dimension)
    return Neighborhood(dimension) - {zero}


def part1():
    debug.console.rule("[bold red]Part 1")
    p = Parse(problem.GetRaw(17), dimension=3)
    for _ in range(0, 6):
        p = Step(p)
    debug.console.log(len(p))


def part2():
    debug.console.rule("[bold red]Part 2")
    p = Parse(problem.GetRaw(17), dimension=4)
    for _ in range(0, 6):
        p = Step(p)
    debug.console.log(len(p))


if __name__ == "__main__":
    part1()
    part2()
