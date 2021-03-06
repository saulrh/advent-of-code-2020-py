#!/usr/bin/env python

from __future__ import annotations

import dataclasses
import re
from typing import Iterable, Mapping, Optional

from advent_of_code_2020_py import problem

HGT_RE = re.compile(r"(?P<value>\d+)(?P<unit>cm|in)")
HCL_RE = re.compile(r"#[0-9a-f]{6}")
VALID_ECLS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


@dataclasses.dataclass
class Passport(object):
    byr: Optional[str] = None
    iyr: Optional[str] = None
    eyr: Optional[str] = None
    hgt: Optional[str] = None
    hcl: Optional[str] = None
    ecl: Optional[str] = None
    pid: Optional[str] = None
    cid: Optional[str] = None

    @property
    def byr_valid(self) -> bool:
        return (
            self.byr is not None
            and len(self.byr) == 4
            and self.byr.isdigit()
            and int(self.byr) >= 1920
            and int(self.byr) <= 2002
        )

    @property
    def iyr_valid(self) -> bool:
        return (
            self.iyr is not None
            and len(self.iyr) == 4
            and self.iyr.isdigit()
            and int(self.iyr) >= 2010
            and int(self.iyr) <= 2020
        )

    @property
    def eyr_valid(self) -> bool:
        return (
            self.eyr is not None
            and len(self.eyr) == 4
            and self.eyr.isdigit()
            and int(self.eyr) >= 2020
            and int(self.eyr) <= 2030
        )

    @property
    def hgt_valid(self) -> bool:
        if not self.hgt:
            return False
        match = HGT_RE.fullmatch(self.hgt)
        if not match:
            return False
        value = int(match.group("value"))
        unit = match.group("unit")
        if unit == "cm":
            return 150 <= value <= 193
        elif unit == "in":
            return 59 <= value <= 76
        else:
            # Should be impossible because the regex wouldn't have
            # matched, but whatever
            raise ValueError(f"Invalid unit {unit}")

    @property
    def hcl_valid(self) -> bool:
        if not self.hcl:
            return False
        return HCL_RE.fullmatch(self.hcl) is not None

    @property
    def ecl_valid(self) -> bool:
        if not self.ecl:
            return False
        return self.ecl in VALID_ECLS

    @property
    def pid_valid(self) -> bool:
        return (
            self.pid is not None and len(self.pid) == 9 and self.pid.isdigit()
        )

    @property
    def cid_valid(self) -> bool:
        # don't even care if it's missing
        return True

    @property
    def Part1Valid(self) -> bool:
        # CID not present
        missing = (
            not self.byr
            or not self.iyr
            or not self.eyr
            or not self.hgt
            or not self.hcl
            or not self.ecl
            or not self.pid
        )
        return not missing

    @property
    def Part2Valid(self) -> bool:
        return (
            self.byr_valid
            and self.iyr_valid
            and self.eyr_valid
            and self.hgt_valid
            and self.hcl_valid
            and self.ecl_valid
            and self.pid_valid
            and self.cid_valid
        )


def LineTransform(line: str) -> Mapping[str, str]:
    return dict(word.split(":", maxsplit=1) for word in line.split())


def BatchTransform(group: Iterable[Mapping[str, str]]) -> Passport:
    fields = {}
    for partial in group:
        fields.update(partial)
    return Passport(**fields)


def part1():
    passports = problem.GetBatches(4, LineTransform, BatchTransform)
    print(sum(p.Part1Valid for p in passports))


def part2():
    passports = problem.GetBatches(4, LineTransform, BatchTransform)
    print(sum(p.Part2Valid for p in passports))


if __name__ == "__main__":
    part1()
    part2()
