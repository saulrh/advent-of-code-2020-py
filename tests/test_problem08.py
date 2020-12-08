import unittest

from advent_of_code_2020_py import console
from advent_of_code_2020_py import problem08

DATA_1 = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


class Test01(unittest.TestCase):
    def test_Example1(self):
        memory = [console.Instruction.FromLine(s) for s in DATA_1.splitlines()]
        final_state = problem08.DetectLoop(memory)
        self.assertEqual(final_state.accumulator, 5)

    def test_Example2(self):
        memory = [console.Instruction.FromLine(s) for s in DATA_1.splitlines()]
        memory[0] = console.Instruction(
            operation=console.Operation.JMP, argument=memory[0].argument
        )
        final_state = problem08.DetectLoop(memory)
        self.assertEqual(final_state.accumulator, 0)
        self.assertFalse(final_state.halted)

    def test_Example3(self):
        memory = [console.Instruction.FromLine(s) for s in DATA_1.splitlines()]
        memory[7] = console.Instruction(
            operation=console.Operation.NOP, argument=memory[7].argument
        )
        final_state = problem08.DetectLoop(memory)
        self.assertEqual(final_state.accumulator, 8)
        self.assertTrue(final_state.halted)

    def test_Example4(self):
        memory = [console.Instruction.FromLine(s) for s in DATA_1.splitlines()]
        memory[2] = console.Instruction(
            operation=console.Operation.NOP, argument=memory[2].argument
        )
        final_state = problem08.DetectLoop(memory)
        self.assertFalse(final_state.halted)

    def test_Example5(self):
        memory = [console.Instruction.FromLine(s) for s in DATA_1.splitlines()]
        memory[4] = console.Instruction(
            operation=console.Operation.NOP, argument=memory[4].argument
        )
        final_state = problem08.DetectLoop(memory)
        self.assertFalse(final_state.halted)


if __name__ == "__main__":
    unittest.main()
