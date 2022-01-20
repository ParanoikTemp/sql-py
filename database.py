import sqlite3


class Database:
    def __init__(self, sql_file, autosave=False):
        self.con = sqlite3.connect(sql_file)
        self.cur = self.con.cursor()
        self.table = None
        self.autosave = autosave

    def command(self, cmd):
        answer = self.cur.execute(cmd)
        return answer

    def set_table(self, table):
        self.table = table

    def add_table(self, table_name):
        self.cur.execute(f'''DROP TABLE IF EXISTS {table_name};
CREATE TABLE {table_name}
(sqlpynull text NOT NULL DEFAULT "0");''')
        self.con.commit()

    def create_table(self, table_name):
            self.cur.execute(f'''DROP TABLE IF EXISTS {table_name};
    CREATE TABLE {table_name}
    (sqlpynull text NOT NULL DEFAULT "0");''')
            self.con.commit()

    def delete_table(self, table_name=''):
        if not table_name:
            table_name = self.table
        self.cur.execute(f'''DROP TABLE {table_name};''')
        self.con.commit()

    def drop_table(self, table_name=''):
        if not table_name:
            table_name = self.table
        self.cur.execute(f'''DROP TABLE {table_name};''')
        self.con.commit()

    def db_save(self):
        self.con.commit()

    def rename_table(self, new_name):
        old_name = self.table
        self.cur.execute(f"SP_RENAME '{old_name}','{new_name}';")
        self.table = new_name

    def select(self, *names, _or=False, where=None, **cond):
        if cond and not where:
            where = []
            for i in cond.items():
                if type(i[1]) is int or type(i[1]) is float:
                    where.append(i[0] + ' == ' + str(i[1]))
                else:
                    where.append(i[0] + ' == "' + i[1] + '"')
            word = " AND " if not _or else " OR "
            answer = self.cur.execute(
                f'''SELECT {", ".join(names)} FROM {self.table} WHERE {word.join(where)};''').fetchall()
        elif where:
            answer = self.cur.execute(
                f'''SELECT {", ".join(names)} FROM {self.table} WHERE {where};''').fetchall()
        else:
            answer = self.cur.execute(f'''SELECT {", ".join(names)} FROM {self.table}''').fetchall()
        return answer

    def search(self, *names, _or=False, where=None, **cond):
        if cond and not where:
            where = []
            for i in cond.items():
                if type(i[1]) is int or type(i[1]) is float:
                    where.append(i[0] + ' == ' + str(i[1]))
                else:
                    where.append(i[0] + ' == "' + i[1] + '"')
            word = " AND " if not _or else " OR "
            answer = self.cur.execute(
                f'''SELECT {", ".join(names)} FROM {self.table} WHERE {word.join(where)};''').fetchall()
        elif where:
            answer = self.cur.execute(
                f'''SELECT {", ".join(names)} FROM {self.table} WHERE {where};''').fetchall()
        else:
            answer = self.cur.execute(f'''SELECT {", ".join(names)} FROM {self.table}''').fetchall()
        return answer

    def add(self, **items):
        it = []
        for i in items.values():
            if type(i) is int or type(i) is float:
                it.append(str(i))
            else:
                it.append('"' + i + '"')
        self.cur.execute(f'''INSERT INTO {self.table}({", ".join(items.keys())}) VALUES({", ".join(it)});''')
        if self.autosave:
            self.con.commit()

    def insert(self, **items):
        it = []
        for i in items.values():
            if type(i) is int or type(i) is float:
                it.append(str(i))
            else:
                it.append('"' + i + '"')
        self.cur.execute(f'''INSERT INTO {self.table}({", ".join(items.keys())}) VALUES({", ".join(it)});''')
        if self.autosave:
            self.con.commit()

    @staticmethod
    def where(_or=False, **cond):
        where = []
        for i in cond.items():
            if type(i[1]) is int or type(i[1]) is float:
                where.append(i[0] + ' == ' + str(i[1]))
            else:
                where.append(i[0] + ' == "' + i[1] + '"')
        word = " AND " if not _or else " OR "
        return word.join(where)

    def update(self, where=None, **items):
        val = []
        for i in items.items():
            if type(i[1]) is int or type(i[1]) is float:
                where.append(i[0] + ' = ' + str(i[1]))
            else:
                where.append(i[0] + ' = "' + i[1] + '"')
        if where:
            self.cur.execute(f'''UPDATE {self.table} SET {", ".join(val)} WHERE {where};''')
        else:
            self.cur.execute(f'''UPDATE {self.table} SET {", ".join(val)};''')
        if self.autosave:
            self.con.commit()

    def edit(self, where=None, **items):
        val = []
        for i in items.items():
            if type(i[1]) is int or type(i[1]) is float:
                where.append(i[0] + ' = ' + str(i[1]))
            else:
                where.append(i[0] + ' = "' + i[1] + '"')
        if where:
            self.cur.execute(f'''UPDATE {self.table} SET {", ".join(val)} WHERE {where};''')
        else:
            self.cur.execute(f'''UPDATE {self.table} SET {", ".join(val)};''')
        if self.autosave:
            self.con.commit()

    def delete(self, _or=False, where=None, **cond):
        if not where:
            where = []
            for i in cond.items():
                if type(i[1]) is int or type(i[1]) is float:
                    where.append(i[0] + ' == ' + str(i[1]))
                else:
                    where.append(i[0] + ' == "' + i[1] + '"')
            word = " AND " if not _or else " OR "
            self.cur.execute(f'''DELETE FROM {self.table} WHERE {word.join(where)};''')
        else:
            self.cur.execute(f'''DELETE FROM {self.table} WHERE {where};''')
        if self.autosave:
            self.con.commit()

    def remove(self, _or=False, where=None, **cond):
        if not where:
            where = []
            for i in cond.items():
                if type(i[1]) is int or type(i[1]) is float:
                    where.append(i[0] + ' == ' + str(i[1]))
                else:
                    where.append(i[0] + ' == "' + i[1] + '"')
            word = " AND " if not _or else " OR "
            self.cur.execute(f'''DELETE FROM {self.table} WHERE {word.join(where)};''')
        else:
            self.cur.execute(f'''DELETE FROM {self.table} WHERE {where};''')
        if self.autosave:
            self.con.commit()
