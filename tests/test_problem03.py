import unittest

from advent_of_code_2020_py import problem03

DATA = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""


class Test01(unittest.TestCase):
    def test_example1(self):
        hill = problem03.Map.FromString(DATA)
        self.assertEqual(
            problem03.CountTrees(hill, problem03.Slope(over=3, down=1)), 7
        )


if __name__ == "__main__":
    unittest.main()
