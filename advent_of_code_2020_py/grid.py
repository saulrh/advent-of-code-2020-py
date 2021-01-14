from __future__ import annotations

import dataclasses
import enum
import functools
from typing import Mapping, Tuple

from advent_of_code_2020_py import linalg


class Axis(enum.Enum):
    ROW = enum.auto()
    COL = enum.auto()


class Direction(enum.Enum):
    LOW = enum.auto()
    HIGH = enum.auto()


class Side(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
    FORWARD = enum.auto()
    BACKWARD = enum.auto()

    def AD(self) -> Tuple[Axis, Direction]:
        if self == Side.UP:
            return (Axis.ROW, Direction.LOW)
        elif self == Side.DOWN:
            return (Axis.ROW, Direction.HIGH)
        elif self == Side.LEFT:
            return (Axis.COL, Direction.LOW)
        elif self == Side.RIGHT:
            return (Axis.COL, Direction.HIGH)
        else:
            raise ValueError(f"{self} does not correspond to an axis")


class BoundaryBehavior(enum.Enum):
    WRAP = enum.auto()
    OUT_OF_BOUNDS = enum.auto()


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


@dataclasses.dataclass(frozen=True)
class Grid(object):
    tiles: Mapping[linalg.Point, Tile]
    boundary_behaviors: Mapping[Tuple[Axis, Direction], BoundaryBehavior]

    def bound(self, axis: Axis, direction: Direction) -> int:
        if direction == Direction.LOW:
            return 0
        if axis == Axis.ROW:
            return self.rows
        elif axis == Axis.COL:
            return self.cols
        else:
            raise ValueError(f"Unknown axis {axis}")

    @functools.cached_property
    def cols(self) -> int:
        return 1 + max(pt.col for pt in self.tiles.keys())

    @functools.cached_property
    def rows(self) -> int:
        return 1 + max(pt.row for pt in self.tiles.keys())

    def __post_init__(self):
        # work around frozen=True as suggested by attrs docs
        object.__setattr__(
            self,
            "boundary_behaviors",
            {
                Side.UP.AD(): BoundaryBehavior.OUT_OF_BOUNDS,
                Side.DOWN.AD(): BoundaryBehavior.OUT_OF_BOUNDS,
                Side.LEFT.AD(): BoundaryBehavior.OUT_OF_BOUNDS,
                Side.RIGHT.AD(): BoundaryBehavior.OUT_OF_BOUNDS,
                **self.boundary_behaviors,
            },
        )

    def _Normalize(self, axis: Axis, value: int) -> int:
        lower = self.bound(axis, Direction.LOW)
        upper = self.bound(axis, Direction.HIGH)

        if value < lower:
            direction = Direction.LOW
        elif value >= upper:
            direction = Direction.HIGH
        else:
            # In range
            return value

        # we're out of range, so see if we should normalize
        behavior = self.boundary_behaviors[axis, direction]
        if behavior == BoundaryBehavior.OUT_OF_BOUNDS:
            raise ValueError(f"{axis} {value} is out of bounds in {direction}")
        elif behavior == BoundaryBehavior.WRAP:
            return value % upper
        else:
            raise ValueError(f"Unknown boundary behavior {behavior}")

    def Get(self, coord: linalg.Point) -> Tile:
        normalized = linalg.Point(
            row=self._Normalize(Axis.ROW, coord.row),
            col=self._Normalize(Axis.COL, coord.col),
        )
        return self.tiles[normalized]

    @classmethod
    def FromString(
        cls,
        inp: str,
        bounds: Mapping[Tuple[Axis, Direction], BoundaryBehavior] = {},
    ) -> Grid:
        data = dict()
        for row_idx, line in enumerate(inp.splitlines()):
            for col_idx, char in enumerate(line):
                pt = linalg.Point(row=row_idx, col=col_idx)
                data[pt] = Tile.FromChar(char)
        return cls(tiles=data, boundary_behaviors=bounds)
