import unittest
import unittest.mock

from relations_sqlite import *


class TestOPTIONS(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = OPTIONS()
        self.assertFalse(clause)

        clause("people", "stuff", "things")
        clause.generate()
        self.assertEqual(clause.sql, """people stuff things""")
        self.assertEqual(clause.args, [])

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """  people
  stuff
  things""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """  people
    stuff
    things""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """  people
      stuff
      things""")


class TestFIELDS(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = FIELDS()

        self.assertFalse(clause)

        clause("*")
        clause.generate()
        self.assertEqual(clause.sql, """*""")
        self.assertEqual(clause.args, [])

        clause(stuff="things")
        clause.generate()
        self.assertEqual(clause.sql, """*,`things` AS `stuff`""")
        self.assertEqual(clause.args, [])

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """  *,
  `things` AS `stuff`""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """  *,
    `things` AS `stuff`""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """  *,
      `things` AS `stuff`""")


class TestFROM(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = FROM()

        self.assertFalse(clause)

        clause("people", stuff="things")
        clause.generate()
        self.assertEqual(clause.sql, """FROM `people`,`things` AS `stuff`""")
        self.assertEqual(clause.args, [])

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """FROM
  `people`,
  `things` AS `stuff`""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """FROM
    `people`,
    `things` AS `stuff`""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """FROM
      `people`,
      `things` AS `stuff`""")


class TestWHERE(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = WHERE()

        self.assertFalse(clause)

        clause("people", stuff="things")
        clause.generate()
        self.assertEqual(clause.sql, """WHERE ? AND `stuff`=?""")
        self.assertEqual(clause.args, ["people", "things"])

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """WHERE
  ? AND
  `stuff`=?""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """WHERE
    ? AND
    `stuff`=?""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """WHERE
      ? AND
      `stuff`=?""")


class TestGROUP_BY(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = GROUP_BY()

        self.assertFalse(clause)

        clause("people", "stuff", "things")
        clause.generate()
        self.assertEqual(clause.sql, """GROUP BY `people`,`stuff`,`things`""")
        self.assertEqual(clause.args, [])

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """GROUP BY
  `people`,
  `stuff`,
  `things`""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """GROUP BY
    `people`,
    `stuff`,
    `things`""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """GROUP BY
      `people`,
      `stuff`,
      `things`""")


class TestHAVING(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = HAVING()

        self.assertFalse(clause)

        clause("people", stuff="things")
        clause.generate()
        self.assertEqual(clause.sql, """HAVING ? AND `stuff`=?""")
        self.assertEqual(clause.args, ["people", "things"])

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """HAVING
  ? AND
  `stuff`=?""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """HAVING
    ? AND
    `stuff`=?""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """HAVING
      ? AND
      `stuff`=?""")


class TestORDER_BY(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = ORDER_BY()

        self.assertFalse(clause)

        clause("people", stuff=ASC, things=DESC)
        clause.generate()
        self.assertEqual(clause.sql, """ORDER BY `people`,`stuff` ASC,`things` DESC""")
        self.assertEqual(clause.args, [])

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """ORDER BY
  `people`,
  `stuff` ASC,
  `things` DESC""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """ORDER BY
    `people`,
    `stuff` ASC,
    `things` DESC""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """ORDER BY
      `people`,
      `stuff` ASC,
      `things` DESC""")


class TestLIMIT(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = LIMIT()

        self.assertFalse(clause)

        clause(10, 5)
        clause.generate()
        self.assertEqual(clause.sql, """LIMIT ? OFFSET ?""")
        self.assertEqual(clause.args, [10, 5])

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """LIMIT ? OFFSET ?""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """LIMIT ? OFFSET ?""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """LIMIT ? OFFSET ?""")


class TestSET(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = SET()

        self.assertFalse(clause)

        clause(fee="fie", foe="fum")
        clause.generate()
        self.assertEqual(clause.sql, """SET `fee`=?,`foe`=?""")
        self.assertEqual(clause.args, ["fie", "fum"])

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """SET
  `fee`=?,
  `foe`=?""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """SET
    `fee`=?,
    `foe`=?""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """SET
      `fee`=?,
      `foe`=?""")


class TestVALUES(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        clause = VALUES()

        self.assertFalse(clause)

        clause(fee="fie", foe="fum")
        clause.generate()
        self.assertEqual(clause.sql, """VALUES (?,?)""")
        self.assertEqual(clause.args, ["fie", "fum"])

        clause(fee="fie", foe="fum")

        clause.generate(indent=2)
        self.assertEqual(clause.sql, """VALUES
  (
    ?,
    ?
  ),(
    ?,
    ?
  )""")

        clause.generate(indent=2, count=1)
        self.assertEqual(clause.sql, """VALUES
    (
      ?,
      ?
    ),(
      ?,
      ?
    )""")

        clause.generate(indent=2, count=2)
        self.assertEqual(clause.sql, """VALUES
      (
        ?,
        ?
      ),(
        ?,
        ?
      )""")
