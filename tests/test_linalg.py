import unittest

from advent_of_code_2020_py import linalg


class TestPoint(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(
            linalg.Point(1, 2) + linalg.Point(3, 4), linalg.Point(4, 6)
        )

    def test_subtraction(self):
        self.assertEqual(
            linalg.Point(1, 2) - linalg.Point(3, 4), linalg.Point(-2, -2)
        )
        self.assertEqual(
            linalg.Point(5, 10) - linalg.Point(3, 2), linalg.Point(2, 8)
        )

    def test_multiplication(self):
        self.assertEqual(linalg.Point(1, 2) * 2, linalg.Point(2, 4))
        self.assertEqual(linalg.Point(1, 2) * -2, linalg.Point(-2, -4))

    def test_Rotate(self):
        self.assertEqual(
            linalg.Point(1, 2).RotateClockwise(90), linalg.Point(2, -1)
        )
        self.assertEqual(
            linalg.Point(1, 2).RotateClockwise(-90), linalg.Point(-2, 1)
        )


class TestSlope(unittest.TestCase):
    def test_CanAddToPoint(self):
        self.assertEqual(
            linalg.Point(row=1, col=2) + linalg.Slope(over=10, down=30),
            linalg.Point(row=31, col=12),
        )


if __name__ == "__main__":
    unittest.main()
