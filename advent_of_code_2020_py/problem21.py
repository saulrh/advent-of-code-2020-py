#!/usr/bin/env python

from __future__ import annotations

import functools
import itertools
import operator
from typing import Dict, Iterable, Set

import attr
import regex

from advent_of_code_2020_py import debug
from advent_of_code_2020_py import problem

_FOOD_RE = regex.compile(
    r"((?P<ing>[a-z]+) )+\(contains ((?P<all>[a-z]+)(, )?)+\)"
)


@attr.s(auto_attribs=True)
class Food(object):
    ingredients: Set[str]
    allergens: Set[str]

    @classmethod
    def FromStr(cls, line: str) -> Food:
        match = _FOOD_RE.match(line.strip())
        if not match:
            raise ValueError(f'Failed to match "{line}"')
        return cls(
            ingredients=set(match.captures("ing")),
            allergens=set(match.captures("all")),
        )


def SafeIngredients(
    foods: Iterable[Food], possibilities: Dict[str, Set[str]]
) -> Set[str]:
    appearing = functools.reduce(operator.or_, possibilities.values())
    all_ingredients = functools.reduce(
        operator.or_, (f.ingredients for f in foods)
    )
    return all_ingredients - appearing


def PossibleIngredientsForAllergens(
    foods: Iterable[Food],
) -> Dict[str, Set[str]]:
    possible_ingredients = {}
    allergens = set(itertools.chain.from_iterable(f.allergens for f in foods))
    for allergen in allergens:
        ingredient_sets = [
            f.ingredients for f in foods if allergen in f.allergens
        ]
        if not ingredient_sets:
            raise RuntimeError(f"Could not find {allergen} in any foods")
        possible_ingredients[allergen] = functools.reduce(
            operator.and_, ingredient_sets
        )
    return possible_ingredients


def Solve(foods: Iterable[Food]) -> Dict[str, str]:
    possibilities = PossibleIngredientsForAllergens(foods)
    solution = {}

    while len(possibilities) > 0:
        for allergen, possibles in possibilities.items():
            if len(possibles) == 1:
                soln = next(iter(possibles))
                solution[allergen] = soln
                for poss in possibilities.values():
                    poss.discard(soln)
        for allergen in set(possibilities.keys()) & set(solution.keys()):
            del possibilities[allergen]

    return solution


def Canonicalize(solution: Dict[str, str]) -> str:
    pairs = sorted(solution.items(), key=lambda pair: pair[0])
    return ",".join(ing for _, ing in pairs)


def part1():
    debug.console.rule("[bold red]Part 1")
    foods = list(problem.Get(21, Food.FromStr))
    possibilities = PossibleIngredientsForAllergens(foods)
    safe = SafeIngredients(foods, possibilities)
    debug.console.log(sum(len(safe & f.ingredients) for f in foods))


def part2():
    debug.console.rule("[bold red]Part 2")
    foods = list(problem.Get(21, Food.FromStr))
    debug.console.log(Canonicalize(Solve(foods)))


if __name__ == "__main__":
    part1()
    part2()
