import unittest

from advent_of_code_2020_py import problem
from advent_of_code_2020_py import problem06

DATA = """abc

a
b
c

ab
ac

a
a
a
a

b
"""


class Test06(unittest.TestCase):
    def test_example1(self):
        groups = problem.InBatches(
            lines=DATA.splitlines(),
            line_transform=set,
            batch_transform=problem06.Part1Batch,
        )
        self.assertEqual(sum(len(g) for g in groups), 11)

    def test_example2(self):
        groups = problem.InBatches(
            lines=DATA.splitlines(),
            line_transform=set,
            batch_transform=problem06.Part2Batch,
        )
        self.assertEqual(sum(len(g) for g in groups), 6)


if __name__ == "__main__":
    unittest.main()
