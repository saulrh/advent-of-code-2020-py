from __future__ import annotations

import dataclasses
import math


@dataclasses.dataclass(frozen=True)
class Slope(object):
    over: int
    down: int


@dataclasses.dataclass(frozen=True)
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

    def __sub__(self, other) -> Point:
        if isinstance(other, Point):
            return self + (other * -1)
        elif isinstance(other, Slope):
            return self + Slope(over=other.over * -1, down=other.down * -1)
        else:
            raise NotImplementedError(
                f"__sub__ not implemented for Point and {type(other).name}"
            )

    def __mul__(self, other: int) -> Point:
        return Point(
            col=self.col * other,
            row=self.row * other,
        )

    def RotateClockwise(self, theta: int) -> Point:
        return Point(
            col=int(
                round(
                    self.col * math.cos(math.radians(theta))
                    - self.row * math.sin(math.radians(theta))
                )
            ),
            row=int(
                round(
                    self.col * math.sin(math.radians(theta))
                    + self.row * math.cos(math.radians(theta))
                )
            ),
        )
