import unittest

from advent_of_code_2020_py import problem01

EXAMPLE_DATA = [1721, 979, 366, 299, 675, 1456]


class Test01(unittest.TestCase):
    def test_example(self):
        pair = problem01.get_point(EXAMPLE_DATA, 2020, 2)
        self.assertCountEqual(pair, [1721, 299])
        self.assertEqual(problem01.get_result(pair), 514579)

    def test_example2(self):
        pair = problem01.get_point(EXAMPLE_DATA, 2020, 3)
        self.assertCountEqual(pair, [979, 366, 675])
        self.assertEqual(problem01.get_result(pair), 241861950)


if __name__ == "__main__":
    unittest.main()
