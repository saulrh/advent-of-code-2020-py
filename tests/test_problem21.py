import functools
import operator
import unittest

from advent_of_code_2020_py import problem21

EXAMPLE_1 = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""


class Test21(unittest.TestCase):
    def test_Example1(self):
        foods = [
            problem21.Food.FromStr(line) for line in EXAMPLE_1.splitlines()
        ]
        possible_ingredients = problem21.PossibleIngredientsForAllergens(foods)
        appearing = functools.reduce(
            operator.or_, possible_ingredients.values()
        )
        all_ingredients = functools.reduce(
            operator.or_, (f.ingredients for f in foods)
        )
        no_allergens = all_ingredients - appearing
        self.assertEqual(no_allergens, {"kfcds", "nhms", "sbzzf", "trh"})
        self.assertEqual(
            sum(len(no_allergens & f.ingredients) for f in foods), 5
        )

    def test_Example2(self):
        foods = [
            problem21.Food.FromStr(line) for line in EXAMPLE_1.splitlines()
        ]
        solution = problem21.Solve(foods)
        self.assertEqual(
            problem21.Canonicalize(solution), "mxmxvkd,sqjhc,fvjkl"
        )
