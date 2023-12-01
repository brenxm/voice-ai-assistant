from datetime import datetime, timedelta
import sqlite3
import jwt
import bcrypt


class Authentication:
    def __init__(self):
        self.db_conn = sqlite3.connect('database.db')
        self.db_cursor = self.db_conn.cursor()

        # Ensure to initialize table for users
        self.db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY, 
            username TEXT, 
            password_hash TEXT, salt TEXT)''')

        # Ensure to initialize table for tokens
        self.db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS tokens (
            token_id INT PRIMARY KEY,
            user_id INT,
            token TEXT,
            expiry TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )'''
        )

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
            '''INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)''', (username, password_hash, salt))

        self.db_conn.commit()

    def login(self, username, password):
        user_id = self.verify_user(username, password)

        if not user_id:
            print(f'Cannot identify username/password')
            return

        self.grant_token(user_id)
        print('Succesfully logged in.')

    def verify_user(self, username, password):
        '''
        username: str -
        password: str - (raw str)
        return False (bool) / user_id (str)
        '''

        user_data = self.db_cursor.execute(
            'SELECT password_hash, user_id FROM users WHERE username = ?', (username,)).fetchone()
        if user_data:
            stored_pw = user_data[0]
            user_id = user_data[1]

            if bcrypt.chekpw(password.encode(), stored_pw):
                print('Password match.')
                return user_id

        return False

    def grant_token(self, user_id):
        expiry = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + timedelta(days=5)
        self.db_cursor.execute(
            'UPDATE tokens SET expiry = ? WHERE user_id = ?', (expiry, user_id)
        )
        self.db_conn.commit()

    def verify_token(self, user_id):
        try:
            data = self.db_cursor.execute(
                'SELECT expiry FROM tokens WHERE user_id = ?', (user_id,)
            ).fetchone()

            if data and data[0]:
                datetime_obj = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')
                return datetime_obj < datetime.now()

            else:
                return False
        except Exception as e:
            print(
                f'Error during attempt to verify token of user_id: {user_id}: {e}')
            return False

    def delete_user(self, user_id):
        try:
            self.db_cursor.execute(
                'DELETE FROM users where id =?', (user_id,)
            )
            self.db_conn.commit()

        except Exception as e:
            print(f'Error during attempt to delete user_id: {user_id}: {e}')
            return False

    def revoke_token(self, user_id):
        try:
            self.db_cursor.execute(
                'UPDATE tokens SET expiry = ? WHERE user_id = ?', (
                    None, user_id)
            )

            self.db_conn.commit()
        except Exception as e:
            print(f'Error: {e}')

    def show_users(self):
        res = self.db_conn.execute('SELECT * FROM users')
        print(res.fetchall())


auth = Authentication()
auth.register_user('colleenross', 'heheh')
