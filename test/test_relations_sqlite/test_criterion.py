import unittest
import unittest.mock

from relations_sqlite import *



class TestNULL(unittest.TestCase):

    def test_generate(self):

        criterion = NULL("totes", True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` IS NULL""")
        self.assertEqual(criterion.args, [])

        criterion = NULL(totes__a=False)

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?) IS NOT NULL""")
        self.assertEqual(criterion.args, ['$.a'])


class TestEQ(unittest.TestCase):

    def test_generate(self):

        criterion = EQ("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`=?""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = EQ("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`!=?""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = EQ(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?)=?""")
        self.assertEqual(criterion.args, ['$.a', 'maigoats'])


class TestGT(unittest.TestCase):

    def test_generate(self):

        criterion = GT("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`>?""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = GT(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?)>?""")
        self.assertEqual(criterion.args, ['$.a', 'maigoats'])


class TestGTE(unittest.TestCase):

    def test_generate(self):

        criterion = GTE("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`>=?""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = GTE(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?)>=?""")
        self.assertEqual(criterion.args, ['$.a', 'maigoats'])


class TestLT(unittest.TestCase):

    def test_generate(self):

        criterion = LT("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`<?""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = LT(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?)<?""")
        self.assertEqual(criterion.args, ['$.a', 'maigoats'])


class TestLTE(unittest.TestCase):

    def test_generate(self):

        criterion = LTE("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes`<=?""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = LTE(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?)<=?""")
        self.assertEqual(criterion.args, ['$.a', 'maigoats'])


class TestLIKE(unittest.TestCase):

    def test_generate(self):

        criterion = LIKE("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` LIKE ?""")
        self.assertEqual(criterion.args, ["%maigoats%"])

        criterion = LIKE("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` NOT LIKE ?""")
        self.assertEqual(criterion.args, ["%maigoats%"])

        criterion = LIKE(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?) LIKE ?""")
        self.assertEqual(criterion.args, ['$.a', '%maigoats%'])


class TestSTART(unittest.TestCase):

    def test_generate(self):

        criterion = START("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` LIKE ?""")
        self.assertEqual(criterion.args, ["maigoats%"])

        criterion = START("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` NOT LIKE ?""")
        self.assertEqual(criterion.args, ["maigoats%"])

        criterion = START(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?) LIKE ?""")
        self.assertEqual(criterion.args, ['$.a', 'maigoats%'])


class TestEND(unittest.TestCase):

    def test_generate(self):

        criterion = END("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` LIKE ?""")
        self.assertEqual(criterion.args, ["%maigoats"])

        criterion = END("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` NOT LIKE ?""")
        self.assertEqual(criterion.args, ["%maigoats"])

        criterion = END(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?) LIKE ?""")
        self.assertEqual(criterion.args, ['$.a', '%maigoats'])


class TestIN(unittest.TestCase):

    def test_generate(self):

        criterion = IN("totes", ["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` IN (?,?)""")
        self.assertEqual(criterion.args, ["mai", "goats"])

        criterion = IN("totes", ["mai", "goats"], invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """`totes` NOT IN (?,?)""")
        self.assertEqual(criterion.args, ["mai", "goats"])

        criterion = IN(totes__a=["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(`totes`,?) IN (?,?)""")
        self.assertEqual(criterion.args, ['$.a', 'mai', 'goats'])

        criterion = IN(totes__a=[])

        criterion.generate()
        self.assertEqual(criterion.sql, """?""")
        self.assertEqual(criterion.args, [False])


class TestCONTAINS(unittest.TestCase):

    def test_generate(self):

        criterion = CONTAINS("totes", ["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """json_extract(?,'$') IN (SELECT json_data.value FROM json_each(`totes`) AS json_data)""")
        self.assertEqual(criterion.args, ['["mai", "goats"]'])


class TestLENGTHS(unittest.TestCase):

    def test_generate(self):

        criterion = LENGTHS("totes", ["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """json_array_length(`totes`)=json_array_length(json_extract(?,'$'))""")
        self.assertEqual(criterion.args, ['["mai", "goats"]'])
