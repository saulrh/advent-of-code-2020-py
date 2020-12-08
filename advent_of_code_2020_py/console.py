#!/usr/bin/env python

from __future__ import annotations

import enum
import re
from typing import List

import attr


@attr.s(auto_attribs=True, frozen=True)
class State(object):
    accumulator: int = 0
    next_instruction: int = 0
    halted: bool = False


@enum.unique
class Operation(enum.Enum):
    ACC = enum.auto()
    JMP = enum.auto()
    NOP = enum.auto()


@attr.s(auto_attribs=True, frozen=True)
class Instruction(object):
    operation: Operation
    argument: int

    @classmethod
    def FromLine(cls, line: str) -> Instruction:
        match = re.fullmatch(r"(?P<op>...) (?P<arg>[+-]\d+)", line.strip())
        if not match:
            raise ValueError(f"Could not parse line as instruction: {line}")
        op = Operation[match.group("op").upper()]
        arg = int(match.group("arg"))
        return cls(
            operation=op,
            argument=arg,
        )


def Step(memory: List[Instruction], state: State) -> State:
    if state.next_instruction == len(memory):
        return State(
            next_instruction=state.next_instruction,
            accumulator=state.accumulator,
            halted=True,
        )
    next_instruction = memory[state.next_instruction]
    if next_instruction.operation == Operation.ACC:
        return State(
            accumulator=state.accumulator + next_instruction.argument,
            next_instruction=state.next_instruction + 1,
            halted=False,
        )
    elif next_instruction.operation == Operation.NOP:
        return State(
            accumulator=state.accumulator,
            next_instruction=state.next_instruction + 1,
            halted=False,
        )
    elif next_instruction.operation == Operation.JMP:
        return State(
            accumulator=state.accumulator,
            next_instruction=state.next_instruction
            + next_instruction.argument,
            halted=False,
        )
    else:
        raise RuntimeError(f"Invalid instruction: {next_instruction}")
