#!/usr/bin/env python

from __future__ import annotations

import re
from typing import List

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem


def Tokenize(s: str) -> List[str]:
    return list(re.sub(r"\s+", "", s))


def Compute(s: str):
    pass


def part1():
    debug.console.rule("[bold red]Part 1")
    debug.console.log(Compute(problem.GetRaw(18)))


def part2():
    debug.console.rule("[bold red]Part 2")


if __name__ == "__main__":
    part1()
    part2()
