import sqlite3
import bcrypt


class Authentication:
    def __init__(self):
        self.db_conn = sqlite3.connect('database.db')
        self.db_cursor = self.db_conn.cursor()

        self.db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users (username TEXT, password_hash TEXT, salt TEXT)''')

    def register_user(self, username, password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)

        # Get existing usernames
        res = self.db_conn.execute('SELECT username FROM users')
        usernames = [tple[0] for tple in res.fetchall()]

        # Verify if the username is already taken
        if username in usernames:
            print(f'Username {username} already existing!')
            return False

        self.db_cursor.execute(
            'INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)', (username, password_hash, salt))

        self.db_conn.commit()

    def show_users(self):
        res = self.db_conn.execute('SELECT * FROM users')
        print(res.fetchall())


auth = Authentication()
auth.register_user('colleenross', 'heheh')
