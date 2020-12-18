#!/usr/bin/env python

from __future__ import annotations

import collections
import copy
import functools
import operator
import re
from typing import List, Sequence, Union

import parsimonious

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


class MathVisitor(parsimonious.NodeVisitor):
    @parsimonious.rule("product")
    def visit_expr(self, node, visited_children):
        return visited_children[0]

    @parsimonious.rule("sum product_tail*")
    def visit_product(self, node, visited_children):
        return visited_children[0] * functools.reduce(
            operator.mul, visited_children[1], 1
        )

    @parsimonious.rule('ws? "*" ws? sum')
    def visit_product_tail(self, node, visited_children):
        _, _, _, value = visited_children
        return value

    @parsimonious.rule("value sum_tail*")
    def visit_sum(self, node, visited_children):
        return visited_children[0] + sum(visited_children[1])

    @parsimonious.rule('ws? "+" ws? value')
    def visit_sum_tail(self, node, visited_children):
        _, _, _, value = visited_children
        return value

    @parsimonious.rule("num / par_expr")
    def visit_value(self, node, visited_children):
        return visited_children[0]

    @parsimonious.rule('"(" expr ")"')
    def visit_par_expr(self, node, visited_children):
        _, expr, _ = visited_children
        return expr

    @parsimonious.rule(r'~"\d+"')
    def visit_num(self, node, visited_children):
        return int(node.text)

    @parsimonious.rule(r'~"\s+"')
    def visit_ws(self, node, visited_children):
        return None

    def generic_visit(self, node, visited_children):
        return visited_children or node


def Compute2(s: str) -> int:
    vis = MathVisitor()
    return vis.parse(s)


def part1():
    debug.console.rule("[bold red]Part 1")
    debug.console.log(sum(Compute1(line) for line in problem.Get(18)))


def part2():
    debug.console.rule("[bold red]Part 2")
    debug.console.log(sum(Compute2(line.strip()) for line in problem.Get(18)))


if __name__ == "__main__":
    part1()
    part2()
