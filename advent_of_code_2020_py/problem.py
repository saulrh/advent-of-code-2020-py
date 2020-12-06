from typing import Callable, Iterable, Iterator, TypeVar

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


def InBatches(
    lines: Iterable[str],
    line_transform: Callable[[str], ProblemRowType] = lambda x: x,
    batch_transform: Callable[
        [Iterable[ProblemRowType]], ProblemType
    ] = lambda xs: xs,
) -> Iterable[ProblemType]:
    batch = []
    for line in lines:
        line = line.strip()
        if not line:
            yield batch_transform(batch)
            batch = []
        else:
            batch.append(line_transform(line))
    yield batch_transform(batch)


def GetBatches(
    problem_number: int,
    line_transform: Callable[[str], ProblemRowType] = lambda x: x,
    batch_transform: Callable[
        [Iterable[ProblemRowType]], ProblemType
    ] = lambda xs: xs,
) -> Iterable[ProblemType]:
    with open(_Filename(problem_number), "r") as f:
        yield from InBatches(f, line_transform, batch_transform)
