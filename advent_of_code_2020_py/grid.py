from __future__ import annotations

import enum
from typing import Mapping

import attr

from advent_of_code_2020_py import linalg


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
            raise ValueError(f"Invalid character {char} in grid")


@attr.s(auto_attribs=True, frozen=True)
class Grid(object):
    tiles: Mapping[linalg.Point, Tile]
    cols: int
    rows: int

    def Get(self, coord: linalg.Point) -> Tile:
        if coord.row >= self.rows:
            raise ValueError("row idx out of range")
        normalized = linalg.Point(
            row=coord.row,
            col=coord.col % self.cols,
        )
        return self.tiles[normalized]

    @classmethod
    def FromString(cls, inp: str) -> Grid:
        data = dict()
        cols = 0
        rows = 0
        for row_idx, line in enumerate(inp.splitlines()):
            rows += 1
            for col_idx, char in enumerate(line):
                cols = max(cols, col_idx + 1)
                pt = linalg.Point(row=row_idx, col=col_idx)
                data[pt] = Tile.FromChar(char)
        return cls(tiles=data, rows=rows, cols=cols)
