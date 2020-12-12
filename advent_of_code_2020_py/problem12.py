#!/usr/bin/env python

from __future__ import annotations

import enum
import re
from typing import Iterable

import attr

from advent_of_code_2020_py import linalg
from advent_of_code_2020_py import problem


@enum.unique
class Direction(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def Left(self):
        return Direction((self.value - 1) % 4)

    def Right(self):
        return Direction((self.value + 1) % 4)

    def Movement(self):
        if self == Direction.NORTH:
            return linalg.Point(row=-1, col=0)
        elif self == Direction.EAST:
            return linalg.Point(row=0, col=1)
        elif self == Direction.SOUTH:
            return linalg.Point(row=1, col=0)
        elif self == Direction.WEST:
            return linalg.Point(row=0, col=-1)
        else:
            raise ValueError(f"Invalid direction {self}")


@attr.s(auto_attribs=True, frozen=True)
class Ship(object):
    direction: Direction = Direction.EAST
    position: linalg.Point = linalg.Point(0, 0)

    def Translate(self, pt: linalg.Point) -> Ship:
        return Ship(
            direction=self.direction,
            position=self.position + pt,
        )

    def Command(self, c: str) -> Ship:
        match = INPUT_REGEX.match(c.strip())
        if not match:
            raise ValueError("Could not parse")
        command = match.group("command")
        value = int(match.group("value"))
        if command == "N":
            return self.Translate(Direction.NORTH.Movement() * value)
        elif command == "E":
            return self.Translate(Direction.EAST.Movement() * value)
        elif command == "S":
            return self.Translate(Direction.SOUTH.Movement() * value)
        elif command == "W":
            return self.Translate(Direction.WEST.Movement() * value)
        elif command == "L":
            state = self
            for _ in range(0, value, 90):
                state = Ship(
                    direction=state.direction.Left(),
                    position=state.position,
                )
            return state
        elif command == "R":
            state = self
            for _ in range(0, value, 90):
                state = Ship(
                    direction=state.direction.Right(),
                    position=state.position,
                )
            return state
        elif command == "F":
            return self.Translate(self.direction.Movement() * value)
        raise ValueError(f"Invalid command: {command}, {value}")

    def ApplyInputs(self, inputs: Iterable[str]) -> Ship:
        state = self
        for line in inputs:
            state = state.Command(line)
        return state


@attr.s(auto_attribs=True, frozen=True)
class WaypointShip(object):
    waypoint: linalg.Point = linalg.Point(row=-1, col=10)
    position: linalg.Point = linalg.Point(0, 0)

    def TranslateWaypoint(self, pt: linalg.Point) -> WaypointShip:
        return WaypointShip(
            waypoint=self.waypoint + pt,
            position=self.position,
        )

    def Command(self, c: str) -> WaypointShip:
        match = INPUT_REGEX.match(c.strip())
        if not match:
            raise ValueError("Could not parse")
        command = match.group("command")
        value = int(match.group("value"))
        if command == "N":
            return self.TranslateWaypoint(Direction.NORTH.Movement() * value)
        elif command == "E":
            return self.TranslateWaypoint(Direction.EAST.Movement() * value)
        elif command == "S":
            return self.TranslateWaypoint(Direction.SOUTH.Movement() * value)
        elif command == "W":
            return self.TranslateWaypoint(Direction.WEST.Movement() * value)
        elif command == "L":
            return WaypointShip(
                position=self.position,
                waypoint=self.waypoint.RotateClockwise(-value),
            )
        elif command == "R":
            return WaypointShip(
                position=self.position,
                waypoint=self.waypoint.RotateClockwise(value),
            )
        elif command == "F":
            return WaypointShip(
                waypoint=self.waypoint,
                position=self.position + self.waypoint * value,
            )
        else:
            raise ValueError(f"Invalid command: {command}, {value}")

    def ApplyInputs(self, inputs: Iterable[str]) -> WaypointShip:
        state = self
        for line in inputs:
            state = state.Command(line.strip())
        return state


INPUT_REGEX = re.compile(r"(?P<command>[NSEWLRF])(?P<value>\d+)")


def part1():
    state = Ship()
    state = state.ApplyInputs(problem.Get(12))
    print(abs(state.position.row) + abs(state.position.col))


def part2():
    state = WaypointShip()
    state = state.ApplyInputs(problem.Get(12))
    print(abs(state.position.row) + abs(state.position.col))


if __name__ == "__main__":
    part1()
    part2()
