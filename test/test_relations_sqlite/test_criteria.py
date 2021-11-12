import unittest
import unittest.mock

from relations_sqlite import *


class TestAND(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        criteria = AND(EQ("totes", "maigoats"), EQ("toast", "myghost", invert=True))
        criteria.generate()
        self.assertEqual(criteria.sql, """(`totes`=? AND `toast`!=?)""")
        self.assertEqual(criteria.args, ["maigoats", "myghost"])

        criteria.generate(indent=2)
        self.assertEqual(criteria.sql, """(
  `totes`=? AND
  `toast`!=?
)""")

        criteria.generate(indent=2, count=1)
        self.assertEqual(criteria.sql, """(
    `totes`=? AND
    `toast`!=?
  )""")

        criteria.generate(indent=2, count=2)
        self.assertEqual(criteria.sql, """(
      `totes`=? AND
      `toast`!=?
    )""")


class TestOR(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        criteria = OR(EQ("totes", "maigoats"), EQ("toast", "myghost", invert=True))
        criteria.generate()
        self.assertEqual(criteria.sql, """(`totes`=? OR `toast`!=?)""")
        self.assertEqual(criteria.args, ["maigoats", "myghost"])

        criteria.generate(indent=2)
        self.assertEqual(criteria.sql, """(
  `totes`=? OR
  `toast`!=?
)""")

        criteria.generate(indent=2, count=1)
        self.assertEqual(criteria.sql, """(
    `totes`=? OR
    `toast`!=?
  )""")

        criteria.generate(indent=2, count=2)
        self.assertEqual(criteria.sql, """(
      `totes`=? OR
      `toast`!=?
    )""")


class TestHAS(unittest.TestCase):

    def test_generate(self):

        criteria = HAS("totes", ["mai", "goats"])

        criteria.generate()
        self.assertEqual(criteria.sql, """(NOT (SELECT COUNT(*) FROM json_each(json_extract(?,'$')) as l LEFT JOIN json_each(`totes`) as r ON l.value=r.value WHERE r.value IS NULL))""")
        self.assertEqual(criteria.args, ['["mai", "goats"]'])


class TestANY(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        criteria = ANY("totes", ["mai", "goats"])

        criteria.generate()
        self.assertEqual(criteria.sql, """((NOT (SELECT COUNT(*) FROM json_each(json_extract(?,'$')) as l LEFT JOIN json_each(`totes`) as r ON l.value=r.value WHERE r.value IS NULL)) OR (NOT (SELECT COUNT(*) FROM json_each(json_extract(?,'$')) as l LEFT JOIN json_each(`totes`) as r ON l.value=r.value WHERE r.value IS NULL)))""")
        self.assertEqual(criteria.args, ['["mai"]', '["goats"]'])


class TestALL(unittest.TestCase):

    def test_generate(self):

        criteria = ALL("totes", ["mai", "goats"])

        criteria.generate()
        self.assertEqual(criteria.sql, """((NOT (SELECT COUNT(*) FROM json_each(json_extract(?,'$')) as l LEFT JOIN json_each(`totes`) as r ON l.value=r.value WHERE r.value IS NULL)) AND json_array_length(`totes`)=json_array_length(json_extract(?,'$')))""")
        self.assertEqual(criteria.args, ['["mai", "goats"]', '["mai", "goats"]'])


class TestOP(unittest.TestCase):

    def test_generate(self):

        criteria = OP("totes__null", True)

        criteria.generate()
        self.assertEqual(criteria.sql, """`totes` IS NULL""")
        self.assertEqual(criteria.args, [])

        criteria = OP(totes__a__null=False)

        criteria.generate()
        self.assertEqual(criteria.sql, """json_extract(`totes`,?) IS NOT NULL""")
        self.assertEqual(criteria.args, ['$.a'])

        criteria = OP(totes__a__not_null=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """json_extract(`totes`,?) IS NOT NULL""")
        self.assertEqual(criteria.args, ['$.a'])

        criteria = OP(totes__a__not_has=[1, 2, 3])

        criteria.generate()
        self.assertEqual(criteria.sql, """NOT (NOT (SELECT COUNT(*) FROM json_each(json_extract(?,'$')) as l LEFT JOIN json_each(json_extract(`totes`,?)) as r ON l.value=r.value WHERE r.value IS NULL))""")
        self.assertEqual(criteria.args, ['[1, 2, 3]', '$.a'])

        criteria = OP(totes=1, JSONIFY=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """json_extract(`totes`,'$')=json_extract(?,'$')""")
        self.assertEqual(criteria.args, ['1'])

        self.assertRaisesRegex(relations_sql.SQLError, "need single pair", OP, "nope")

        criteria = OP(totes__a__null=False, EXTRACTED=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """`totes__a` IS NOT NULL""")
        self.assertEqual(criteria.args, [])

        criteria = OP(totes__a__has=1, EXTRACTED=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """(NOT (SELECT COUNT(*) FROM json_each(json_extract(?,'$')) as l LEFT JOIN json_each(`totes__a`) as r ON l.value=r.value WHERE r.value IS NULL))""")
        self.assertEqual(criteria.args, ["[1]"])

        criteria = OP(totes__a__any=[1, 2], EXTRACTED=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """((NOT (SELECT COUNT(*) FROM json_each(json_extract(?,'$')) as l LEFT JOIN json_each(`totes__a`) as r ON l.value=r.value WHERE r.value IS NULL)) OR (NOT (SELECT COUNT(*) FROM json_each(json_extract(?,'$')) as l LEFT JOIN json_each(`totes__a`) as r ON l.value=r.value WHERE r.value IS NULL)))""")
        self.assertEqual(criteria.args, ['[1]', '[2]'])

        criteria = OP(totes__a__all=[1, 2], EXTRACTED=True)

        criteria.generate()
        self.assertEqual(criteria.sql, """((NOT (SELECT COUNT(*) FROM json_each(json_extract(?,'$')) as l LEFT JOIN json_each(`totes__a`) as r ON l.value=r.value WHERE r.value IS NULL)) AND json_array_length(`totes__a`)=json_array_length(json_extract(?,'$')))""")
        self.assertEqual(criteria.args, ['[1, 2]', '[1, 2]'])

        self.assertRaisesRegex(relations_sql.SQLError, "need single pair", OP, "nope")
