import sqlite3
from sqlite3 import Error


class DatabaseManagement:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None
        self.connect_to_database()
        self.create_table()

    def connect_to_database(self):
        try:
            self.conn = sqlite3.connect(self.database_location, check_same_thread=False)
        except Error as e:
            print(e)

    def create_tables(self):
        try:
            self.conn.cursor().execute('''''')
        except Error as e:
            print(e)
