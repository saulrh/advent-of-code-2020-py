#!/usr/bin/env python

from __future__ import annotations

import dataclasses
import re

from advent_of_code_2020_py import problem

_LINE_PARSE_REG = re.compile(
    r"(?P<n1>\d+)-(?P<n2>\d+) (?P<letter>\S): (?P<password>.+)"
)


@dataclasses.dataclass(frozen=True)
class Entry(object):
    n1: int
    n2: int
    letter: str
    password: str

    @classmethod
    def FromLine(self, line) -> Entry:
        match = _LINE_PARSE_REG.fullmatch(line.strip())
        if not match:
            raise ValueError(f"Could not parse line '{line}'")
        return Entry(
            n1=int(match.group("n1")),
            n2=int(match.group("n2")),
            letter=match.group("letter"),
            password=match.group("password"),
        )

    def Part1Valid(self):
        return self.n1 <= self.password.count(self.letter) <= self.n2

    def Part2Valid(self):
        left_correct = self.password[self.n1 - 1] == self.letter
        right_correct = self.password[self.n2 - 1] == self.letter
        return left_correct != right_correct


def part1():
    print(sum(1 for d in problem.Get(2, Entry.FromLine) if d.Part1Valid()))


def part2():
    print(sum(1 for d in problem.Get(2, Entry.FromLine) if d.Part2Valid()))


if __name__ == "__main__":
    part1()
    part2()
