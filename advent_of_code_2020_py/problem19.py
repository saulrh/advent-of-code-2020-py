#!/usr/bin/env python

from __future__ import annotations

from typing import List

import attr
import parsimonious
from parsimonious import grammar
import regex

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem


def RewriteToGrammar(inp: str) -> str:
    inp = "\n".join(sorted(inp.splitlines()))
    inp = (
        inp.replace("|", ") / (").replace(":", " = (").replace("\n", " )\n")
    ) + " )\n"
    return regex.sub(r"\d+", lambda m: "r" + m.group(), inp)


def RewriteToGrammar2(inp: str) -> str:
    return (
        RewriteToGrammar(inp)
        .replace("r8 = ( r42 )\n", "r8 = r42 / ( r42 r8 )\n")
        .replace("r11 = ( r42 r31 )\n", "r11 = ( r42 r31) / ( r42 r11 r31 )\n")
    )


@attr.s(auto_attribs=True)
class ProblemStatement(object):
    g: grammar.Grammar
    messages: List[str]

    @classmethod
    def FromStr(cls, inp: str) -> ProblemStatement:
        head, tail = inp.split("\n\n")
        rewritten = RewriteToGrammar(head)
        return cls(
            g=grammar.Grammar(rewritten),
            messages=[m.strip() for m in tail.splitlines()],
        )

    @classmethod
    def FromStr2(cls, inp: str) -> ProblemStatement:
        head, tail = inp.split("\n\n")
        rewritten = RewriteToGrammar2(head)
        debug.console.log(rewritten)
        return cls(
            g=grammar.Grammar(rewritten),
            messages=[m.strip() for m in tail.splitlines()],
        )

    def TestMessage(self, m: str) -> bool:
        try:
            self.g.parse(m)
            return True
        except parsimonious.exceptions.ParseError:
            return False


def part1():
    debug.console.rule("[bold red]Part 1")
    ps = ProblemStatement.FromStr(problem.GetRaw(19))
    debug.console.log(sum(ps.TestMessage(m) for m in ps.messages))


def part2():
    debug.console.rule("[bold red]Part 2")
    ps = ProblemStatement.FromStr2(problem.GetRaw(19))
    debug.console.log(sum(ps.TestMessage(m) for m in ps.messages))


if __name__ == "__main__":
    part1()
    part2()
