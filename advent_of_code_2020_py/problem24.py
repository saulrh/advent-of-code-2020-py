#!/usr/bin/env python

from __future__ import annotations

from typing import Iterator, Set

import regex

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import linalg
from advent_of_code_2020_py import problem

_MOVE_RE = regex.compile(r"(?P<move>e|w|se|sw|ne|nw)+")


def Neighbors(pt: linalg.Point) -> Iterator[linalg.Point]:
    yield pt + linalg.Point(row=0, col=1)
    yield pt + linalg.Point(row=0, col=-1)
    yield pt + linalg.Point(row=1, col=0)
    yield pt + linalg.Point(row=1, col=-1)
    yield pt + linalg.Point(row=-1, col=1)
    yield pt + linalg.Point(row=-1, col=0)


def Movement(instructions: str) -> linalg.Point:
    match = _MOVE_RE.fullmatch(instructions.strip())
    position = linalg.Point(0, 0)
    for move in match.captures("move"):
        if move == "e":
            position += linalg.Point(row=0, col=1)
        elif move == "w":
            position += linalg.Point(row=0, col=-1)
        elif move == "se":
            position += linalg.Point(row=1, col=0)
        elif move == "sw":
            position += linalg.Point(row=1, col=-1)
        elif move == "ne":
            position += linalg.Point(row=-1, col=1)
        elif move == "nw":
            position += linalg.Point(row=-1, col=0)
    return position


def InitialTiles(flips: Iterator[linalg.Point]) -> Set[linalg.Point]:
    tiles = set()
    for flip in flips:
        if flip in tiles:
            tiles.remove(flip)
        else:
            tiles.add(flip)
    return tiles


def Step(tiles: Set[linalg.Point]) -> Set[linalg.Point]:
    next_tiles = set()
    for possible_tile in tiles:
        for tile in Neighbors(possible_tile):
            live_count = len(tiles & set(Neighbors(tile)))
            if tile in tiles and live_count in [1, 2]:
                next_tiles.add(tile)
            if tile not in tiles and live_count == 2:
                next_tiles.add(tile)
    return next_tiles


def part1():
    debug.console.rule("[bold red]Part 1")
    tiles = InitialTiles(Movement(line) for line in problem.Get(24))
    debug.console.log(len(tiles))


def part2():
    debug.console.rule("[bold red]Part 2")
    tiles = InitialTiles(Movement(line) for line in problem.Get(24))
    for i in range(100):
        tiles = Step(tiles)
    debug.console.log(len(tiles))


if __name__ == "__main__":
    part1()
    part2()
    debug.console.rule("[bold red]Done")
