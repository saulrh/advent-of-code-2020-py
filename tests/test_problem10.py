import collections
import unittest

from advent_of_code_2020_py import problem10

DATA_1 = """16
10
15
5
1
11
7
19
6
12
4"""

DATA_2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
"""


class Test01(unittest.TestCase):
    def test_Preprocess(self):
        adapters = problem10.PreprocessAdapters(
            int(d) for d in DATA_1.splitlines()
        )
        self.assertEqual(min(adapters), 0)
        self.assertEqual(max(adapters), 22)

    def test_Example1(self):
        adapters = problem10.PreprocessAdapters(
            int(d) for d in DATA_1.splitlines()
        )
        differences = problem10.Differences(adapters)
        counts = collections.Counter(differences)
        self.assertEqual(counts, {1: 7, 3: 5})

    def test_Example2(self):
        adapters = problem10.PreprocessAdapters(
            int(d) for d in DATA_2.splitlines()
        )
        differences = problem10.Differences(adapters)
        counts = collections.Counter(differences)
        self.assertEqual(counts, {1: 22, 3: 10})

    def test_BuildGraph(self):
        adapters = problem10.PreprocessAdapters(
            int(d) for d in DATA_1.splitlines()
        )
        graph = problem10.BuildGraph(adapters)
        self.assertCountEqual(graph.successors(0), [1])
        self.assertCountEqual(graph.successors(1), [4])
        self.assertCountEqual(graph.successors(4), [5, 6, 7])

    def test_Example3(self):
        adapters = problem10.PreprocessAdapters(
            int(d) for d in DATA_1.splitlines()
        )
        graph = problem10.BuildGraph(adapters)
        self.assertEqual(problem10.CountPaths(graph, 0, max(graph.nodes)), 8)

    def test_Example4(self):
        adapters = problem10.PreprocessAdapters(
            int(d) for d in DATA_2.splitlines()
        )
        graph = problem10.BuildGraph(adapters)
        self.assertEqual(
            problem10.CountPaths(graph, 0, max(graph.nodes)), 19208
        )


if __name__ == "__main__":
    unittest.main()
