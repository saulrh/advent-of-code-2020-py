import unittest

from advent_of_code_2020_py import problem17

DATA_1 = """.#.
..#
###
"""


class Test17(unittest.TestCase):
    def test_Parse(self):
        p = problem17.Parse(DATA_1, 3)
        self.assertEqual(
            p,
            {
                (0, 1, 0),
                (1, 2, 0),
                (2, 0, 0),
                (2, 1, 0),
                (2, 2, 0),
            },
        )

    def test_Example1(self):
        p = problem17.Parse(DATA_1, 3)
        for _ in range(0, 6):
            p = problem17.Step(p)
        self.assertEqual(len(p), 112)

    def test_Example2(self):
        p = problem17.Parse(DATA_1, 4)
        for _ in range(0, 6):
            p = problem17.Step(p)
        self.assertEqual(len(p), 848)


if __name__ == "__main__":
    unittest.main()
