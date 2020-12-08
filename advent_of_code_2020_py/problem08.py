#!/usr/bin/env python

from __future__ import annotations

import copy

from advent_of_code_2020_py import console
from advent_of_code_2020_py import problem


def DetectLoop(memory) -> console.State:
    visited = set()
    state = console.State()
    visited.add(state.next_instruction)
    while True:
        next_state = console.Step(memory, state)
        if next_state.halted:
            return next_state
        elif next_state.next_instruction in visited:
            return state
        else:
            visited.add(next_state.next_instruction)
        state = next_state


def part1():
    memory = list(problem.Get(8, console.Instruction.FromLine))
    final_state = DetectLoop(memory)
    print(final_state.accumulator)


def part2():
    memory = list(problem.Get(8, console.Instruction.FromLine))
    for idx, instr in enumerate(memory):
        trial_memory = copy.deepcopy(memory)
        if instr.operation == console.Operation.NOP:
            trial_memory[idx] = console.Instruction(
                operation=console.Operation.JMP, argument=instr.argument
            )
        elif instr.operation == console.Operation.JMP:
            trial_memory[idx] = console.Instruction(
                operation=console.Operation.NOP, argument=instr.argument
            )
        final_state = DetectLoop(trial_memory)
        if final_state.halted:
            print(final_state)


if __name__ == "__main__":
    part1()
    part2()
