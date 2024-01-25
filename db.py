import sqlite3


class DataLayer:
    """
    A class for interacting with a SQLite database.
    """

    def __init__(self, database_name):
        """
        Initialize the DataLayer with a SQLite database.

        :param database_name: The name of the SQLite database file.
        """
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        Create a table with the specified columns.

        :param table_name: The name of the table to create.
        :param columns: A list of column definitions for the table.
        """
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def __get_max_id(self, table_name):
        """
        Get the maximum ID value from a table.

        :param table_name: The name of the table to query.
        :return: The maximum ID value or None if the table is empty.
        """
        select_query = f"SELECT max(id) FROM {table_name}"
        self.cursor.execute(select_query)
        max_id = self.cursor.fetchall()[0][0]
        return max_id

    def insert_data(self, table_name, data):
        """
        Insert data into the specified table.

        :param table_name: The name of the table to insert data into.
        :param data: A list of data values to insert.
        """
        placeholders = ', '.join(['?'] * (len(data) + 1))
        id = self.__get_max_id(table_name)
        if id:
            id_list = [id + 1]
        else:
            id_list = [1]
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_query, id_list + data)
        self.conn.commit()

    def fetch_data(self, table_name, id: int):
        """
        Fetch data from the specified table by ID.

        :param table_name: The name of the table to fetch data from.
        :param id: The ID of the record to retrieve.
        :return: A list containing the fetched data or an empty list if no data is found.
        """
        select_query = f"SELECT * FROM {table_name} WHERE id = ?"
        self.cursor.execute(select_query, (id,))
        data = self.cursor.fetchall()
        return data

    def close_connection(self):
        """
        Close the database connection.
        """
        self.cursor.close()
        self.conn.close()
