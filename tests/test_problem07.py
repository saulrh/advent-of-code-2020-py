import unittest

from advent_of_code_2020_py import problem07

DATA_1 = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

DATA_2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""


class Test01(unittest.TestCase):
    def test_SingleLine(self):
        self.assertEqual(
            problem07.LineTransform("black bags contain 1 white bag."),
            ("black", {"white": 1}),
        )

    def test_Part1(self):
        directs = dict(problem07.LineTransform(d) for d in DATA_1.splitlines())
        contents = problem07.MakeContents(directs)
        self.assertEqual(
            sum(
                "shiny gold" in contents(outermost)
                for outermost in directs.keys()
            ),
            4,
        )

    def test_Part2Example1(self):
        directs = dict(problem07.LineTransform(d) for d in DATA_1.splitlines())
        contents = problem07.MakeContents(directs)
        self.assertEqual(sum(contents("shiny gold").values()), 32)

    def test_Part2Example2(self):
        directs = dict(problem07.LineTransform(d) for d in DATA_2.splitlines())
        contents = problem07.MakeContents(directs)
        self.assertEqual(sum(contents("shiny gold").values()), 126)


if __name__ == "__main__":
    unittest.main()
