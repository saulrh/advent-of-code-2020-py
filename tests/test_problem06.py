import unittest

from advent_of_code_2020_py import problem06

data = """abc

a
b
c

ab
ac

a
a
a
a

b
"""


class Test01(unittest.TestCase):
    def test_example1(self):
        self.assertEqual(
            sum(len(s) for s in problem06.ParseFilePart1(data.splitlines())),
            11,
        )

    def test_example2(self):
        self.assertEqual(
            sum(len(s) for s in problem06.ParseFilePart2(data.splitlines())), 6
        )


if __name__ == "__main__":
    unittest.main()
