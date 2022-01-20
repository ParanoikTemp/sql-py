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

    def delete_table(self, table_name=''):
        if not table_name:
            table_name = self.table
        self.cur.execute(f'''DROP TABLE {table_name};''')
        self.con.commit()

    def db_save(self):
        self.con.commit()

    def rename_table(self, new_name):
        old_name = self.table
        self.cur.execute(f"SP_RENAME '{old_name}','{new_name}';")

    def select(self, *names, _or=False, **cond):
        if cond:
            where = []
            for i in cond.items():
                if type(i[1]) is int or type(i[1]) is float:
                    where.append(i[0] + ' == ' + str(i[1]))
                else:
                    where.append(i[0] + ' == "' + i[1] + '"')
            word = " AND " if not _or else " OR "
            answer = self.cur.execute(f'''SELECT {", ".join(names)} FROM {self.table} WHERE {word.join(where)};''').fetchall()
        else:
            answer = self.cur.execute(f'''SELECT {", ".join(names)} FROM {self.table}''').fetchall()
        return answer

    def select_special(self, *names, condition):
        answer = self.cur.execute(f'''SELECT {", ".join(names)} FROM {self.table} WHERE {"".join(condition)};''').fetchall()
        return answer






