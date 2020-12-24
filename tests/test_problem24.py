import unittest

from advent_of_code_2020_py import problem24

EXAMPLE_1 = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""


class Test20(unittest.TestCase):
    def test_Example1(self):
        flips = (problem24.Movement(line) for line in EXAMPLE_1.splitlines())
        tiles = problem24.InitialTiles(flips)
        self.assertEqual(len(tiles), 10)

    def test_Example2(self):
        flips = (problem24.Movement(line) for line in EXAMPLE_1.splitlines())
        tiles = problem24.InitialTiles(flips)
        counts = {}
        for i in range(10):
            tiles = problem24.Step(tiles)
            counts[i + 1] = len(tiles)
        self.assertEqual(
            counts,
            {
                1: 15,
                2: 12,
                3: 25,
                4: 14,
                5: 23,
                6: 28,
                7: 41,
                8: 37,
                9: 49,
                10: 37,
            },
        )
