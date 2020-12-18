import unittest

from advent_of_code_2020_py import problem18


class Test01(unittest.TestCase):
    def test_Part1Example1(self):
        self.assertEqual(problem18.Compute1("1 + 2 * 3 + 4 * 5 + 6"), 71)

    def test_Part1Example2(self):
        self.assertEqual(problem18.Compute1("1 + (2 * 3) + (4 * (5 + 6))"), 51)

    def test_Part1Example3(self):
        self.assertEqual(problem18.Compute1("2 * 3 + (4 * 5)"), 26)

    def test_Part1Example4(self):
        self.assertEqual(
            problem18.Compute1("5 + (8 * 3 + 9 + 3 * 4 * 3)"), 437
        )

    def test_Part1Example5(self):
        self.assertEqual(
            problem18.Compute1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"),
            12240,
        )

    def test_Part1Example6(self):
        self.assertEqual(
            problem18.Compute1(
                "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
            ),
            13632,
        )

    def test_Part2Example1(self):
        self.assertEqual(problem18.Compute2("1 + 2 * 3 + 4 * 5 + 6"), 231)

    def test_Part2Example2(self):
        self.assertEqual(problem18.Compute1("1 + (2 * 3) + (4 * (5 + 6))"), 51)

    def test_Part2Example3(self):
        self.assertEqual(problem18.Compute2("2 * 3 + (4 * 5)"), 46)

    def test_Part2Example4(self):
        self.assertEqual(
            problem18.Compute2("5 + (8 * 3 + 9 + 3 * 4 * 3)"), 1445
        )

    def test_Part2Example5(self):
        self.assertEqual(
            problem18.Compute2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"),
            669060,
        )

    def test_Part2Example6(self):
        self.assertEqual(
            problem18.Compute2(
                "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
            ),
            23340,
        )
