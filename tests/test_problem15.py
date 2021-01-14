import itertools
import unittest

from advent_of_code_2020_py import problem15

DATA_1 = """0,3,6"""


class Test15(unittest.TestCase):
    def test_Memory1(self):
        starting = problem15.Parse(DATA_1)
        self.assertEqual(
            list(itertools.islice(problem15.Memory(starting), 10)),
            [0, 3, 6, 0, 3, 3, 1, 0, 4, 0],
        )
        self.assertEqual(
            list(itertools.islice(problem15.Memory(starting), 2019, 2020)),
            [436],
        )

    def test_Memory2(self):
        starting = problem15.Parse("1,3,2")
        self.assertEqual(
            list(itertools.islice(problem15.Memory(starting), 2019, 2020)), [1]
        )
