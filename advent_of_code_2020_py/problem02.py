#!/usr/bin/env python

import collections
import dataclasses
import re
from typing import List


@dataclasses.dataclass
class Entry(object):
    n1: int
    n2: int
    letter: str
    password: str

    def Part1Valid(self):
        counts = collections.Counter(self.password)
        return self.n1 <= counts[self.letter] <= self.n2

    def Part2Valid(self):
        l1 = self.password[self.n1 - 1] == self.letter
        l2 = self.password[self.n2 - 1] == self.letter
        return l1 != l2


LINE_PARSE_REG = re.compile(
    r"(?P<n1>\d+)-(?P<n2>\d+) (?P<letter>\S): (?P<password>.+)"
)


def ParseEntry(line: str) -> Entry:
    match = LINE_PARSE_REG.fullmatch(line.strip())
    if not match:
        raise ValueError(f"Could not parse line '{line}'")
    return Entry(
        n1=int(match.group("n1")),
        n2=int(match.group("n2")),
        letter=match.group("letter"),
        password=match.group("password"),
    )


def get_data() -> List[Entry]:
    with open("inputs/problem02.part1.csv", "r") as f:
        return [ParseEntry(line) for line in f]


def part1():
    data = get_data()
    print(sum(1 for d in data if d.Part1Valid()))


def part2():
    data = get_data()
    print(sum(1 for d in data if d.Part2Valid()))


if __name__ == "__main__":
    part1()
    part2()
