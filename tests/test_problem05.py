import unittest

from advent_of_code_2020_py import linalg
from advent_of_code_2020_py import problem05


class Test01(unittest.TestCase):
    def test_example1(self):
        self.assertEqual(
            problem05.ToRowColumn("FBFBBFFRLR"), linalg.Point(row=44, col=5)
        )
        self.assertEqual(problem05.SeatID(linalg.Point(row=44, col=5)), 357)

    def test_example2(self):
        self.assertEqual(
            problem05.ToRowColumn("BFFFBBFRRR"), linalg.Point(row=70, col=7)
        )
        self.assertEqual(problem05.SeatID(linalg.Point(row=70, col=7)), 567)

    def test_example3(self):
        self.assertEqual(
            problem05.ToRowColumn("FFFBBBFRRR"), linalg.Point(row=14, col=7)
        )

    def test_example4(self):
        self.assertEqual(
            problem05.ToRowColumn("BBFFBBFRLL"), linalg.Point(row=102, col=4)
        )


if __name__ == "__main__":
    unittest.main()
