import unittest

from advent_of_code_2020_py import linalg
from advent_of_code_2020_py import problem12

EXAMPLE_1 = """F10
N3
F7
R90
F11
"""


class Test01(unittest.TestCase):
    def test_Part1(self):
        state = problem12.Ship()
        state = state.ApplyInputs(EXAMPLE_1.splitlines())
        self.assertEqual(
            state,
            problem12.Ship(
                position=linalg.Point(row=8, col=17),
                direction=problem12.Direction.SOUTH,
            ),
        )
        self.assertEqual(abs(state.position.row) + abs(state.position.col), 25)

    def test_Part2(self):
        state = problem12.WaypointShip()
        state = state.ApplyInputs(EXAMPLE_1.splitlines())
        self.assertEqual(
            state,
            problem12.WaypointShip(
                position=linalg.Point(row=72, col=214),
                waypoint=linalg.Point(row=10, col=4),
            ),
        )
        self.assertEqual(
            abs(state.position.row) + abs(state.position.col), 286
        )
