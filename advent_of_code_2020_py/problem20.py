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


NORMAL_ORIENTATIONS = [
    Orientation.UP,
    Orientation.RIGHT,
    Orientation.DOWN,
    Orientation.LEFT,
]
FLIPPED_ORIENTATIONS = [
    Orientation.FLIP_UP,
    Orientation.FLIP_RIGHT,
    Orientation.FLIP_DOWN,
    Orientation.FLIP_LEFT,
]


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

    def __eq__(self, other) -> bool:
        return self.tile_id != other.tile_id

    def __str__(self) -> str:
        rows = []
        for row in self.data:
            rows.append("".join("#" if r else "." for r in row))
        return "\n".join(rows)

    def Oriented(self, o: Orientation) -> Tile:
        if o == Orientation.UP:
            return self
        elif o == Orientation.LEFT:
            return self.rotated90.Oriented(Orientation.UP)
        elif o == Orientation.DOWN:
            return self.rotated90.Oriented(Orientation.LEFT)
        elif o == Orientation.RIGHT:
            return self.rotated90.Oriented(Orientation.DOWN)
        elif o in FLIPPED_ORIENTATIONS:
            return self.flipped.Oriented(o.flipped)
        else:
            raise ValueError("Unknown orientation")

    def EdgeHash(self, orientation: Orientation, side: Side) -> _EdgeHashType:
        return EdgeHash(self.Edge(orientation, side))

    def Edge(self, orientation: Orientation, side: Side) -> Tuple[bool, ...]:
        eps = EdgePoints(self.data.shape[0], side)
        return tuple(
            self.Oriented(orientation).data[pt[0], pt[1]] for pt in eps
        )

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

    # Find a suitable top-left corner
    solution = {}
    for t, o in itertools.product(tiles.values(), Orientation):
        if (
            t.EdgeHash(o, Side.LEFT) in unique_edges
            and t.EdgeHash(o, Side.UP) in unique_edges
        ):
            solution[0, 0] = (t.tile_id, o)
            break

    for r, c in itertools.product(range(w), repeat=2):
        if r == 0 and c == 0:
            continue
        elif c == 0:
            last_tile_r, last_tile_c = r - 1, c
            last_tile_side = Side.DOWN
            next_tile_side = Side.UP
        else:
            last_tile_r, last_tile_c = r, c - 1
            last_tile_side = Side.RIGHT
            next_tile_side = Side.LEFT
        last_tile_id, last_tile_orientation = solution[
            last_tile_r, last_tile_c
        ]
        last_tile = tiles[last_tile_id]

        last_edge_hash = last_tile.EdgeHash(
            last_tile_orientation, last_tile_side
        )
        for t, o in itertools.product(tiles.values(), Orientation):
            if t.tile_id != last_tile_id and last_edge_hash == t.EdgeHash(
                o, next_tile_side
            ):
                next_tile, next_tile_orientation = t, o
                break
        assert next_tile.EdgeHash(
            next_tile_orientation, next_tile_side
        ) == last_tile.EdgeHash(last_tile_orientation, last_tile_side)
        solution[r, c] = (next_tile.tile_id, next_tile_orientation)
        last_tile = next_tile
        last_tile_orientation = next_tile_orientation

    return solution


def Stitch(
    tiles: Dict[int, Tile],
    solution: Dict[Tuple[int, int], Tuple[int, Orientation]],
) -> Tile:
    w = int(math.sqrt(len(tiles)))
    grid = numpy.ndarray((w * 8, w * 8), dtype=bool)
    for r, c in itertools.product(range(w), range(w)):
        t_id, o = solution[r, c]
        t = tiles[t_id]
        grid[r * 8 : ((r + 1) * 8), c * 8 : ((c + 1) * 8)] = t.Oriented(
            o
        ).data[1:9, 1:9]
    return Tile(
        tile_id=hash(tuple(grid.flat)),
        data=grid,
    )


SERPENT_STR = """                  #
#    ##    ##    ###
 #  #  #  #  #  #
"""


def OverlappingIntersections(
    needle: str, haystack: str
) -> Iterator[Tuple[int, int]]:
    hay_w = len(haystack.splitlines()[0])
    needle_w = len(needle.splitlines()[0])
    needle_fill = "." * (hay_w - needle_w)
    flat_needle = "".join(line + needle_fill for line in needle.splitlines())
    flat_haystack = haystack.replace("\n", "")
    for idx in range(0, len(flat_haystack) - len(flat_needle)):
        if all(
            h == "#"
            for n, h in zip(flat_needle, flat_haystack[idx:])
            if n == "#"
        ):
            yield int(idx / hay_w), int(idx % hay_w)


def SerpentCount(t: Tile) -> int:
    for o in Orientation:
        found = list(
            OverlappingIntersections(
                needle=SERPENT_STR,
                haystack=str(t.Oriented(o)),
            )
        )
        if found:
            return len(found)
    raise RuntimeError("Found no serpents")


def Roughness(t: Tile) -> int:
    serpents = SerpentCount(t)
    waves = sum(c == "#" for c in str(t))
    serpent_size = sum(c == "#" for c in SERPENT_STR)
    return waves - (serpent_size * serpents)


def part1():
    debug.console.rule("[bold red]Part 1")
    tiles = {t.tile_id: t for t in FromStr(problem.GetRaw(20))}
    solution = Solve(tiles)
    debug.console.log(
        solution[0, 0][0]
        * solution[0, 11][0]
        * solution[11, 0][0]
        * solution[11, 11][0]
    )


def part2():
    debug.console.rule("[bold red]Part 2")
    tiles = {t.tile_id: t for t in FromStr(problem.GetRaw(20))}
    solution = Solve(tiles)
    stitched = Stitch(tiles, solution)
    debug.console.log(Roughness(stitched))


if __name__ == "__main__":
    part1()
    part2()
    debug.console.rule("[bold red]Done")
