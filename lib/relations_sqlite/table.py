"""–
Module for Column DDL
"""

# pylint: disable=unused-argument

import relations_sql
import relations_sqlite


class TABLE(relations_sqlite.DDL, relations_sql.TABLE):
    """
    TABLE DDL
    """

    NAME = relations_sqlite.TABLE_NAME
    COLUMN = relations_sqlite.COLUMN
    INDEX = relations_sqlite.INDEX
    UNIQUE = relations_sqlite.UNIQUE
    INSERT = relations_sqlite.INSERT
    SELECT = relations_sqlite.SELECT

    INDEXES = False

    def name(self, state="migration", prefix=''):
        """
        Generate a quoted name, with table as the default
        """

        if isinstance(state, str):
            state = {
                "name": state,
                "schema": state
            }

        store = prefix + (self.definition if state["name"] == "definition" or "store" not in self.migration else self.migration)["store"]
        schema = (self.definition if state["schema"] == "definition" else self.migration).get("schema")

        table = self.NAME(store, schema=schema)

        table.generate()

        return table.sql

    def modify(self, indent=0, count=0, pad=' ', **kwargs): # pylint: disable=too-many-locals,too-many-branches
        """
        MODIFY DLL
        """

        sql = [f"""ALTER TABLE {self.name(state='definition')} RENAME TO {self.name(state='definition', prefix='_old_')}"""]

        migration = {
            "store": self.migration.get("store", self.definition["store"]),
            "schema": self.migration.get("schema", self.definition.get("schema")),
            "fields": [],
            "index": {},
            "unique": {},
        }

        for attr in ["name", "store", "schema"]:
            value = self.migration.get(attr, self.definition.get(attr))
            if value is not None:
                migration[attr] = value

        renames = {}

        for field in self.definition.get("fields", []):
            if field.get("inject") or field["name"] in self.migration.get("fields", {}).get("remove", []):
                continue
            if field["name"] in self.migration.get("fields", {}).get("change", {}):
                migration["fields"].append({**field, **self.migration["fields"]["change"][field["name"]]})
                renames[self.migration["fields"]["change"][field["name"]].get("store", field["store"])] = field["store"]
            else:
                migration["fields"].append(field)
                renames[field["store"]] = field["store"]

        for field in self.migration.get("fields", {}).get("add", []):
            if field.get("inject"):
                continue
            migration["fields"].append(field)

        table = {
            "name": self.definition["store"],
            "schema": self.definition.get("schema")
        }

        indexes = []

        for index in self.definition.get("index", {}):
            indexes.append(self.INDEX(definition={
                "name": index,
                "columns": self.definition["index"][index],
                "table": table
            }))
            if index in self.migration.get("index", {}).get("remove", []):
                continue
            if index in self.migration.get("index", {}).get("rename", {}):
                migration["index"][self.migration["index"]["rename"][index]] = self.definition["index"][index]
            else:
                migration["index"][index] = self.definition["index"][index]

        migration["index"].update(self.migration.get("index", {}).get("add", {}))

        for index in self.definition.get("unique", {}):
            indexes.append(self.UNIQUE(definition={
                "name": index,
                "columns": self.definition["unique"][index],
                "table": table
            }))
            if index in self.migration.get("unique", {}).get("remove", []):
                continue
            if index in self.migration.get("unique", {}).get("rename", {}):
                migration["unique"][self.migration["unique"]["rename"][index]] = self.definition["unique"][index]
            else:
                migration["unique"][index] = self.definition["unique"][index]

        migration["unique"].update(self.migration.get("unique", {}).get("add", {}))

        current = pad * (count * indent)
        delimitter = f";\n\n{current}"

        for index in indexes:
            index.generate()
            sql.append(index.sql)

        ddl = self.__class__(migration)
        ddl.generate(indent=indent, count=count, pad=pad, **kwargs)
        sql.append(ddl.sql[:-2])

        query = self.INSERT(
            self.NAME(ddl.migration["store"], schema=ddl.migration.get("schema")),
            SELECT=self.SELECT(FIELDS=renames).FROM(relations_sql.SQL(self.name(state='definition', prefix='_old_')))
        )

        query.generate(indent, count, pad, **kwargs)
        sql.append(query.sql)

        sql.append(f"""DROP TABLE {self.name(state='definition', prefix='_old_')}""")

        self.sql = f"{delimitter.join(sql)};\n"
