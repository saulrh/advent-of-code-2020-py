import unittest

from advent_of_code_2020_py import problem14

DATA_1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""


DATA_2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""


class Test01(unittest.TestCase):
    def test_LineRegex(self):
        self.assertEqual(
            problem14.ParseLine("mask = XXXX10001"),
            problem14.Instruction("mask", value="XXXX10001"),
        )
        self.assertEqual(
            problem14.ParseLine("mem[8] = 10"),
            problem14.Instruction("mem", addr=8, value="10"),
        )

    def test_Example1(self):
        state = problem14.State()
        state.Interpret1Program(DATA_1.splitlines())
        self.assertEqual(sum(state.memory.values()), 165)

    def test_Example2(self):
        state = problem14.State()
        state.Interpret2Program(DATA_2.splitlines())
        self.assertEqual(sum(state.memory.values()), 208)
