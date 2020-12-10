#!/usr/bin/env python

from __future__ import annotations

import collections
import functools
import itertools
from typing import Iterable, List, TypeVar

import more_itertools
import networkx

from advent_of_code_2020_py import problem


def Differences(adapters: List[int]) -> List[int]:
    return [b - a for a, b in more_itertools.windowed(adapters, 2)]


def PreprocessAdapters(adapters: Iterable[int]) -> List[int]:
    adapters = list(adapters)
    return sorted(itertools.chain(adapters, [0, 3 + max(adapters)]))


def BuildGraph(adapters: List[int]) -> networkx.DiGraph[int]:
    result = networkx.DiGraph()
    result.add_nodes_from(adapters)
    for idx, element in enumerate(adapters):
        for next_element in adapters[idx + 1 : idx + 4]:
            if next_element - element <= 3:
                result.add_edge(element, next_element)
    return result


T = TypeVar("T")


def CountPaths(graph: networkx.DiGraph[T], start: T, end: T) -> int:
    @functools.lru_cache
    def _CountPathsFromStart(idx) -> int:
        if idx == start:
            return 1
        return sum(_CountPathsFromStart(p) for p in graph.predecessors(idx))

    return _CountPathsFromStart(end)


def part1():
    adapters = PreprocessAdapters(problem.Get(10, int))
    differences = Differences(adapters)
    counts = collections.Counter(differences)
    print(counts[1] * counts[3])


def part2():
    adapters = PreprocessAdapters(problem.Get(10, int))
    graph = BuildGraph(adapters)
    print(CountPaths(graph, 0, max(graph.nodes)))


if __name__ == "__main__":
    part1()
    part2()
