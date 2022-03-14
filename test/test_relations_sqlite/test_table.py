import unittest
import unittest.mock

import relations
from relations_sqlite import *


class Simple(relations.Model):
    id = int
    name = str

class Meta(relations.Model):
    id = int, {"auto": True}
    name = str
    flag = bool
    spend = float
    people = set
    stuff = list
    things = dict, {"extract": "for__0____1"}
    push = str, {"inject": "stuff___1__relations.io____1"}

    INDEX = "spend"


class TestTABLE(unittest.TestCase):

    maxDiff = None

    def test_name(self):

        ddl = TABLE(schema="people", name="stuff", definition={"schema": "persons", "name": "things"})

        self.assertEqual(ddl.name(), """`people`.`stuff`""")
        self.assertEqual(ddl.name(state="definition"), """`persons`.`things`""")
        self.assertEqual(ddl.name(state={"name": "definition", "schema": "migration"}), """`people`.`things`""")
        self.assertEqual(ddl.name(state={"name": "definition", "schema": "migration"}, prefix="_old_"), """`people`.`_old_things`""")
        self.assertEqual(ddl.name(state={"name": "definition", "schema": "migration"}, prefix="_old_", rename=True), """`_old_things`""")

    def test_create(self):

        ddl = TABLE(**Meta.thy().define())
        ddl.args = []

        ddl.create(indent=2)
        self.assertEqual(ddl.sql, """CREATE TABLE IF NOT EXISTS `meta` (
  `id` INTEGER PRIMARY KEY,
  `name` TEXT NOT NULL,
  `flag` INTEGER,
  `spend` REAL,
  `people` TEXT NOT NULL,
  `stuff` TEXT NOT NULL,
  `things` TEXT NOT NULL,
  `things__for__0____1` TEXT AS (json_extract(`things`,'$.for[0]."1"'))
);

CREATE INDEX `meta_spend` ON `meta` (`spend`);

CREATE UNIQUE INDEX `meta_name` ON `meta` (`name`);
""")

    def test_modify(self):

        ddl = TABLE(
            migration={
                "name": "good",
                "schema": "dreaming"
            },
            definition={
                "name": "evil",
                "schema": "scheming",
                "fields": Meta.thy().define()["fields"],
                "index": Meta.thy().define()["index"],
                "unique": Meta.thy().define()["unique"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `scheming`.`evil` RENAME TO `_old_evil`;

DROP INDEX `scheming`.`evil_spend`;

DROP INDEX `scheming`.`evil_name`;

CREATE TABLE IF NOT EXISTS `dreaming`.`good` (
  `id` INTEGER PRIMARY KEY,
  `name` TEXT NOT NULL,
  `flag` INTEGER,
  `spend` REAL,
  `people` TEXT NOT NULL,
  `stuff` TEXT NOT NULL,
  `things` TEXT NOT NULL,
  `things__for__0____1` TEXT AS (json_extract(`things`,'$.for[0]."1"'))
);

CREATE INDEX `dreaming`.`good_spend` ON `good` (`spend`);

CREATE UNIQUE INDEX `dreaming`.`good_name` ON `good` (`name`);

INSERT
INTO
  `dreaming`.`good`
  (
    `flag`,
    `id`,
    `name`,
    `people`,
    `spend`,
    `stuff`,
    `things`
  )
SELECT
  `flag` AS `flag`,
  `id` AS `id`,
  `name` AS `name`,
  `people` AS `people`,
  `spend` AS `spend`,
  `stuff` AS `stuff`,
  `things` AS `things`
FROM
  `scheming`.`_old_evil`;

DROP TABLE `scheming`.`_old_evil`;
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "add": Meta.thy().define()["fields"][-2:]
                }
            },
            definition=Simple.thy().define()
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql,"""ALTER TABLE `simple` RENAME TO `_old_simple`;

DROP INDEX `simple_name`;

CREATE TABLE IF NOT EXISTS `simple` (
  `id` INTEGER,
  `name` TEXT NOT NULL,
  `things` TEXT NOT NULL,
  `things__for__0____1` TEXT AS (json_extract(`things`,'$.for[0]."1"'))
);

CREATE UNIQUE INDEX `simple_name` ON `simple` (`name`);

INSERT
INTO
  `simple`
  (
    `id`,
    `name`
  )
SELECT
  `id` AS `id`,
  `name` AS `name`
FROM
  `_old_simple`;

DROP TABLE `_old_simple`;
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "change": {
                        "push": {
                            "name": "push",
                            "store": "pull"
                        },
                        "spend": {
                            "default": 1.25
                        },
                        "things": {
                            "store": "thingies"
                        }
                    }
                },
                "index": {
                    "remove": ["spend"]
                },
                "unique": {
                    "remove": ["name"]
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"],
                "index": Meta.thy().define()["index"],
                "unique": Meta.thy().define()["unique"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql,"""ALTER TABLE `yep` RENAME TO `_old_yep`;

DROP INDEX `yep_spend`;

DROP INDEX `yep_name`;

CREATE TABLE IF NOT EXISTS `yep` (
  `id` INTEGER PRIMARY KEY,
  `name` TEXT NOT NULL,
  `flag` INTEGER,
  `spend` REAL DEFAULT 1.25,
  `people` TEXT NOT NULL,
  `stuff` TEXT NOT NULL,
  `thingies` TEXT NOT NULL,
  `thingies__for__0____1` TEXT AS (json_extract(`thingies`,'$.for[0]."1"'))
);

INSERT
INTO
  `yep`
  (
    `flag`,
    `id`,
    `name`,
    `people`,
    `spend`,
    `stuff`,
    `thingies`
  )
SELECT
  `flag` AS `flag`,
  `id` AS `id`,
  `name` AS `name`,
  `people` AS `people`,
  `spend` AS `spend`,
  `stuff` AS `stuff`,
  `things` AS `thingies`
FROM
  `_old_yep`;

DROP TABLE `_old_yep`;
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "change": {
                        "push": {
                            "name": "push",
                            "store": "pull"
                        },
                        "spend": {
                            "default": 1.25
                        },
                        "things": {
                            "store": "thingies"
                        }
                    }
                },
                "index": {
                    "rename": {"spend": "spoon"}
                },
                "unique": {
                    "rename": {"name": "label"}
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"],
                "index": Meta.thy().define()["index"],
                "unique": Meta.thy().define()["unique"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `yep` RENAME TO `_old_yep`;

DROP INDEX `yep_spend`;

DROP INDEX `yep_name`;

CREATE TABLE IF NOT EXISTS `yep` (
  `id` INTEGER PRIMARY KEY,
  `name` TEXT NOT NULL,
  `flag` INTEGER,
  `spend` REAL DEFAULT 1.25,
  `people` TEXT NOT NULL,
  `stuff` TEXT NOT NULL,
  `thingies` TEXT NOT NULL,
  `thingies__for__0____1` TEXT AS (json_extract(`thingies`,'$.for[0]."1"'))
);

CREATE INDEX `yep_spoon` ON `yep` (`spend`);

CREATE UNIQUE INDEX `yep_label` ON `yep` (`name`);

INSERT
INTO
  `yep`
  (
    `flag`,
    `id`,
    `name`,
    `people`,
    `spend`,
    `stuff`,
    `thingies`
  )
SELECT
  `flag` AS `flag`,
  `id` AS `id`,
  `name` AS `name`,
  `people` AS `people`,
  `spend` AS `spend`,
  `stuff` AS `stuff`,
  `things` AS `thingies`
FROM
  `_old_yep`;

DROP TABLE `_old_yep`;
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "remove": [
                        "things",
                        "push"
                    ]
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `yep` RENAME TO `_old_yep`;

CREATE TABLE IF NOT EXISTS `yep` (
  `id` INTEGER PRIMARY KEY,
  `name` TEXT NOT NULL,
  `flag` INTEGER,
  `spend` REAL,
  `people` TEXT NOT NULL,
  `stuff` TEXT NOT NULL
);

INSERT
INTO
  `yep`
  (
    `flag`,
    `id`,
    `name`,
    `people`,
    `spend`,
    `stuff`
  )
SELECT
  `flag` AS `flag`,
  `id` AS `id`,
  `name` AS `name`,
  `people` AS `people`,
  `spend` AS `spend`,
  `stuff` AS `stuff`
FROM
  `_old_yep`;

DROP TABLE `_old_yep`;
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "fields": {
                    "remove": [
                        "things",
                        "push"
                    ]
                }
            },
            definition={
                "name": "yep",
                "fields": Meta.thy().define()["fields"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `yep` RENAME TO `_old_yep`;

CREATE TABLE IF NOT EXISTS `yep` (
  `id` INTEGER PRIMARY KEY,
  `name` TEXT NOT NULL,
  `flag` INTEGER,
  `spend` REAL,
  `people` TEXT NOT NULL,
  `stuff` TEXT NOT NULL
);

INSERT
INTO
  `yep`
  (
    `flag`,
    `id`,
    `name`,
    `people`,
    `spend`,
    `stuff`
  )
SELECT
  `flag` AS `flag`,
  `id` AS `id`,
  `name` AS `name`,
  `people` AS `people`,
  `spend` AS `spend`,
  `stuff` AS `stuff`
FROM
  `_old_yep`;

DROP TABLE `_old_yep`;
""")
        self.assertEqual(ddl.args, [])

        ddl = TABLE(
            migration={
                "index": {
                    "add": {
                        "flag": ["flag"]
                    },
                    "remove": [
                        "price"
                    ]
                },
                "unique": {
                    "add": {
                        "flag": ["flag"]
                    },
                    "remove": [
                        "name"
                    ]
                }
            },
            definition={
                "name": "yep",
                "index": Meta.thy().define()["index"],
                "unique": Meta.thy().define()["unique"]
            }
        )

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `yep` RENAME TO `_old_yep`;

DROP INDEX `yep_spend`;

DROP INDEX `yep_name`;

CREATE TABLE IF NOT EXISTS `yep` (
  """ """
);

CREATE INDEX `yep_flag` ON `yep` (`flag`);

CREATE INDEX `yep_spend` ON `yep` (`spend`);

CREATE UNIQUE INDEX `yep_flag` ON `yep` (`flag`);

INSERT
INTO
  `yep`
SELECT
FROM
  `_old_yep`;

DROP TABLE `_old_yep`;
""")
        self.assertEqual(ddl.args, [])

        ddl.generate(indent=2)
        self.assertEqual(ddl.sql, """ALTER TABLE `yep` RENAME TO `_old_yep`;

DROP INDEX `yep_spend`;

DROP INDEX `yep_name`;

CREATE TABLE IF NOT EXISTS `yep` (
  """ """
);

CREATE INDEX `yep_flag` ON `yep` (`flag`);

CREATE INDEX `yep_spend` ON `yep` (`spend`);

CREATE UNIQUE INDEX `yep_flag` ON `yep` (`flag`);

INSERT
INTO
  `yep`
SELECT
FROM
  `_old_yep`;

DROP TABLE `_old_yep`;
""")

        self.assertEqual(ddl.args, [])

    def test_drop(self):

        ddl = TABLE(
            definition={
                "name": "yep"
            }
        )

        ddl.generate()
        self.assertEqual(ddl.sql, """DROP TABLE IF EXISTS `yep`;\n""")
        self.assertEqual(ddl.args, [])
