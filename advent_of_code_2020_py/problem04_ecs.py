#!/usr/bin/env python

from __future__ import annotations

import dataclasses
import re
from typing import Iterable

import esper

from advent_of_code_2020_py import problem

HGT_RE = re.compile(r"(?P<value>\d+)(?P<unit>cm|in)")
HCL_RE = re.compile(r"#[0-9a-f]{6}")
VALID_ECLS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


@dataclasses.dataclass
class Passport(object):
    valid: bool


@dataclasses.dataclass
class HairColor(object):
    hcl: str


@dataclasses.dataclass
class Height(object):
    hgt: str


@dataclasses.dataclass
class BirthYear(object):
    byr: str


@dataclasses.dataclass
class IssueYear(object):
    iyr: str


@dataclasses.dataclass
class ExpirationYear(object):
    eyr: str


@dataclasses.dataclass
class EyeColor(object):
    ecl: str


@dataclasses.dataclass
class PassportID(object):
    pid: str


@dataclasses.dataclass
class CountryID(object):
    cid: str


class BirthYearValidator(esper.Processor):
    def validate(self, s):
        return (
            len(s) == 4 and s.isdigit() and int(s) >= 1920 and int(s) <= 2002
        )

    def process(self):
        for ent, (passport, byr) in self.world.get_components(
            Passport, BirthYear
        ):
            passport.valid &= self.validate(byr.byr)


class IssueYearValidator(esper.Processor):
    def validate(self, s):
        return (
            len(s) == 4 and s.isdigit() and int(s) >= 2010 and int(s) <= 2020
        )

    def process(self):
        for ent, (passport, iyr) in self.world.get_components(
            Passport, IssueYear
        ):
            passport.valid &= self.validate(iyr.iyr)


class ExpirationYearValidator(esper.Processor):
    def validate(self, s):
        return (
            len(s) == 4 and s.isdigit() and int(s) >= 2020 and int(s) <= 2030
        )

    def process(self):
        for ent, (passport, eyr) in self.world.get_components(
            Passport, ExpirationYear
        ):
            passport.valid &= self.validate(eyr.eyr)


class HeightValidator(esper.Processor):
    def process(self):
        for ent, (passport, hgt) in self.world.get_components(
            Passport, Height
        ):
            passport.valid &= self.validate(hgt.hgt)

    def validate(self, s):
        match = HGT_RE.fullmatch(s)
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


class HairColorValidator(esper.Processor):
    def validate(self, s):
        return HCL_RE.fullmatch(s) is not None

    def process(self):
        for ent, (passport, hcl) in self.world.get_components(
            Passport, HairColor
        ):
            passport.valid &= self.validate(hcl.hcl)


class EyeColorValidator(esper.Processor):
    def validate(self, s):
        return s in VALID_ECLS

    def process(self):
        for ent, (passport, ecl) in self.world.get_components(
            Passport, EyeColor
        ):
            passport.valid &= self.validate(ecl.ecl)


class PassportIDValidator(esper.Processor):
    def validate(self, s):
        return s is not None and len(s) == 9 and s.isdigit()

    def process(self):
        for ent, (passport, pid) in self.world.get_components(
            Passport, PassportID
        ):
            passport.valid &= self.validate(pid.pid)


PASSPORT_REQUIRED_COMPONENTS = [
    HairColor,
    Height,
    BirthYear,
    IssueYear,
    ExpirationYear,
    EyeColor,
    PassportID,
]


class FieldPresenceValidator(esper.Processor):
    def process(self):
        for ent, (passport,) in self.world.get_components(Passport):
            for c in PASSPORT_REQUIRED_COMPONENTS:
                passport.valid &= self.world.has_component(ent, c)


FIELD_TO_COMPONENT = {
    "byr": BirthYear,
    "iyr": IssueYear,
    "eyr": ExpirationYear,
    "hgt": Height,
    "hcl": HairColor,
    "ecl": EyeColor,
    "pid": PassportID,
    "cid": CountryID,
}


def ParseFile(lines: Iterable[str], world: esper.World):
    working = world.create_entity()
    world.add_component(working, Passport(True))
    for line in lines:
        words = line.strip().split()
        if not words:
            working = world.create_entity()
            world.add_component(working, Passport(True))
        for word in words:
            tag, value = word.split(":")
            world.add_component(working, FIELD_TO_COMPONENT[tag](value))


def WorldSetup(w: esper.World):
    w.add_processor(BirthYearValidator())
    w.add_processor(IssueYearValidator())
    w.add_processor(ExpirationYearValidator())
    w.add_processor(HeightValidator())
    w.add_processor(HairColorValidator())
    w.add_processor(EyeColorValidator())
    w.add_processor(PassportIDValidator())
    w.add_processor(FieldPresenceValidator())


def part1():
    world = esper.World()
    world.add_processor(FieldPresenceValidator())
    ParseFile(problem.GetRaw(4).splitlines(), world)
    world.process()
    print(sum(p.valid for e, (p,) in world.get_components(Passport)))


def part2():
    world = esper.World()
    WorldSetup(world)
    ParseFile(problem.GetRaw(4).splitlines(), world)
    world.process()
    print(sum(p.valid for e, (p,) in world.get_components(Passport)))


if __name__ == "__main__":
    part1()
    part2()
