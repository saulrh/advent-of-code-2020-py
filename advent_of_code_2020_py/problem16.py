#!/usr/bin/env python
import copy
import dataclasses
import itertools
import re
from typing import Dict, Iterable, Iterator, List, Sequence, Tuple

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem


@dataclasses.dataclass(frozen=True)
class Rule(object):
    field: str

    lower_lower: int
    lower_upper: int
    upper_lower: int
    upper_upper: int

    def __call__(self, field: int) -> bool:
        return (self.lower_lower <= field <= self.lower_upper) or (
            self.upper_lower <= field <= self.upper_upper
        )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return (
            f"<{self.field}: "
            + f"{self.lower_lower}-{self.lower_upper}"
            + " or "
            + f"{self.upper_lower}-{self.upper_upper}>"
        )


@dataclasses.dataclass
class ProblemStatement(object):
    rules: List[Rule] = dataclasses.field(default_factory=list)
    your_ticket: List[int] = dataclasses.field(default_factory=list)
    tickets: List[List[int]] = dataclasses.field(default_factory=list)

    def GetRule(self, field: str) -> Rule:
        return next(r for r in self.rules if r.field == field)

    def KnownInvalidTickets(self) -> Iterator[Tuple[List[int], List[int]]]:
        for t in self.tickets:
            if invalids := self.KnownInvalidFields(t):
                yield t, invalids

    def KnownInvalidFields(self, t: Iterable[int]) -> List[int]:
        invalids = []
        for x in t:
            if all(not r(x) for r in self.rules):
                invalids.append(x)
        return invalids

    def ValidTickets(self) -> Iterator[List[int]]:
        for t in self.tickets:
            if not self.KnownInvalidFields(t):
                yield t

    def DiscardInvalidTickets(self):
        self.tickets = list(self.ValidTickets())


_RULE_REGEX = re.compile(
    r"(?P<field>.*): "
    + r"(?P<lower_lower>\d+)"
    + r"-"
    + r"(?P<lower_upper>\d+)"
    + r" or "
    + r"(?P<upper_lower>\d+)"
    + r"-"
    + r"(?P<upper_upper>\d+)"
)


def ParseRule(line: str) -> Rule:
    match = _RULE_REGEX.fullmatch(line)
    if not match:
        raise ValueError(f"Could not parse '{line}'")
    return Rule(
        field=match.group("field"),
        lower_lower=int(match.group("lower_lower")),
        lower_upper=int(match.group("lower_upper")),
        upper_lower=int(match.group("upper_lower")),
        upper_upper=int(match.group("upper_upper")),
    )


def Parse(ticket: Iterable[str]) -> ProblemStatement:
    it = iter(ticket)
    result = ProblemStatement()

    def Next():
        return next(it).strip()

    line = Next()
    while line:
        result.rules.append(ParseRule(line))
        line = Next()

    line = Next()
    assert line == "your ticket:"
    line = Next()

    result.your_ticket = [int(x) for x in line.split(",")]
    line = Next()
    line = Next()
    assert line == "nearby tickets:"

    for line in it:
        line = line.strip()
        result.tickets.append([int(x) for x in line.split(",")])

    return result


def PossibleColumns(
    tickets: Sequence[Sequence[int]], rules: Iterable[Rule]
) -> Dict[Rule, int]:
    all_columns = set(range(len(tickets[0])))
    columns = {r: copy.deepcopy(all_columns) for r in rules}
    while any(len(cs) > 1 for cs in columns.values()):
        for r, t, col in itertools.product(rules, tickets, all_columns):
            if col in columns[r]:
                if not r(t[col]):
                    columns[r].discard(col)
        for r in rules:
            cols = columns[r]
            if len(cols) == 1:
                for other_r, other_cs in columns.items():
                    if other_r != r:
                        other_cs -= cols
    result = {r: next(iter(cols)) for r, cols in columns.items()}
    return result


def part1():
    debug.console.rule("[bold red]Part 1")
    p = Parse(problem.Get(16))
    debug.console.log(
        sum(sum(invalids) for _, invalids in p.KnownInvalidTickets())
    )


def part2():
    debug.console.rule("[bold red]Part 2")
    p = Parse(problem.Get(16))
    p.DiscardInvalidTickets()
    columns = PossibleColumns(p.tickets, p.rules)
    result = 1
    for rule, column in columns.items():
        if rule.field.startswith("departure "):
            result *= p.your_ticket[column]
    debug.console.log(result)


if __name__ == "__main__":
    part1()
    part2()
