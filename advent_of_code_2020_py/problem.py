from typing import Callable, Iterator, TypeVar

ProblemRowType = TypeVar("ProblemRowType")
ProblemType = TypeVar("ProblemType")


def _Filename(problem_number: int) -> str:
    return f"inputs/problem{problem_number:02}.txt"


def GetRaw(
    problem_number: int, transform: Callable[[str], ProblemType] = lambda x: x
) -> ProblemType:
    with open(_Filename(problem_number), "r") as f:
        return transform(f.read())


def Get(
    problem_number: int,
    transform: Callable[[str], ProblemRowType] = lambda x: x,
) -> Iterator[ProblemRowType]:
    with open(_Filename(problem_number), "r") as f:
        for line in f:
            yield transform(line)
