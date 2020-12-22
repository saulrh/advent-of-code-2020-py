import functools
import itertools
import operator
import unittest

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

STITCHED = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###
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
        self.assertTrue(t.Oriented(problem20.Orientation.UP).data[0, 0])
        self.assertFalse(t.Oriented(problem20.Orientation.UP).data[0, 1])
        self.assertTrue(t.Oriented(problem20.Orientation.UP).data[0, 2])
        self.assertFalse(t.Oriented(problem20.Orientation.UP).data[1, 0])
        self.assertFalse(t.Oriented(problem20.Orientation.UP).data[2, 0])
        self.assertTrue(t.Oriented(problem20.Orientation.UP).data[3, 0])

        self.assertFalse(t.Oriented(problem20.Orientation.RIGHT).data[0, 0])
        self.assertFalse(t.Oriented(problem20.Orientation.DOWN).data[0, 0])
        self.assertFalse(t.Oriented(problem20.Orientation.LEFT).data[0, 0])
        self.assertTrue(t.Oriented(problem20.Orientation.UP).data[1, 1])
        self.assertFalse(t.Oriented(problem20.Orientation.RIGHT).data[1, 1])
        self.assertFalse(t.Oriented(problem20.Orientation.DOWN).data[1, 1])
        self.assertTrue(t.Oriented(problem20.Orientation.LEFT).data[1, 1])
        self.assertFalse(t.Oriented(problem20.Orientation.FLIP_UP).data[0, 0])
        self.assertFalse(
            t.Oriented(problem20.Orientation.FLIP_RIGHT).data[0, 0]
        )
        self.assertFalse(
            t.Oriented(problem20.Orientation.FLIP_DOWN).data[0, 0]
        )
        self.assertTrue(t.Oriented(problem20.Orientation.FLIP_LEFT).data[0, 0])
        self.assertTrue(t.Oriented(problem20.Orientation.FLIP_UP).data[1, 2])
        self.assertFalse(
            t.Oriented(problem20.Orientation.FLIP_RIGHT).data[1, 2]
        )
        self.assertTrue(t.Oriented(problem20.Orientation.FLIP_DOWN).data[1, 2])
        self.assertFalse(
            t.Oriented(problem20.Orientation.FLIP_LEFT).data[1, 2]
        )

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

        self.assertEqual(
            len(list(v[0] for v in solution.values())),
            len(set(v[0] for v in solution.values())),
        )

        self.assertEqual(
            functools.reduce(
                operator.mul,
                (solution[c][0] for c in [(0, 0), (0, 2), (2, 0), (2, 2)]),
            ),
            20899048083289,
        )

    def test_Stitch(self):
        tiles = {t.tile_id: t for t in problem20.FromStr(EXAMPLE_1)}
        solution = problem20.Solve(tiles)
        stitched = problem20.Stitch(tiles, solution)
        renders = {
            str(stitched.Oriented(o)).strip() for o in problem20.Orientation
        }
        pretty_renders = "\n\n".join(renders)
        self.assertIn(
            STITCHED.strip(),
            renders,
            msg=f"Did not find:\n\n{STITCHED}\n\nIN\n\n{pretty_renders}",
        )

    def test_Example2(self):
        tiles = {t.tile_id: t for t in problem20.FromStr(EXAMPLE_1)}
        solution = problem20.Solve(tiles)
        stitched = problem20.Stitch(tiles, solution)
        serpent_count = problem20.SerpentCount(stitched)
        self.assertEqual(serpent_count, 2)
        self.assertEqual(problem20.Roughness(stitched), 273)
