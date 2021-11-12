import unittest
import unittest.mock

from relations_sqlite import *


class TestVALUE(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = VALUE(None)
        expression.generate()
        self.assertEqual(expression.sql, """?""")
        self.assertEqual(expression.args, [None])

        expression = VALUE("unit")
        expression.generate()
        self.assertEqual(expression.sql, """?""")
        self.assertEqual(expression.args, ["unit"])

        expression = VALUE("test", jsonify=True)
        expression.generate()
        self.assertEqual(expression.sql, """json_extract(?,'$')""")
        self.assertEqual(expression.args, ['"test"'])

        expression = VALUE({"a": 1})
        expression.generate()
        self.assertEqual(expression.sql, """json_extract(?,'$')""")
        self.assertEqual(expression.args, ['{"a": 1}'])

        expression = VALUE({'a', 'b'})
        expression.generate()
        self.assertEqual(expression.sql, """json_extract(?,'$')""")
        self.assertEqual(expression.args, ['["a", "b"]'])

class TestNOT(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = NOT("unit")
        expression.generate()
        self.assertEqual(expression.sql, """NOT ?""")
        self.assertEqual(expression.args, ["unit"])

        expression = NOT(relations_sql.SQL("test"))
        expression.generate()
        self.assertEqual(expression.sql, """NOT test""")
        self.assertEqual(expression.args, [])


class TestLIST(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = LIST(["unit", "test"])
        expression.generate()
        self.assertEqual(expression.sql, """?,?""")
        self.assertEqual(expression.args, ["unit", "test"])

        expression = LIST(["unit", "test"], jsonify=True)
        expression.generate()
        self.assertEqual(expression.sql, """json_extract(?,'$'),json_extract(?,'$')""")
        self.assertEqual(expression.args, ['"unit"', '"test"'])

        expression = LIST([{"a": 1}, {"b": 2}])
        expression.generate()
        self.assertEqual(expression.sql, """json_extract(?,'$'),json_extract(?,'$')""")
        self.assertEqual(expression.args, ['{"a": 1}', '{"b": 2}'])

        expression.generate(indent=2)
        self.assertEqual(expression.sql, """json_extract(?,'$'),
json_extract(?,'$')""")

        expression.generate(indent=2, count=1)
        self.assertEqual(expression.sql, """json_extract(?,'$'),
  json_extract(?,'$')""")

        expression.generate(indent=2, count=2)
        self.assertEqual(expression.sql, """json_extract(?,'$'),
    json_extract(?,'$')""")


class TestNAME(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = NAME("people")
        expression.generate()
        self.assertEqual(expression.sql, """`people`""")
        self.assertEqual(expression.args, [])


class TestSCHEMA_NAME(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = SCHEMA_NAME("people")
        expression.generate()
        self.assertEqual(expression.sql, """`people`""")
        self.assertEqual(expression.args, [])


class TestTABLE_NAME(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = TABLE_NAME("people.stuff", prefix="things")
        expression.generate()
        self.assertEqual(expression.sql, """things `people`.`stuff`""")
        self.assertEqual(expression.args, [])

        schema = relations_sql.SQL("unit", ["test"])
        expression = TABLE_NAME("stuff", schema=schema)
        expression.generate()
        self.assertEqual(expression.sql, """unit.`stuff`""")
        self.assertEqual(expression.args, ["test"])

        expression = TABLE_NAME("people.stuff", prefix="PRE")

        expression.generate(indent=2)
        self.assertEqual(expression.sql, """PRE
  `people`.`stuff`""")

        expression.generate(indent=2, count=1)
        self.assertEqual(expression.sql, """PRE
    `people`.`stuff`""")

        expression.generate(indent=2, count=2)
        self.assertEqual(expression.sql, """PRE
      `people`.`stuff`""")

        expression = TABLE_NAME("people.stuff", prefix="")

        expression.generate(indent=2)
        self.assertEqual(expression.sql, """  `people`.`stuff`""")

        expression.generate(indent=2, count=1)
        self.assertEqual(expression.sql, """  `people`.`stuff`""")

        expression.generate(indent=2, count=2)
        self.assertEqual(expression.sql, """  `people`.`stuff`""")


class TestCOLUMN_NAME(unittest.TestCase):

    maxDiff = None

    def test_walk(self):

        column, path = COLUMN_NAME.split("things__a__b__0____1")
        self.assertEqual(COLUMN_NAME.walk(path), '$.a.b[0]."1"')

    def test_generate(self):

        expression = COLUMN_NAME("*")
        expression.generate()
        self.assertEqual(expression.sql, """*""")
        self.assertEqual(expression.args, [])

        expression = COLUMN_NAME("people.stuff.things", jsonify=True)
        expression.generate()
        self.assertEqual(expression.sql, """json_extract(`people`.`stuff`.`things`,'$')""")
        self.assertEqual(expression.args, [])

        table = relations_sql.SQL("test", ["unit"])

        expression = COLUMN_NAME("people.stuff.things__a__0___1____2_____3", table=table)
        expression.generate()
        self.assertEqual(expression.sql, """json_extract(test.`things`,?)""")
        self.assertEqual(expression.args, ["unit", '$.a[0][-1]."2"."-3"'])

        schema = relations_sql.SQL("unit", ["test"])

        expression = COLUMN_NAME("people.stuff.things__a__0___1____2_____3", schema=schema)
        expression.generate()
        self.assertEqual(expression.sql, """json_extract(unit.`stuff`.`things`,?)""")
        self.assertEqual(expression.args, ["test", '$.a[0][-1]."2"."-3"'])


class TestNAMES(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = NAMES(["unit", relations_sql.SQL("test")])
        expression.generate()
        self.assertEqual(expression.sql, """`unit`,test""")
        self.assertEqual(expression.args, [])


class TestCOLUMN_NAMES(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = COLUMN_NAMES(["unit", relations_sql.SQL("test")])
        expression.generate()
        self.assertEqual(expression.sql, """(`unit`,test)""")
        self.assertEqual(expression.args, [])

        expression.generate(indent=2)
        self.assertEqual(expression.sql, """  (
    `unit`,
    test
  )""")

        expression.generate(indent=2, count=1)
        self.assertEqual(expression.sql, """  (
      `unit`,
      test
    )""")

        expression.generate(indent=2, count=2)
        self.assertEqual(expression.sql, """  (
        `unit`,
        test
      )""")


class TestAS(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        column = relations_sql.SQL("test", ["unit"])

        expression = AS("people", column)
        expression.generate()
        self.assertEqual(expression.sql, """test AS `people`""")
        self.assertEqual(expression.args, ["unit"])

        label = relations_sql.SQL("unit", ["test"])

        expression = AS(label, column)
        expression.generate()
        self.assertEqual(expression.sql, """test AS unit""")
        self.assertEqual(expression.args, ["unit", "test"])

        expression.generate(indent=2)
        self.assertEqual(expression.sql, """test AS unit""")


class TestORDER(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = ORDER("people")
        expression.generate()
        self.assertEqual(expression.sql, """`people`""")
        self.assertEqual(expression.args, [])

        expression = ORDER("people", ASC)
        expression.generate()
        self.assertEqual(expression.sql, """`people` ASC""")
        self.assertEqual(expression.args, [])

        expression = ORDER(people=DESC)
        expression.generate()
        self.assertEqual(expression.sql, """`people` DESC""")
        self.assertEqual(expression.args, [])

        column = relations_sql.SQL("test", ["unit"])

        expression = ORDER(column)
        expression.generate()
        self.assertEqual(expression.sql, """test""")
        self.assertEqual(expression.args, ["unit"])

        column = relations_sql.SQL("", [])

        expression = ORDER(column)
        self.assertFalse(expression.generate())


class TestASSIGN(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        expression = ASSIGN("people", "stuff")
        expression.generate()
        self.assertEqual(expression.sql, """`people`=?""")
        self.assertEqual(expression.args, ["stuff"])

        column = relations_sql.SQL("unit", ["test"])
        value = relations_sql.SQL("test", ["unit"])

        expression = ASSIGN(column, value)
        expression.generate()
        self.assertEqual(expression.sql, """unit=test""")
        self.assertEqual(expression.args, ["test", "unit"])

        expression.generate(indent=2)
        self.assertEqual(expression.sql, """unit=test""")
