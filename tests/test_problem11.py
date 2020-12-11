import unittest

from advent_of_code_2020_py import problem11

EXAMPLE_1 = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

EXAMPLE_1_STEP_2 = """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
"""

EXAMPLE_1_STEP_3 = """#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
"""

EXAMPLE_1_STEP_4 = """#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
"""

EXAMPLE_1_STEP_5 = """#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
"""

EXAMPLE_1_CONVERGED = """#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
"""

EXAMPLE_2_STEP_2 = """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
"""

EXAMPLE_2_STEP_3 = """#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
"""

EXAMPLE_2_STEP_4 = """#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
"""

EXAMPLE_2_STEP_5 = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
"""

EXAMPLE_2_STEP_6 = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
"""

EXAMPLE_2_CONVERGED = """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
"""


def Comparable(g) -> str:
    if type(g) == str:
        return g.strip()
    else:
        return str(g).strip()


class Test01(unittest.TestCase):
    def assertGridsEqual(self, a, b):
        self.assertEqual(Comparable(a), Comparable(b))

    def test_ParseAndPrettyPrint(self):
        grid = problem11.ParseInput(EXAMPLE_1)
        self.assertGridsEqual(grid, EXAMPLE_1)

    def test_Small(self):
        grid = problem11.ParseInput("LLL#")
        grid2 = grid.Step()
        self.assertGridsEqual(grid2, "##L#")

    def test_Step(self):
        grid = problem11.ParseInput(EXAMPLE_1)
        grid2 = grid.Step()
        self.assertGridsEqual(grid2, EXAMPLE_1_STEP_2)
        grid3 = grid2.Step()
        self.assertGridsEqual(grid3, EXAMPLE_1_STEP_3)
        grid4 = grid3.Step()
        self.assertGridsEqual(grid4, EXAMPLE_1_STEP_4)
        grid5 = grid4.Step()
        self.assertGridsEqual(grid5, EXAMPLE_1_STEP_5)
        converged = grid5.Step()
        self.assertGridsEqual(converged, converged.Step())
        self.assertGridsEqual(converged, EXAMPLE_1_CONVERGED)

    def test_Convergence(self):
        grid = problem11.ParseInput(EXAMPLE_1)
        converged = grid.RunToConvergence()
        self.assertGridsEqual(converged, EXAMPLE_1_CONVERGED)
        self.assertEqual(
            sum(cell == "#" for cell in converged.data.values()), 37
        )

    def test_Part2(self):
        grid = problem11.ParseInput(EXAMPLE_1)
        grid2 = grid.Step(
            get_neighbors=problem11.AllVisible, leave_threshold=5
        )
        self.assertGridsEqual(grid2, EXAMPLE_2_STEP_2)
        grid3 = grid2.Step(
            get_neighbors=problem11.AllVisible, leave_threshold=5
        )
        self.assertGridsEqual(grid3, EXAMPLE_2_STEP_3)
        grid4 = grid3.Step(
            get_neighbors=problem11.AllVisible, leave_threshold=5
        )
        self.assertGridsEqual(grid4, EXAMPLE_2_STEP_4)
        grid5 = grid4.Step(
            get_neighbors=problem11.AllVisible, leave_threshold=5
        )
        self.assertGridsEqual(grid5, EXAMPLE_2_STEP_5)
        grid6 = grid5.Step(
            get_neighbors=problem11.AllVisible, leave_threshold=5
        )
        self.assertGridsEqual(grid6, EXAMPLE_2_STEP_6)
        converged = grid6.Step(
            get_neighbors=problem11.AllVisible, leave_threshold=5
        )
        self.assertGridsEqual(
            converged,
            converged.Step(
                get_neighbors=problem11.AllVisible, leave_threshold=5
            ),
        )
        self.assertGridsEqual(converged, EXAMPLE_2_CONVERGED)


if __name__ == "__main__":
    unittest.main()
