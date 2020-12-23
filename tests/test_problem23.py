import unittest

from advent_of_code_2020_py import problem23

EXAMPLE_1 = [3, 8, 9, 1, 2, 5, 4, 6, 7]


class Test20(unittest.TestCase):
    def test_Example1(self):
        numbers = EXAMPLE_1
        numbers = problem23.Step(numbers)
        self.assertEqual(numbers, [2, 8, 9, 1, 5, 4, 6, 7, 3])
        for _ in range(9):
            numbers = problem23.Step(numbers)
        self.assertEqual(numbers, [8, 3, 7, 4, 1, 9, 2, 6, 5])
        self.assertEqual(problem23.Collect(numbers), "92658374")

    def test_Example2(self):
        numbers = EXAMPLE_1 + list(range(max(EXAMPLE_1) + 1, 1000000))
        for _ in range(10000000):
            numbers = problem23.Step(numbers)
        self.assertEqual(problem23.Stars(numbers), 149245887792)
