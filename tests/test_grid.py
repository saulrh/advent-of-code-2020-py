import unittest

from advent_of_code_2020_py import grid
from advent_of_code_2020_py import linalg


class TestGrid(unittest.TestCase):
    def test_Parsing(self):
        g = grid.Grid.FromString(".#\n#.")
        self.assertEqual(g.Get(linalg.Point(row=0, col=0)), grid.Tile.SNOW)
        self.assertEqual(g.Get(linalg.Point(row=0, col=1)), grid.Tile.TREE)
        self.assertEqual(g.Get(linalg.Point(row=1, col=0)), grid.Tile.TREE)
        self.assertEqual(g.Get(linalg.Point(row=1, col=1)), grid.Tile.SNOW)

    def test_OutOfBounds(self):
        g = grid.Grid.FromString(".#\n#.")
        with self.assertRaisesRegex(ValueError, "ROW.*out of bounds.*LOW"):
            g.Get(linalg.Point(row=-1, col=0))
        with self.assertRaisesRegex(ValueError, "ROW.*out of bounds.*HIGH"):
            g.Get(linalg.Point(row=10, col=0))
        with self.assertRaisesRegex(ValueError, "COL.*out of bounds.*LOW"):
            g.Get(linalg.Point(row=0, col=-1))
        with self.assertRaisesRegex(ValueError, "COL.*out of bounds.*HIGH"):
            g.Get(linalg.Point(row=0, col=10))

    def test_Wrapping(self):
        g1 = grid.Grid.FromString(
            ".#.\n##.",
            {
                grid.Side.LEFT.AD(): grid.BoundaryBehavior.WRAP,
            },
        )
        self.assertEqual(g1.Get(linalg.Point(row=0, col=-1)), grid.Tile.SNOW)
        self.assertEqual(g1.Get(linalg.Point(row=0, col=-2)), grid.Tile.TREE)
        self.assertEqual(g1.Get(linalg.Point(row=0, col=-3)), grid.Tile.SNOW)
        with self.assertRaises(ValueError):
            g1.Get(linalg.Point(row=-1, col=0))
        with self.assertRaises(ValueError):
            g1.Get(linalg.Point(row=5, col=0))
        with self.assertRaises(ValueError):
            g1.Get(linalg.Point(row=0, col=5))

        g2 = grid.Grid.FromString(
            ".#.\n##.",
            {
                grid.Side.RIGHT.AD(): grid.BoundaryBehavior.WRAP,
            },
        )
        self.assertEqual(g2.Get(linalg.Point(row=0, col=4)), grid.Tile.TREE)
        self.assertEqual(g2.Get(linalg.Point(row=0, col=5)), grid.Tile.SNOW)
        self.assertEqual(g2.Get(linalg.Point(row=0, col=6)), grid.Tile.SNOW)
        with self.assertRaises(ValueError):
            g2.Get(linalg.Point(row=-1, col=0))
        with self.assertRaises(ValueError):
            g2.Get(linalg.Point(row=5, col=0))
        with self.assertRaises(ValueError):
            g2.Get(linalg.Point(row=0, col=-5))

        g3 = grid.Grid.FromString(
            ".#.\n#..",
            {
                grid.Side.UP.AD(): grid.BoundaryBehavior.WRAP,
            },
        )
        self.assertEqual(g3.Get(linalg.Point(row=-1, col=1)), grid.Tile.SNOW)
        self.assertEqual(g3.Get(linalg.Point(row=-2, col=1)), grid.Tile.TREE)
        self.assertEqual(g3.Get(linalg.Point(row=-3, col=1)), grid.Tile.SNOW)
        with self.assertRaises(ValueError):
            g3.Get(linalg.Point(row=5, col=0))
        with self.assertRaises(ValueError):
            g3.Get(linalg.Point(row=0, col=5))
        with self.assertRaises(ValueError):
            g3.Get(linalg.Point(row=0, col=-5))

        g4 = grid.Grid.FromString(
            ".#.\n#..",
            {
                grid.Side.DOWN.AD(): grid.BoundaryBehavior.WRAP,
            },
        )
        self.assertEqual(g4.Get(linalg.Point(row=4, col=1)), grid.Tile.TREE)
        self.assertEqual(g4.Get(linalg.Point(row=5, col=1)), grid.Tile.SNOW)
        self.assertEqual(g4.Get(linalg.Point(row=6, col=1)), grid.Tile.TREE)
        with self.assertRaises(ValueError):
            g4.Get(linalg.Point(row=-5, col=0))
        with self.assertRaises(ValueError):
            g4.Get(linalg.Point(row=0, col=5))
        with self.assertRaises(ValueError):
            g4.Get(linalg.Point(row=0, col=-5))


if __name__ == "__main__":
    unittest.main()
