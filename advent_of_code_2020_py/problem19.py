#!/usr/bin/env python

from __future__ import annotations

from typing import List

import attr
import lark
import regex

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem


def RewriteToGrammar(inp: str) -> str:
    def RewriteLine(line):
        return regex.sub(r"\d+", lambda m: "r" + m.group(), line)

    return "\n".join(RewriteLine(line) for line in inp.splitlines())


def RewriteForPart2(inp: str) -> str:
    inp = inp.replace("8: 42", "8: 42 | 42 8")
    return inp.replace("11: 42 31", "11: 42 31 | 42 11 31")


@attr.s(auto_attribs=True)
class ProblemStatement(object):
    g: lark.Lark
    messages: List[str]

    @classmethod
    def FromStr(cls, inp: str) -> ProblemStatement:
        head, tail = inp.split("\n\n")
        return cls(
            g=lark.Lark(RewriteToGrammar(head), start="r0"),
            messages=[m.strip() for m in tail.splitlines()],
        )

    def TestMessage(self, m: str) -> bool:
        try:
            self.g.parse(m)
            return True
        except lark.exceptions.UnexpectedCharacters:
            return False
        except lark.exceptions.UnexpectedEOF:
            return False


def part1():
    debug.console.rule("[bold red]Part 1")
    ps = ProblemStatement.FromStr(problem.GetRaw(19))
    debug.console.log(sum(ps.TestMessage(m) for m in ps.messages))


def part2():
    debug.console.rule("[bold red]Part 2")
    ps = ProblemStatement.FromStr(RewriteForPart2(problem.GetRaw(19)))
    debug.console.log(sum(ps.TestMessage(m) for m in ps.messages))


if __name__ == "__main__":
    part1()
    part2()
