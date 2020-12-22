#!/usr/bin/env python

from __future__ import annotations

import itertools
from typing import List, Optional, Set

import attr

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem


@attr.s(auto_attribs=True)
class State(object):
    decka: List[int]
    deckb: List[int]
    winner: Optional[str] = None
    visited: Set[int] = attr.ib(factory=set)

    def Step(self, recurse: bool):
        def VictorySimple(a, b):
            if a > b:
                return "a"
            else:
                return "b"

        def VictoryRecursive(a, b):
            if len(self.decka) < a or len(self.deckb) < b:
                return VictorySimple(a=a, b=b)

            nextstate = State(
                decka=list(self.decka[:a]),
                deckb=list(self.deckb[:b]),
            )
            return nextstate.Run(recurse)

        if self.signature in self.visited:
            self.winner = "a"
            return

        self.visited.add(self.signature)

        if recurse:
            victory = VictoryRecursive
        else:
            victory = VictorySimple

        a, b = self.decka.pop(0), self.deckb.pop(0)
        if victory(a=a, b=b) == "a":
            self.decka.append(a)
            self.decka.append(b)
        else:
            self.deckb.append(b)
            self.deckb.append(a)

        if not self.decka:
            self.winner = "b"
        if not self.deckb:
            self.winner = "a"

    @property
    def signature(self) -> int:
        return hash(tuple(itertools.chain(self.decka, [-1], self.deckb)))

    def Run(self, recurse) -> str:
        while not self.winner:
            self.Step(recurse)
        return self.winner

    @property
    def valuea(self) -> int:
        return sum(
            (idx + 1) * card for idx, card in enumerate(reversed(self.decka))
        )

    @property
    def valueb(self) -> int:
        return sum(
            (idx + 1) * card for idx, card in enumerate(reversed(self.deckb))
        )

    @property
    def value_winner(self) -> Optional[int]:
        if self.winner == "a":
            return self.valuea
        elif self.winner == "b":
            return self.valueb
        else:
            return None

    @classmethod
    def FromStr(cls, s: str) -> State:
        player_a, player_b = s.split("\n\n")
        return cls(
            decka=list(int(x) for x in player_a.splitlines()[1:]),
            deckb=list(int(x) for x in player_b.splitlines()[1:]),
        )


def part1():
    debug.console.rule("[bold red]Part 1")
    state = State.FromStr(problem.GetRaw(22))
    state.Run(False)
    debug.console.log(state.value_winner)


def part2():
    debug.console.rule("[bold red]Part 2")
    state = State.FromStr(problem.GetRaw(22))
    state.Run(True)
    debug.console.log(state.value_winner)


if __name__ == "__main__":
    part1()
    part2()
    debug.console.rule("[bold red]Done")
