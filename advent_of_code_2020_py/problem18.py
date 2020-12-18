#!/usr/bin/env python

from __future__ import annotations

import collections
import copy
import re
from typing import List, Sequence, Union

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem


def Tokenize1(s: str) -> List[Union[str, int]]:
    return [int(t) if t.isdigit() else t for t in re.sub(r"\s+", "", s)]


def Group1(toks: Sequence[str]) -> List[str]:
    toks = list(toks)
    stack = collections.deque()
    idx = 0
    while idx < len(toks):
        if toks[idx] == "(":
            stack.append(idx)
        elif toks[idx] == ")":
            start = stack.pop()
            end = idx
            replacement = toks[start + 1 : end]
            toks[start : end + 1] = [replacement]
            idx = start
        idx += 1
    return toks


def ProcessTree1(toks):
    toks = copy.deepcopy(toks)
    for idx1 in range(len(toks)):
        tok = toks[idx1]
        if type(tok) == list:
            value = ProcessTree1(tok)
            toks[idx1] = value

    idx2 = 0
    while idx2 < len(toks):
        tok = toks[idx2]
        if tok == "+":
            toks[idx2 - 1 : idx2 + 2] = [toks[idx2 - 1] + toks[idx2 + 1]]
            idx2 -= 2
        elif tok == "*":
            toks[idx2 - 1 : idx2 + 2] = [toks[idx2 - 1] * toks[idx2 + 1]]
            idx2 -= 2
        elif type(tok) == int:
            idx2 += 1
        else:
            raise ValueError(f"Can't handle: {tok}")

    assert len(toks) == 1
    return toks[0]


def Compute1(s: str):
    return ProcessTree1(Group1(Tokenize1(s)))


def part1():
    debug.console.rule("[bold red]Part 1")
    debug.console.log(sum(Compute1(line) for line in problem.Get(18)))


def part2():
    debug.console.rule("[bold red]Part 2")


if __name__ == "__main__":
    part1()
    part2()
