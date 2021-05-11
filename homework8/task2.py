import sqlite3


class TableData:
    """
    Class TableData implements Collection protocol for a given database.
    """

    def __init__(self, database_name, table_name):
        """
        Creates attributes associated with the class.

        :type database_name: str
        :param database_name: name of the database

        :type table_name: str
        :param table_name: name of the database table
        """

        self.database_name = database_name
        self.table_name = table_name

        self.__connection = sqlite3.connect(self.database_name)

    def __getitem__(self, item):
        """
        Return the table item with an index key.

        :type item: str
        :param item: primary key

        :return: singe data row for a given primary key
        :rtype: tuple | None
        """

        cur = self.__connection.cursor()
        cur.execute(
            'SELECT * FROM "{}" WHERE name = "{}"'.format(self.table_name, item)
        )
        return cur.fetchone()

    def __len__(self):
        """
        Return the current amount of rows in the table.

        :return: current amount of rows in the table
        :rtype: int
        """

        cur = self.__connection.cursor()
        cur.execute("SELECT COUNT(*) FROM {}".format(self.table_name))
        return cur.fetchone()[0]

    def __iter__(self):
        """
        Return object itself for an iteration.

        :return: TableData object
        :rtype: TableData
        """
        self.__iter_cursor = self.__connection.cursor().execute(
            "SELECT * FROM {}".format(self.table_name)
        )
        return self

    def __next__(self):
        """
        Return row from the table until records are exhausted.

        :return: row from the table
        :rtype: tuple
        """
        while row := self.__iter_cursor.fetchone():
            return row
        raise StopIteration

    def __contains__(self, item):
        """
        Return True if item is in table.

        :type item: str | int
        :param item: value to search in table

        :return: True if item is in table
        """
        for i in self:
            if item in i:
                return True
        return False
