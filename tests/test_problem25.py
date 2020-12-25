import unittest

from advent_of_code_2020_py import problem25

EXAMPLE_1_CARD = 5764801
EXAMPLE_1_DOOR = 17807724


class Test20(unittest.TestCase):
    def test_Example1Card(self):
        self.assertEqual(problem25.Reverse(EXAMPLE_1_CARD, 7), 8)

    def test_Example1Door(self):
        self.assertEqual(problem25.Reverse(EXAMPLE_1_DOOR, 7), 11)

    def test_Forward(self):
        self.assertEqual(
            problem25.Forward(8, EXAMPLE_1_DOOR),
            problem25.Forward(11, EXAMPLE_1_CARD),
        )
