#!/usr/bin/env python

from __future__ import annotations

import multiprocessing
from typing import Tuple

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem


def Forward(loop_size: int, subject: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject
        value %= 20201227
    return value


def Test(args: Tuple[int, int, int]) -> Tuple[int, int]:
    subject, public, loop_size = args
    return loop_size, Forward(loop_size, subject) == public


def Reverse(public: int, subject: int) -> int:
    with multiprocessing.Pool(10) as p:
        for ls, success in p.imap_unordered(
            Test, ((subject, public, ls) for ls in range(1000000000))
        ):
            if success:
                return ls
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
