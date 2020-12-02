from typing import Callable, Iterator, TypeVar

ProblemRowType = TypeVar("ProblemRowType")


def Get(
    problem_number: int,
    transform: Callable[[str], ProblemRowType] = lambda x: x,
) -> Iterator[ProblemRowType]:
    with open(f"inputs/problem{problem_number:02}.txt", "r") as f:
        for line in f:
            yield transform(line)
