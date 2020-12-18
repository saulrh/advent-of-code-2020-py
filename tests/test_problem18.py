import unittest

from advent_of_code_2020_py import problem18


class Test01(unittest.TestCase):
    def test_Example1(self):
        self.assertEqual(problem18.Compute("1 + 2 * 3 + 4 * 5 + 6"), 71)

    def test_Example2(self):
        self.assertEqual(problem18.Compute("2 * 3 + (4 * 5)"), 26)

    def test_Example3(self):
        self.assertEqual(problem18.Compute("5 + (8 * 3 + 9 + 3 * 4 * 3)"), 437)

    def test_Example4(self):
        self.assertEqual(
            problem18.Compute("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"),
            12240,
        )

    def test_Example5(self):
        self.assertEqual(
            problem18.Compute(
                "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
            ),
            13632,
        )
