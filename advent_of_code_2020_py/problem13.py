#!/usr/bin/env python

import dataclasses
import itertools
from typing import List, Tuple

from advent_of_code_2020_py import problem


@dataclasses.dataclass(frozen=True)
class Bus(object):
    idx: int
    period: int

    def Wait(self, t: int) -> int:
        return (self.period - (t % self.period)) % self.period


def ParseInput(data: str) -> Tuple[int, List[Bus]]:
    line1, line2 = data.splitlines()
    return int(line1), [
        Bus(idx=idx, period=int(x))
        for idx, x in enumerate(line2.split(","))
        if x.isdigit()
    ]


def NextDeparture(t: int, buses: List[Bus]) -> Tuple[Bus, int]:
    min_bus = min(buses, key=lambda b: b.Wait(t))
    return min_bus, min_bus.Wait(t)


def SolvePart2(buses: List[Bus]) -> int:
    offset = 0
    period = 1
    for bus in buses:
        n = next(
            n
            for n in itertools.count(1)
            if bus.idx % bus.period == bus.Wait(offset + n * period)
        )
        offset += n * period
        period *= bus.period
    return offset


def part1():
    t, buses = ParseInput(problem.GetRaw(13))
    bus, wait = NextDeparture(t, buses)
    print(bus.period * wait)


def part2():
    _, buses = ParseInput(problem.GetRaw(13))
    print(SolvePart2(buses))


if __name__ == "__main__":
    part1()
    part2()
