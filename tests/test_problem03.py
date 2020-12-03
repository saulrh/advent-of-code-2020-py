import unittest

from advent_of_code_2020_py import grid
from advent_of_code_2020_py import linalg
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
        self.assertEqual(
            problem03.CountTrees(
                grid.Grid.FromString(
                    DATA,
                    problem03.WRAP_RIGHT,
                ),
                linalg.Slope(over=3, down=1),
            ),
            7,
        )


if __name__ == "__main__":
    unittest.main()
