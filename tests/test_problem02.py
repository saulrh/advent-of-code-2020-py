import unittest

from advent_of_code_2020_py import problem02

EXAMPLE_DATA = [
    "1-3 a: abcde",
    "1-3 b: cdefg",
    "2-9 c: ccccccccc",
]


class Test02(unittest.TestCase):
    def test_parsing(self):
        data = [problem02.Entry.FromLine(e) for e in EXAMPLE_DATA]
        self.assertEqual(
            data,
            [
                problem02.Entry(
                    n1=1,
                    n2=3,
                    letter="a",
                    password="abcde",
                ),
                problem02.Entry(
                    n1=1,
                    n2=3,
                    letter="b",
                    password="cdefg",
                ),
                problem02.Entry(
                    n1=2,
                    n2=9,
                    letter="c",
                    password="ccccccccc",
                ),
            ],
        )

    def test_example_part1(self):
        self.assertEqual(
            [problem02.Entry.FromLine(e).Part1Valid() for e in EXAMPLE_DATA],
            [True, False, True],
        )

    def test_example_part2(self):
        self.assertEqual(
            [problem02.Entry.FromLine(e).Part2Valid() for e in EXAMPLE_DATA],
            [True, False, False],
        )


if __name__ == "__main__":
    unittest.main()
