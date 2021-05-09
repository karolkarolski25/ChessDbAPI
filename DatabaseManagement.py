import sqlite3
from sqlite3 import Error
from datetime import datetime


class DatabaseManagement:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None
        self.connect_to_database()
        self.create_tables()

    @staticmethod
    def format_json(data):
        return [dict((data.description[i][0], value) for i, value in enumerate(row)) for row in
                data.fetchall()]

    def connect_to_database(self):
        try:
            self.conn = sqlite3.connect(self.connection_string, check_same_thread=False)
            self.conn.execute("PRAGMA foreign_keys = ON")
        except Error as e:
            print(e)

    def create_tables(self):
        try:
            self.conn.cursor().execute('''CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username varchar(255) NOT NULL UNIQUE, password_hash varchar(255) NOT NULL,
                        created_at varchar (255) NOT NULL, updated_at varchar (255) DEFAULT NULL);''')

            self.conn.cursor().execute('''CREATE TABLE IF NOT EXISTS Moves (move_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL, game_id INTEGER NOT NULL, move varchar(255) NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE ,
                        FOREIGN KEY (game_id) REFERENCES GamesPlayed (game_id) ON DELETE CASCADE );''')

            self.conn.cursor().execute('''CREATE TABLE IF NOT EXISTS GamesPlayed (game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user1_id INTEGER NOT NULL, user2_id INTEGER NOT NULL, winner_id INTEGER NOT NULL,
                        win_type varchar(255) NOT NULL, FOREIGN KEY (user1_id) REFERENCES Users(user_id) ON DELETE CASCADE,
                        FOREIGN KEY (user2_id) REFERENCES Users(user_id) ON DELETE CASCADE );''')

            self.conn.cursor().execute('''CREATE TABLE IF NOT EXISTS GameStatistics (statistic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        game_id INTEGER NOT NULL, FOREIGN KEY (game_id) REFERENCES GamesPlayed (game_id) ON DELETE CASCADE );''')

        except Error as e:
            print(e)

    def create_user(self, user_data):
        try:
            if not self.check_if_user_exists(user_data['username']):
                self.conn.cursor().execute('''INSERT INTO Users (username, password_hash, created_at) VALUES (?,?,?)''',
                                           (user_data['username'], user_data['password_hash'],
                                            str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))))
                self.conn.commit()

                return f"User {user_data['username']} successfully created", True
            else:
                return "User with given username already exists", False
        except Exception as e:
            if type(e) is Error:
                return f"Error occurred during creating new user: {e}", False
            if type(e) is KeyError:
                return "Not enough data provided", False

    def get_user(self, **kwargs):
        username = kwargs.get('username', None)
        details = kwargs.get('details', None)
        try:
            if not username:
                if details:
                    return self.format_json(self.conn.cursor().execute('SELECT * FROM Users'))
                else:
                    return self.format_json(self.conn.cursor().execute('SELECT user_id, username FROM Users'))
            else:
                return self.format_json(
                    self.conn.cursor().execute('SELECT * FROM Users WHERE username = ?', (username,)))

        except Error:
            return None

    def check_if_user_exists(self, username):
        return len(
            self.conn.cursor().execute('SELECT user_id FROM Users WHERE username = ?', (username,)).fetchall()) != 0

    def delete_user(self, username):
        if self.check_if_user_exists(username):
            self.conn.cursor().execute('DELETE FROM Users WHERE username = ?', (username,))
            self.conn.commit()
            return f"User {username} successfully deleted"
        else:
            return f"User {username} doesn't exist"

    def update_user(self, username, new_data):
        new_username_exists_in_database = False

        if 'username' in new_data:
            new_username_exists_in_database = self.check_if_user_exists(new_data['username'])

        if self.check_if_user_exists(username) and not new_username_exists_in_database:
            user = self.get_user(username=username)[0]
            try:
                for columng in new_data:
                    sql_update = "UPDATE Users SET {0} = '{1}' WHERE user_id = {2}".format(columng, new_data[columng],
                                                                                           user['user_id'])
                    self.conn.cursor().execute(sql_update)

                self.conn.cursor().execute('UPDATE Users SET updated_at = ? WHERE user_id = ?',
                                           (str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), user['user_id']))

                self.conn.commit()
                return True
            except Error:
                return False
        else:
            return False
