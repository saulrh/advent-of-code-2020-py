import unittest

from advent_of_code_2020_py import problem05


class Test05(unittest.TestCase):
    def test_example1(self):
        self.assertEqual(problem05.SeatID("FBFBBFFRLR"), 357)

    def test_example2(self):
        self.assertEqual(problem05.SeatID("BFFFBBFRRR"), 567)

    def test_example3(self):
        self.assertEqual(problem05.SeatID("FFFBBBFRRR"), 119)

    def test_example4(self):
        self.assertEqual(problem05.SeatID("BBFFBBFRLL"), 820)


if __name__ == "__main__":
    unittest.main()
