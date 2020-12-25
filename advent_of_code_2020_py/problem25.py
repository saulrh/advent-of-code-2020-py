#!/usr/bin/env python

from __future__ import annotations

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem

CONSTANT = 20201227


def Forward(loop_size: int, subject: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= CONSTANT
    return value


def Reverse(public: int, subject: int) -> int:
    value = 1
    for loop_size in range(1, 1000000000):
        value *= subject
        value %= CONSTANT
        if value == public:
            return loop_size
    raise ValueError(f"Did not find the loop size for public key {public}")


def part1():
    debug.console.rule("[bold red]Part 1")
    card_public, door_public = [int(s.strip()) for s in problem.Get(25)]
    card_private = Reverse(card_public, 7)
    debug.console.log(card_private)
    debug.console.log(Forward(card_private, door_public))


def part2():
    debug.console.rule("[bold red]Part 2")


if __name__ == "__main__":
    part1()
    part2()
    debug.console.rule("[bold red]Done")
