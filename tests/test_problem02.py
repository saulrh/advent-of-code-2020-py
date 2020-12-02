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
        self.assertEqual(data[0], problem02.Entry(
            n1=1,
            n2=3,
            letter="a",
            password="abcde",
        ))
        self.assertEqual(data[1], problem02.Entry(
            n1=1,
            n2=3,
            letter="b",
            password="cdefg",
        ))
        self.assertEqual(data[2], problem02.Entry(
            n1=2,
            n2=9,
            letter="c",
            password="ccccccccc",
        ))

    def test_example_part1(self):
        data = [problem02.Entry.FromLine(e) for e in EXAMPLE_DATA]
        validation = [d.Part1Valid() for d in data]
        self.assertEqual(validation, [True, False, True])

    def test_example_part2(self):
        data = [problem02.Entry.FromLine(e) for e in EXAMPLE_DATA]
        validation = [d.Part2Valid() for d in data]
        self.assertEqual(validation, [True, False, False])


if __name__ == "__main__":
    unittest.main()
