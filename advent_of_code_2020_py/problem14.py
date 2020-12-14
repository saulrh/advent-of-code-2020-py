#!/usr/bin/env python

import re
from typing import Dict, Iterable, Iterator, Optional

import attr

from advent_of_code_2020_py import problem


@attr.s(auto_attribs=True)
class State:
    mask: str = "X" * 36
    memory: Dict[int, int] = attr.ib(factory=dict)

    def Interpret1(self, line: str):
        instr = ParseLine(line)
        if instr.op == "mask":
            self.mask = instr.value
        elif instr.op == "mem":
            self.memory[instr.addr] = MaskValue(self.mask, int(instr.value))
        else:
            raise ValueError(f"Invalid instruction {instr}")

    def Interpret1Program(self, program: Iterable[str]):
        for line in program:
            self.Interpret1(line)

    def Interpret2(self, line: str):
        instr = ParseLine(line)
        if instr.op == "mask":
            self.mask = instr.value
        elif instr.op == "mem":
            for mem_value in MaskAddress(self.mask, instr.addr):
                # print(self.mask, instr.addr, mem_value)
                self.memory[mem_value] = int(instr.value)
        else:
            raise ValueError(f"Invalid instruction {instr}")

    def Interpret2Program(self, program: Iterable[str]):
        for line in program:
            self.Interpret2(line)


@attr.s(auto_attribs=True, frozen=True)
class Instruction(object):
    op: str
    addr: Optional[int] = None
    value: Optional[str] = None


def MaskValue(mask: str, value: int) -> int:
    # Get all the '1' values into an int and bitwise-OR it to force
    # specific bits to 1
    set_bits = int("".join("1" if c == "1" else "0" for c in mask), 2)
    # Get all the '0' values into an int and bitwise-AND it to force
    # specific bits to 0
    cleared_bits = int("".join("0" if c == "0" else "1" for c in mask), 2)
    return cleared_bits & (set_bits | value)


def MaskAddress(mask: str, value: int) -> Iterator[int]:
    def ApplyMaskBit(mask_char: str, value_char: str) -> str:
        if mask_char == "1":
            return "1"
        elif mask_char == "X":
            return "X"
        else:
            return value_char

    def Floating(value: str) -> Iterator[int]:
        if "X" not in value:
            yield int(value)
        else:
            head, tail = value.split("X", maxsplit=1)
            assert len(head) + len(tail) == 35
            yield from Floating(head + "0" + tail)
            yield from Floating(head + "1" + tail)

    value_str = f"{value:036b}"
    masked = "".join(ApplyMaskBit(mc, vc) for (mc, vc) in zip(mask, value_str))
    yield from Floating(masked)


LINE_REGEX = re.compile(
    r"(?:(?P<mask>mask)|(?:mem\[(?P<addr>\d+)\])) = (?P<value>.*)"
)


def ParseLine(line: str) -> Instruction:
    line = line.strip()
    match = LINE_REGEX.fullmatch(line)
    if not match:
        raise ValueError(f"Could not parse line {line}")
    if match.group("mask"):
        return Instruction("mask", value=match.group("value"))
    return Instruction("mem", int(match.group("addr")), match.group("value"))


def part1():
    state = State()
    state.Interpret1Program(problem.Get(14))
    print(sum(state.memory.values()))


def part2():
    state = State()
    state.Interpret2Program(problem.Get(14))
    print(sum(state.memory.values()))


if __name__ == "__main__":
    part1()
    part2()
