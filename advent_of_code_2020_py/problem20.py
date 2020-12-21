#!/usr/bin/env python

from __future__ import annotations

import collections
import enum
import functools
import itertools
import math
import re
from typing import Dict, Iterable, Iterator, List, Set, Tuple

import attr
import more_itertools
import numpy

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem

_EdgeHashType = str


def BaseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    # from https://stackoverflow.com/a/2267428
    return ((num == 0) and numerals[0]) or (
        BaseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b]
    )


def EdgeHash(e: Iterable[bool]) -> _EdgeHashType:
    return "".join("#" if x else "." for x in e)
    # val = sum(2**i for i, v in enumerate(e) if v)
    # return BaseN(val, 36)


@enum.unique
class Orientation(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    FLIP_UP = 4
    FLIP_RIGHT = 5
    FLIP_DOWN = 6
    FLIP_LEFT = 7

    @functools.cached_property
    def flipped(self):
        if self.value >= 4:
            return Orientation(self.value - 4)
        else:
            return Orientation(self.value + 4)


@enum.unique
class Side(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


@attr.s()
class Tile(object):
    tile_id: int = attr.ib()
    data = attr.ib(default=numpy.ndarray(shape=(0, 0), dtype=bool))

    @functools.cached_property
    def rotated90(self) -> Tile:
        return Tile(tile_id=self.tile_id, data=numpy.rot90(self.data))

    @functools.cached_property
    def flipped(self) -> Tile:
        return Tile(tile_id=self.tile_id, data=numpy.fliplr(self.data))

    def __str__(self) -> str:
        rows = []
        for r in self.data:
            row = []
            for c in r:
                row.append("#" if c else ".")
            rows.append(row)
        return "\n".join("".join(row) for row in rows)

    def __getitem__(self, key: Tuple[int, int, Orientation]) -> bool:
        r, c, o = key

        if o == Orientation.UP:
            return self.data[r, c]
        elif o == Orientation.LEFT:
            return self.rotated90[r, c, Orientation.UP]
        elif o == Orientation.DOWN:
            return self.rotated90[r, c, Orientation.LEFT]
        elif o == Orientation.RIGHT:
            return self.rotated90[r, c, Orientation.DOWN]
        if o.value >= 4:
            return self.flipped[r, c, o.flipped]
        else:
            raise ValueError("Unknown orientation")

    def EdgeHash(self, orientation: Orientation, side: Side) -> _EdgeHashType:
        return EdgeHash(self.Edge(orientation, side))

    def Edge(self, orientation: Orientation, side: Side) -> Tuple[bool, ...]:
        eps = EdgePoints(self.data.shape[0], side)
        return tuple(self[pt[0], pt[1], orientation] for pt in eps)

    @functools.cached_property
    def all_edge_hashes(self) -> Set[_EdgeHashType]:
        result = set()
        for o, s in itertools.product(Orientation, Side):
            result.add(self.EdgeHash(o, s))
        return result

    @classmethod
    def FromStr(cls, block: str) -> Tile:
        head, rest = block.split("\n", maxsplit=1)
        match = re.search(r"\d+", head)
        if not match:
            raise ValueError(f"could not parse {head}")
        tile_id = int(match.group())
        data = numpy.ndarray(dtype=bool, shape=(10, 10))
        for row_idx, row in enumerate(rest.splitlines()):
            for col_idx, char in enumerate(row):
                data[row_idx, col_idx] = char == "#"
        return cls(tile_id=tile_id, data=data)


@functools.lru_cache
def EdgePoints(w: int, side: Side) -> List[List[Tuple[int, int]]]:
    return [
        # Top from left to right
        [(0, col) for col in range(w)],
        # Right from top to bottom
        [(row, 9) for row in range(w)],
        # Bottom from left to right
        [(9, col) for col in range(w)],
        # Left form top to bottom
        [(row, 0) for row in range(w)],
    ][side.value]


def FromStr(s: str) -> Iterator[Tile]:
    for block in s.split("\n\n"):
        yield Tile.FromStr(block)


def Solve(
    tiles: Dict[int, Tile]
) -> Dict[Tuple[int, int], Tuple[int, Orientation]]:
    w = int(math.sqrt(len(tiles)))
    all_edges = itertools.chain.from_iterable(
        t.all_edge_hashes for t in tiles.values()
    )
    edge_counts = collections.Counter(all_edges)
    unique_edges = {k for k, v in edge_counts.items() if v == 1}
    corners = [
        t for t in tiles.values() if len(t.all_edge_hashes & unique_edges) == 2
    ]

    # Top-left corner
    solution = {}
    solution[0, 0] = (corners[0].tile_id, Orientation.UP)

    for r, c in itertools.product(range(w), repeat=2):
        if r == 0 and c == 0:
            continue
        elif c == 0:
            last_tile_id, last_tile_orientation = solution[r - 1, c]
            last_tile_side = Side.DOWN
            next_tile_side = Side.UP
        else:
            last_tile_id, last_tile_orientation = solution[r, c - 1]
            last_tile_side = Side.RIGHT
            next_tile_side = Side.LEFT
        last_tile = tiles[last_tile_id]
        debug.console.log(f"last tile: {last_tile_id}")
        last_edge_hash = last_tile.EdgeHash(
            last_tile_orientation, last_tile_side
        )
        debug.console.log(f"  last edge: {last_edge_hash} {last_tile_side}")
        for t, o in itertools.product(tiles.values(), Orientation):
            if t != last_tile and last_edge_hash == t.EdgeHash(
                o, next_tile_side
            ):
                next_tile, next_tile_orientation = t, o
                break
        debug.console.log(
            f"  next tile: {next_tile.tile_id} {next_tile_orientation}"
        )
        solution[r, c] = (next_tile.tile_id, next_tile_orientation)
        last_tile = next_tile
        last_tile_orientation = next_tile_orientation

    return solution


def StitchSolution(
    tiles: Dict[int, Tile],
    solution: Dict[Tuple[int, int], Tuple[int, Orientation]],
) -> str:
    def GetPt(r, c, ir, ic):
        tile_id, orient = solution[r, c]
        tile = tiles[tile_id]
        return tile[ir, ic, orient]

    w = int(math.sqrt(len(tiles)))
    output = {}
    # Chop off the rightmost column and bottom row of each tile
    for r, c, ir, ic in itertools.product(
        range(w), range(w), range(9), range(9)
    ):
        output[w * (r * 10 + ir) + (c * 10 + ic)] = GetPt(r, c, ir, ic)

    # populate the rightmost column
    c = w - 1
    ic = 9
    for r, ir in itertools.product(range(w), range(9)):
        output[w * (r * 10 + ir) + (c * 10 + ic)] = GetPt(r, c, ir, ic)

    # populate the bottom row
    r = w - 1
    ir = 9
    for c, ic in itertools.product(range(w), range(9)):
        output[w * (r * 10 + ir) + (c * 10 + ic)] = GetPt(r, c, ir, ic)

    # populate the bottom-right corner
    r = w - 1
    ir = 9
    c = w - 1
    ic = 9
    output[w * (r * 10 + ir) + (c * 10 + ic)] = GetPt(r, c, ir, ic)

    output_list = [None] * len(output)
    for idx, value in output.items():
        output_list[idx] = value
    rows = []
    for row in more_itertools.chunked(output_list, w * 9):
        rows.append("".join("X" if r else " " for r in row))
    return "\n".join(rows)


def part1():
    debug.console.rule("[bold red]Part 1")
    tiles = list(FromStr(problem.GetRaw(20)))
    debug.console.log(tiles)
    # debug.console.log(functools.reduce(
    #     operator.mul,
    #     (t.tile_id for t in tiles_with_two_unique_edges)))
    # debug.console.log(collections.Counter(edge_counts.values()))


def part2():
    debug.console.rule("[bold red]Part 2")


if __name__ == "__main__":
    part1()
    part2()
