#!/usr/bin/env python

from __future__ import annotations

from typing import List

from advent_of_code_2020_py import debug


def FindDestIdx(numbers: List[int]) -> int:
    dest_num = numbers[0] - 1
    while dest_num not in numbers[4:]:
        dest_num -= 1
        if dest_num < min(numbers):
            dest_num = max(numbers)
    return numbers.index(dest_num)


def Step(numbers: List[int]) -> List[int]:
    dest_idx = FindDestIdx(numbers)
    assert dest_idx >= 4
    return (
        numbers[4 : dest_idx + 1]
        + numbers[1:4]
        + numbers[dest_idx + 1 :]
        + numbers[0:1]
    )


def Collect(numbers: List[int]) -> str:
    idx = numbers.index(1)
    seq = numbers[idx + 1 :] + numbers[:idx]
    return "".join(str(s) for s in seq)


def Stars(numbers: List[int]) -> int:
    idx = numbers.index(1)
    return numbers[idx + 1] * numbers[idx + 2]


INIT_STATE = [4, 1, 8, 9, 7, 6, 2, 3, 5]


def part1():
    debug.console.rule("[bold red]Part 1")
    state = INIT_STATE
    for _ in range(100):
        state = Step(state)
    debug.console.log(Collect(state))


def part2():
    debug.console.rule("[bold red]Part 2")


if __name__ == "__main__":
    part1()
    part2()
    debug.console.rule("[bold red]Done")
