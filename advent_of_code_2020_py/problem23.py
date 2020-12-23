#!/usr/bin/env python

from __future__ import annotations

import itertools
from typing import Dict, Iterable, Iterator

import attr

from advent_of_code_2020_py import debug


@attr.s(auto_attribs=True)
class Buffer(object):
    head: Node
    nodes: Dict[int, Node]
    largest: int

    @classmethod
    def Build(cls, numbers: Iterable[int]):
        prv = None
        largest = -1
        head = None
        nodes = {}
        for n in numbers:
            if head is None:
                node = Node(car=n)
                head = node
            else:
                node = Node(car=n, nxt=head, prv=prv)
                prv.nxt = node
            nodes[n] = node
            largest = max(n, largest)
            prv = node
        prv.nxt = head
        head.prv = prv
        return cls(
            head=head,
            nodes=nodes,
            largest=largest,
        )

    def __iter__(self) -> Iterator[Node]:
        n = self.head
        yield n
        n = n.nxt
        while n != self.head:
            yield n
            n = n.nxt

    def Step(self):
        dest = FindDest(self)
        head = self.head
        after_dest = dest.nxt
        held1 = self.head.nxt
        held2 = held1.nxt
        held3 = held2.nxt
        after_held = held3.nxt

        # head -> held1 ... held3 -> after_held ... dest -> after_dest ... tail
        head.SetNxt(after_held)
        # head -> after_held ... dest -> after_dest ... tail
        dest.SetNxt(held1)
        held3.SetNxt(after_dest)
        # head -> after_held ... dest -> held1 ... held3 -> after_dest ... tail
        self.head = self.head.nxt
        # after_head ... dest -> held1 ... held3 -> after_dest ... tail -> head


@attr.s(auto_attribs=True, eq=False)
class Node(object):
    car: int
    nxt: "Node" = attr.ib(factory=lambda self: self)
    prv: "Node" = attr.ib(factory=lambda self: self)

    def SetNxt(self, other):
        self.nxt = other
        other.prv = self

    def SetPrv(self, other):
        other.SetNxt(self)


def FindDest(buf: Buffer) -> Node:
    dest_num = buf.head.car
    held1 = buf.head.nxt
    held2 = held1.nxt
    held3 = held2.nxt
    held = [held1.car, held2.car, held3.car]
    while True:
        dest_num -= 1
        if dest_num < 1:
            dest_num = buf.largest
        if dest_num not in held:
            return buf.nodes[dest_num]


def Collect(buf: Buffer) -> str:
    node = buf.nodes[1]
    start = node
    node = node.nxt
    result = []
    while node != start:
        result.append(node.car)
        node = node.nxt
    return "".join(str(s) for s in result)


def Stars(buf: Buffer) -> int:
    node = buf.nodes[1]
    return node.nxt.car * node.nxt.nxt.car


INIT_STATE = [4, 1, 8, 9, 7, 6, 2, 3, 5]


def part1():
    debug.console.rule("[bold red]Part 1")
    state = Buffer.Build(INIT_STATE)
    for _ in range(100):
        state.Step()
    debug.console.log(Collect(state))


def part2():
    debug.console.rule("[bold red]Part 2")
    state = Buffer.Build(
        itertools.chain(INIT_STATE, range(max(INIT_STATE) + 1, 1000000 + 1))
    )
    for _ in range(10000000):
        state.Step()
    debug.console.log(Stars(state))


if __name__ == "__main__":
    part1()
    part2()
    debug.console.rule("[bold red]Done")
