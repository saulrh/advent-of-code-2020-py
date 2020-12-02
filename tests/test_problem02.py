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
        self.assertEqual(data[0].n1, 1)
        self.assertEqual(data[0].n2, 3)
        self.assertEqual(data[0].letter, "a")
        self.assertEqual(data[0].password, "abcde")
        self.assertEqual(data[1].n1, 1)
        self.assertEqual(data[1].n2, 3)
        self.assertEqual(data[1].letter, "b")
        self.assertEqual(data[1].password, "cdefg")
        self.assertEqual(data[2].n1, 2)
        self.assertEqual(data[2].n2, 9)
        self.assertEqual(data[2].letter, "c")
        self.assertEqual(data[2].password, "ccccccccc")

    def test_example_part1(self):
        data = [problem02.Entry.FromLine(e) for e in EXAMPLE_DATA]
        self.assertTrue(data[0].Part1Valid())
        self.assertFalse(data[1].Part1Valid())
        self.assertTrue(data[2].Part1Valid())

    def test_example_part2(self):
        data = [problem02.Entry.FromLine(e) for e in EXAMPLE_DATA]
        self.assertTrue(data[0].Part2Valid())
        self.assertFalse(data[1].Part2Valid())
        self.assertFalse(data[2].Part2Valid())


if __name__ == "__main__":
    unittest.main()
