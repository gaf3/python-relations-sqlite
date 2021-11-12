import unittest
import unittest.mock

import os
import json
import sqlite3

import ipaddress

import relations
import relations_sqlite


class Meta(relations.Model):

    SCHEMA = "test_sqlite3"

    id = int,{"auto": True}
    name = str
    flag = bool
    spend = float
    people = set
    stuff = list
    things = dict, {"extract": "for__0____1"}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class TestSQLite3(unittest.TestCase):

    maxDiff = None

    def setUp(self):

        self.connection = sqlite3.connect("/main.db")
        self.connection.cursor().execute(f"ATTACH DATABASE '/test_sqlite3.db' AS `test_sqlite3`")

        self.connection.row_factory = dict_factory

    def tearDown(self):

        self.connection.close()

        if os.path.exists("/main.db"):
            os.remove("/main.db")

        if os.path.exists("/test_sqlite3.db"):
            os.remove("/test_sqlite3.db")

    def test_execute(self):

        cursor = self.connection.cursor()

        ddl = relations_sqlite.TABLE(Meta.thy().define())

        ddl.generate(indent=2)

        for sql in ddl.sql.split(";\n"):
            if sql:
                cursor.execute(sql)

        query = relations_sqlite.INSERT(
            "test_sqlite3.meta"
        ).VALUES(**{
            "name": "yep",
            "flag": True,
            "spend": 1.1,
            "people": {"tom"},
            "stuff": [1, None],
            "things": {"a": 1}
        }).VALUES(
            name="dive",
            flag=False,
            spend=3.5,
            people={"tom", "mary"},
            stuff=[1, 2, 3, None],
            things={"a": {"b": [1, 2], "c": "sure"}, "4": 5, "for": [{"1": "yep"}]}
        )

        query.generate()

        cursor.execute(query.sql, query.args)

        def check(value, **kwargs):

            query = relations_sqlite.SELECT(
                "name"
            ).FROM(
                "test_sqlite3.meta"
            ).WHERE(
                **kwargs
            )

            query.generate()

            cursor.execute(query.sql, query.args)

            rows = cursor.fetchall()

            if len(rows) != 1:
                name = None
            else:
                name = rows[0]["name"]

            self.assertEqual(name, value, query.sql)

        check("yep", flag=True)

        check("dive", flag=False)

        check("dive", people={"tom", "mary"})

        check("dive", things={"a": {"b": [1, 2], "c": "sure"}, "4": 5, "for": [{"1": "yep"}]})

        check("dive", stuff__1=2)

        check("dive", things__a__b__0=1)

        check("dive", things__a__c__like="su")

        check("yep", things__a__b__null=True)

        check("dive", things____4=5)

        check(None, things__a__b__0__gt=1)

        check(None, things__a__c__not_like="su")

        check(None, things__a__d__null=False)

        check(None, things____4=6)

        check("dive", things__a__b__has=1)

        check(None, things__a__b__has=[1, 3])

        check("dive", name="dive", things__a__b__not_has=[1, 3])

        check("yep", name="yep", things__a__b__not_has=[1, 3])

        check("dive", things__a__b__any=[1, 3])

        check(None, things__a__b__any=[4, 3])

        check("dive", things__a__b__all=[2, 1])

        check(None, things__a__b__all=[3, 2, 1])

        check("dive", people__has="mary")

        check(None, people__has="dick")

        check("dive", people__any=["mary", "dick"])

        check(None, people__any=["harry", "dick"])

        check("dive", people__all=["mary", "tom"])

        check(None, people__all=["tom", "dick", "mary"])
