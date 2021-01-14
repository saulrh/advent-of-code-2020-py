import unittest

from advent_of_code_2020_py import problem22

EXAMPLE_1 = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


TERMINATING = """player 1:
43
19

Player 2:
2
29
14
"""


class Test22(unittest.TestCase):
    def test_Example1(self):
        state = problem22.State.FromStr(EXAMPLE_1)
        state.Run(False)
        self.assertEqual(state.value_winner, 306)

    def test_Example2(self):
        state = problem22.State.FromStr(EXAMPLE_1)
        state.Run(True)
        self.assertEqual(state.value_winner, 291)

    def test_NotInfinite(self):
        state = problem22.State.FromStr(TERMINATING)
        state.Run(True)
