import unittest

from advent_of_code_2020_py import temp


class Test01(unittest.TestCase):
    def test_Positions(self):
        self.assertEqual(tuple(temp.Positions(9)), (0, 3, 1, 6, 4, 2, 7, 5, 8))
