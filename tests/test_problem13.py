import unittest

from advent_of_code_2020_py import problem13

DATA = """939
7,13,x,x,59,x,31,19"""


class Test01(unittest.TestCase):
    def test_Parse(self):
        t, buses = problem13.ParseInput(DATA)
        self.assertEqual(t, 939)
        self.assertCountEqual(
            buses,
            [
                problem13.Bus(idx=0, period=7),
                problem13.Bus(idx=1, period=13),
                problem13.Bus(idx=4, period=59),
                problem13.Bus(idx=6, period=31),
                problem13.Bus(idx=7, period=19),
            ],
        )

    def test_Part1(self):
        t, buses = problem13.ParseInput(DATA)
        self.assertEqual(
            problem13.NextDeparture(t, buses),
            (problem13.Bus(idx=4, period=59), 5),
        )

    def test_Part2_example1(self):
        _, buses = problem13.ParseInput("0\n17,x,13,19")
        self.assertEqual(problem13.SolvePart2(buses), 3417)

    def test_Part2_example2(self):
        _, buses = problem13.ParseInput("0\n67,7,59,61")
        self.assertEqual(problem13.SolvePart2(buses), 754018)

    def test_Part2_example3(self):
        _, buses = problem13.ParseInput("0\n67,x,7,59,61")
        self.assertEqual(problem13.SolvePart2(buses), 779210)

    def test_Part2_example4(self):
        _, buses = problem13.ParseInput("0\n67,7,x,59,61")
        self.assertEqual(problem13.SolvePart2(buses), 1261476)

    def test_Part2_example5(self):
        _, buses = problem13.ParseInput("0\n1789,37,47,1889")
        self.assertEqual(problem13.SolvePart2(buses), 1202161486)

    def test_Part2(self):
        _, buses = problem13.ParseInput(DATA)
        self.assertEqual(problem13.SolvePart2(buses), 1068781)
