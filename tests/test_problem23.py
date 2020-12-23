import itertools
import unittest

from advent_of_code_2020_py import problem23

EXAMPLE_1 = [3, 8, 9, 1, 2, 5, 4, 6, 7]


class Test20(unittest.TestCase):
    def test_List(self):
        state = problem23.Buffer.Build(range(10))
        self.assertEqual(
            list(s.car for s in state), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        )
        state.head.nxt.nxt.nxt.SetNxt(state.head)
        self.assertEqual(list(s.car for s in state), [0, 1, 2, 3])

    def test_Example1(self):
        state = problem23.Buffer.Build(EXAMPLE_1)
        state.Step()
        self.assertEqual(
            list(n.car for n in state), [2, 8, 9, 1, 5, 4, 6, 7, 3]
        )
        state.Step()
        self.assertEqual(
            list(n.car for n in state), [5, 4, 6, 7, 8, 9, 1, 3, 2]
        )
        for _ in range(8):
            state.Step()
        self.assertEqual(
            list(n.car for n in state), [8, 3, 7, 4, 1, 9, 2, 6, 5]
        )
        self.assertEqual(problem23.Collect(state), "92658374")

    def test_Example2(self):
        state = problem23.Buffer.Build(
            itertools.chain(EXAMPLE_1, range(max(EXAMPLE_1) + 1, 1000000 + 1))
        )
        self.assertEqual(state.largest, 1000000)
        self.assertEqual(len(state.nodes), 1000000)
        for _ in range(10000000):
            state.Step()
        self.assertEqual(problem23.Stars(state), 149245887792)
