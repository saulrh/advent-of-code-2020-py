import unittest

from advent_of_code_2020_py import problem16

DATA_1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

DATA_2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""


class Test16(unittest.TestCase):
    def test_Parse(self):
        p = problem16.Parse(DATA_1.splitlines())
        self.assertEqual(
            p,
            problem16.ProblemStatement(
                your_ticket=[7, 1, 14],
                tickets=[[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]],
                rules=[
                    problem16.Rule("class", 1, 3, 5, 7),
                    problem16.Rule("row", 6, 11, 33, 44),
                    problem16.Rule("seat", 13, 40, 45, 50),
                ],
            ),
        )

    def test_Part1(self):
        p = problem16.Parse(DATA_1.splitlines())
        self.assertCountEqual(
            list(p.KnownInvalidTickets()),
            [
                ([40, 4, 50], [4]),
                ([55, 2, 20], [55]),
                ([38, 6, 12], [12]),
            ],
        )
        self.assertEqual(
            sum(sum(invalids) for _, invalids in p.KnownInvalidTickets()), 71
        )
        self.assertEqual(list(p.ValidTickets()), [[7, 3, 47]])
        p.DiscardInvalidTickets()
        self.assertEqual(list(p.tickets), [[7, 3, 47]])

    def test_PossibleColumns(self):
        p = problem16.Parse(DATA_2.splitlines())
        p.DiscardInvalidTickets()
        columns = problem16.PossibleColumns(p.tickets, p.rules)
        self.assertEqual(columns[p.GetRule("class")], 1)
        self.assertEqual(columns[p.GetRule("row")], 0)
        self.assertEqual(columns[p.GetRule("seat")], 2)
        self.assertEqual(p.your_ticket[columns[p.GetRule("class")]], 12)
        self.assertEqual(p.your_ticket[columns[p.GetRule("row")]], 11)
        self.assertEqual(p.your_ticket[columns[p.GetRule("seat")]], 13)


if __name__ == "__main__":
    unittest.main()
