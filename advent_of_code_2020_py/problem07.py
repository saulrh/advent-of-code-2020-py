#!/usr/bin/env python

from __future__ import annotations

import collections
import functools
from typing import Callable, Mapping, Tuple, TypeVar

import regex

from advent_of_code_2020_py import perf
from advent_of_code_2020_py import problem

LINE_RE = regex.compile(
    # Initial color
    "(?P<base>.+)"
    # Fixed string, note the space on the front
    + " bags contain"
    # A non-capturing group for each repetition of the child-bag
    # statement, like "7 blue bags" or "1 green bag" or "no other
    # bags".
    + (
        "(?:"
        # Common prefix: a single space
        " "
        # A non-capturing group that we used to separate out common
        # prefix/suffix on the child-bag statement (space, "bags,")
        + (
            "(?:"
            # Option 1: "no other". Non-capturing because the absence
            # of captures is all we need.
            + "(?:no other)"
            + "|"
            # Option 2: capture the count (a series of digits) and the
            # color (a series of digits).
            + r"(?:(?P<count>\d+) (?P<color>\D+))"
            + ")"
        )
        # Common suffix: "bag" "bags," "bags.", "bag."
        + " bags?,?"
        + ")"
    )
    # Capture multiple repetitions of the child-bag capture group
    + "+"
    + r"\."
)


def LineTransform(line: str) -> Tuple[str, collections.Counter[str]]:
    match = LINE_RE.fullmatch(line.strip())
    return match.group("base"), collections.Counter(
        dict(
            zip(
                match.captures("color"),
                [int(c) for c in match.captures("count")],
            )
        )
    )


_CounterKeyType = TypeVar("_CounterKeyType")


def MultiplyCounter(
    c: collections.Counter[_CounterKeyType], x: int
) -> collections.Counter[_CounterKeyType]:
    return collections.Counter({k: v * x for k, v in c.items()})


def MakeContents(
    directs: Mapping[str, collections.Counter[str]]
) -> Callable[[str], collections.Counter[str]]:
    @functools.lru_cache
    def Contents(bag: str) -> collections.Counter[str]:
        children = directs[bag]
        total = collections.Counter()
        for (child_color, child_count) in children.items():
            # Count the bag itself
            total[child_color] += child_count
            # And then count the bags inside the bag
            total += MultiplyCounter(Contents(child_color), child_count)
        return total

    return Contents


@perf.TimedMethod
def part1():
    directs = dict(problem.Get(7, LineTransform))
    contents = MakeContents(directs)
    print(
        sum(
            "shiny gold" in contents(outermost) for outermost in directs.keys()
        )
    )


@perf.TimedMethod
def part2():
    directs = dict(problem.Get(7, LineTransform))
    contents = MakeContents(directs)
    print(sum(contents("shiny gold").values()))


if __name__ == "__main__":
    part1()
    part2()
