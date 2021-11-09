import unittest
import unittest.mock

from relations_sqlite import *


class TestDDL(unittest.TestCase):

    maxDiff = None

    def test_class(self):

        self.assertEqual(DDL.QUOTE, """`""")
        self.assertEqual(DDL.STR, """'""")
        self.assertEqual(DDL.SEPARATOR, """.""")
        self.assertEqual(DDL.PLACEHOLDER, """?""")
        self.assertEqual(DDL.JSONIFY, """json_extract(%s,'$')""")
        self.assertEqual(DDL.PATH, """json_extract(%s,%s)""")
