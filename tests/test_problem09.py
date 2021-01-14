import unittest

from advent_of_code_2020_py import problem09

DATA_1 = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


class Test09(unittest.TestCase):
    def test_Example1(self):
        data = [int(d) for d in DATA_1.splitlines()]
        self.assertEqual(data[problem09.FindFirstInvalidIdx(data, 5)], 127)

    def test_Example2(self):
        data = [int(d) for d in DATA_1.splitlines()]
        lower, upper = problem09.FindRangeWithSum(data, 127)
        self.assertEqual((lower, upper), (2, 5))
        self.assertEqual(problem09.MinMaxSum(data[lower : upper + 1]), 62)


if __name__ == "__main__":
    unittest.main()
