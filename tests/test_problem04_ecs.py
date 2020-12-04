import unittest

import esper

from advent_of_code_2020_py import problem04_ecs

DATA_1 = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

INVALID_PASSPORTS = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""

VALID_PASSPORTS = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""


class Test01(unittest.TestCase):
    def test_example1(self):
        world = esper.World()
        world.add_processor(problem04_ecs.FieldPresenceValidator())
        problem04_ecs.ParseFile(DATA_1.splitlines(), world)
        world.process()
        validities = {
            "860033327": True,
            "028048884": False,
            "760753108": True,
            "166559648": False,
        }
        for e, (p, pid) in world.get_components(
            problem04_ecs.Passport, problem04_ecs.PassportID
        ):
            target = validities[pid.pid]
            self.assertEqual(
                p.valid,
                target,
                f"Passport with PID {pid.pid} should have validity {target}",
            )

    def test_example2(self):
        world = esper.World()
        problem04_ecs.WorldSetup(world)
        problem04_ecs.ParseFile(INVALID_PASSPORTS.splitlines(), world)
        world.process()
        for e, (p, pid) in world.get_components(
            problem04_ecs.Passport, problem04_ecs.PassportID
        ):
            self.assertFalse(
                p.valid, f"Passport with PID {pid.pid} should be invalid"
            )

    def test_example3(self):
        world = esper.World()
        problem04_ecs.WorldSetup(world)
        problem04_ecs.ParseFile(VALID_PASSPORTS.splitlines(), world)
        world.process()
        for e, (p, pid) in world.get_components(
            problem04_ecs.Passport, problem04_ecs.PassportID
        ):
            self.assertTrue(
                p.valid, f"Passport with PID {pid.pid} should be valid"
            )


if __name__ == "__main__":
    unittest.main()
