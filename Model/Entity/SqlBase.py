import sqlite3


class SqlBase():
    def __init__(self, path_to_container=""):
        self.path_to_container=path_to_container

    def conn(self):
        try:
            self.__conn = sqlite3.connect(self.path_to_container)
            self.__c = self.__conn.cursor()
        except:
            return

    def set_table(self, name=""):
        try:
            self.conn()
            self.__c.execute('CREATE TABLE ' + name + '(id TEXT, artist TEXT, title TEXT, album TEXT,like TEXT)')
        except:
            return
        finally:
            self.__conn.close()

    def set_col(self, name='', name_table=''):
        try:
            self.conn()
            self.__c.execute("ALTER TABLE '%s' ADD COLUMN '%s'" % (name_table, name))
        except:
            return
        finally:
            self.__conn.close()

    def update_cell(self, name_table='', cell='', value='', val='', title=''):
        try:
            self.conn()
            purchases = (value, title)
            self.__c.execute('Update %s SET %s=? WHERE %s=?' % (name_table, cell, val), purchases)
            self.__conn.commit()
        except:
            return
        finally:
            self.__conn.close()

    def set_cell(self, name_table='', idd='', artist='', title='', album='', like=''):
        try:
            self.conn()
            self.__c.execute("SELECT * FROM '%s'" % name_table)
        except:
            return

        for row in self.__c:
            for index in row:
                if index.startswith(title):
                    return
        try:
            purchases = (idd, artist, title, album, like)
            self.__c.execute("INSERT INTO musiccc (id, artist, title, album,like) VALUES(?,?,?,?,?)", purchases)
            self.__conn.commit()
        except:
            return
        finally:
            self.__conn.close()

    def get_columns(self, name_table='', cell='', value=''):
        array = []
        self.conn()
        if value != '':
            self.__c.execute(
                "SELECT id, artist, title, album,like FROM '%s' WHere %s = '%s'" % (name_table, cell, value))
            for row in self.__c:
                column = []
                for i in row:
                    column.append(i)
                array.append(column)
            return array
        try:
            self.__c.execute("SELECT * FROM '%s'" % name_table)
        except:
            return

        for row in self.__c:
            column = []
            for index in row:
                column.append(index)
            array.append(column)
        self.__conn.close()
        return array


if __name__ == "__main__":
    table = 'mus'
    con = SqlBase("t45.db")
    con.set_table(table)
    con.set_col("artist", table)
    con.set_col("title", table)
    con.set_col("album", table)
    con.set_col("like", table)
    con.set_cell(table, "4", "RHCP", "Californication", "Californication", "1")
    con.set_cell(table, "4", "RHCP", "Californicationnnnn", "Californication", "1")
    con.set_cell(table, "2", "RHCP", "Ca", "Californication", "1")
    con.set_cell(table, "4", "RHCP", "Universe", "Californication", "0")
    con.update_cell(table, "artist", "Motley Crue", "Ca")
    con.update_cell(table, "like", "5", "Californication")

