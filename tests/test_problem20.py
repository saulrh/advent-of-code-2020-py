import functools
import itertools
import operator
import unittest

from rich import table

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem20

EXAMPLE_1 = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""


class Test20(unittest.TestCase):
    def assertEdgesEqual(self, a, b):
        self.assertEqual(problem20.EdgeHash(a), problem20.EdgeHash(b))

    def test_Parse(self):
        tiles = {t.tile_id: t for t in problem20.FromStr(EXAMPLE_1)}
        self.assertEqual(len(tiles), 9)
        self.assertCountEqual(
            tiles.keys(),
            [2311, 1951, 1171, 1427, 1489, 2473, 2971, 2729, 3079],
        )

    def test_ToStr(self):
        tiles = {t.tile_id: t for t in problem20.FromStr(EXAMPLE_1)}
        t = tiles[3079]
        self.assertEqual(str(t).strip(), EXAMPLE_1[-110:].strip())

    def test_GetItem(self):
        tiles = {t.tile_id: t for t in problem20.FromStr(EXAMPLE_1)}
        t = tiles[3079]
        self.assertTrue(t[0, 0, problem20.Orientation.UP])
        self.assertFalse(t[0, 1, problem20.Orientation.UP])
        self.assertTrue(t[0, 2, problem20.Orientation.UP])
        self.assertFalse(t[1, 0, problem20.Orientation.UP])
        self.assertFalse(t[2, 0, problem20.Orientation.UP])
        self.assertTrue(t[3, 0, problem20.Orientation.UP])

        self.assertFalse(t[0, 0, problem20.Orientation.RIGHT])
        self.assertFalse(t[0, 0, problem20.Orientation.DOWN])
        self.assertFalse(t[0, 0, problem20.Orientation.LEFT])

        self.assertTrue(t[1, 1, problem20.Orientation.UP])
        self.assertFalse(t[1, 1, problem20.Orientation.RIGHT])
        self.assertFalse(t[1, 1, problem20.Orientation.DOWN])
        self.assertTrue(t[1, 1, problem20.Orientation.LEFT])

        self.assertFalse(t[0, 0, problem20.Orientation.FLIP_UP])
        self.assertFalse(t[0, 0, problem20.Orientation.FLIP_RIGHT])
        self.assertFalse(t[0, 0, problem20.Orientation.FLIP_DOWN])
        self.assertTrue(t[0, 0, problem20.Orientation.FLIP_LEFT])

        self.assertTrue(t[1, 2, problem20.Orientation.FLIP_UP])
        self.assertFalse(t[1, 2, problem20.Orientation.FLIP_RIGHT])
        self.assertTrue(t[1, 2, problem20.Orientation.FLIP_DOWN])
        self.assertFalse(t[1, 2, problem20.Orientation.FLIP_LEFT])

    def test_RotationsContiguous(self):
        tiles = {t.tile_id: t for t in problem20.FromStr(EXAMPLE_1)}
        for t, o in itertools.product(tiles.values(), problem20.Orientation):
            self.assertEqual(
                t.Edge(o, problem20.Side.UP)[-1],
                t.Edge(o, problem20.Side.RIGHT)[0],
            )
            self.assertEqual(
                t.Edge(o, problem20.Side.RIGHT)[-1],
                t.Edge(o, problem20.Side.DOWN)[-1],
            )
            self.assertEqual(
                t.Edge(o, problem20.Side.DOWN)[0],
                t.Edge(o, problem20.Side.LEFT)[-1],
            )
            self.assertEqual(
                t.Edge(o, problem20.Side.LEFT)[0],
                t.Edge(o, problem20.Side.UP)[0],
            )

    def test_RotationsInExampleAlign(self):
        tiles = {t.tile_id: t for t in problem20.FromStr(EXAMPLE_1)}

        solution = {
            (0, 0): (tiles[1951], problem20.Orientation.FLIP_DOWN),
            (0, 1): (tiles[2311], problem20.Orientation.FLIP_DOWN),
            (0, 2): (tiles[3079], problem20.Orientation.UP),
            (1, 0): (tiles[2729], problem20.Orientation.FLIP_DOWN),
            (1, 1): (tiles[1427], problem20.Orientation.FLIP_DOWN),
            (1, 2): (tiles[2473], problem20.Orientation.FLIP_RIGHT),
            (2, 0): (tiles[2971], problem20.Orientation.FLIP_DOWN),
            (2, 1): (tiles[1489], problem20.Orientation.FLIP_DOWN),
            (2, 2): (tiles[1171], problem20.Orientation.FLIP_UP),
        }

        def EdgeFor(row, col, side):
            tile, tile_orientation = solution[row, col]
            return tile.Edge(tile_orientation, side)

        for row1, row2 in [[0, 1], [1, 2]]:
            for col1, col2 in [[0, 1], [1, 2]]:
                self.assertEdgesEqual(
                    EdgeFor(row1, col1, problem20.Side.RIGHT),
                    EdgeFor(row1, col2, problem20.Side.LEFT),
                )
                self.assertEdgesEqual(
                    EdgeFor(row1, col1, problem20.Side.DOWN),
                    EdgeFor(row2, col1, problem20.Side.UP),
                )
                self.assertEdgesEqual(
                    EdgeFor(row2, col1, problem20.Side.RIGHT),
                    EdgeFor(row2, col2, problem20.Side.LEFT),
                )
                self.assertEdgesEqual(
                    EdgeFor(row1, col2, problem20.Side.DOWN),
                    EdgeFor(row2, col2, problem20.Side.UP),
                )

    def test_Example1(self):
        tiles = {t.tile_id: t for t in problem20.FromStr(EXAMPLE_1)}

        solution = problem20.Solve(tiles)

        t = table.Table(show_lines=True, show_header=False)
        for r in range(3):
            t.add_row(*[str(solution[r, c][0]) for c in range(3)])
        debug.console.log(t)

        self.assertEqual(
            len(list(v[0] for v in solution.values())),
            len(set(v[0] for v in solution.values())),
        )

        debug.console.log(solution)
        debug.console.log(problem20.StitchSolution(tiles, solution))
        self.assertEqual(
            functools.reduce(
                operator.mul,
                (solution[c][0] for c in [(0, 0), (0, 2), (2, 0), (2, 2)]),
            ),
            20899048083289,
        )
