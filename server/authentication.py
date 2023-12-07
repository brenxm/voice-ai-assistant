from datetime import datetime, timedelta
from dotenv import load_dotenv
import sqlite3
import bcrypt
import jwt
import os


class Authentication:
    def __init__(self):
        self.db_conn = sqlite3.connect('credentials.db')
        self.db_cursor = self.db_conn.cursor()
        self.secret_key = self.load_jwt_secret_key()

        # Ensure to initialize table for users
        self.db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT, 
            password_hash TEXT, salt TEXT)''')

        # Ensure to initialize table for tokens
        self.db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS tokens (
            token_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT,
            token TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )'''
        )

    def register_user(self, username, password):
        # TODO: Apply username and password input validations
        
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)

        # Get existing usernames
        res = self.db_conn.execute('SELECT username FROM users')
        usernames = [tple[0] for tple in res.fetchall()]

        # Verify if the username is already taken
        if username in usernames:
            print(f'Username {username} already existing!')
            return False

        # Add user to the users table in credentials database
        self.db_cursor.execute(
            '''INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)''', (username, password_hash, salt))

        user_id = self.db_cursor.lastrowid

        # Generate fresh token
        token = self.gen_token(user_id)

        # Create a token in the tokens table in credentials database
        self.db_cursor.execute(
            '''INSERT INTO tokens (user_id, token) VALUES (?, ?)''', (user_id, token)
        )

        # Commit all action to database
        self.db_conn.commit()
        print('Succesfully registered in users and tokens')

    def login(self, username, password):
        user_id = self.verify_user(username, password)

        if not user_id:
            print(f'Cannot identify username/password')
            return

        self.reissue_token(user_id)

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

            if bcrypt.checkpw(password.encode(), stored_pw):
                print('Password match.')
                return user_id

        print('Password didn\'t match')
        return False

    def gen_token(self, user_id):
        hex_key = os.getenv('JWT_SECRET_HEX_KEY')

        print(hex_key)
        secret_key = bytes.fromhex(hex_key)

        expiry = datetime.now() + timedelta(days=5)
        expiry_timestamp = int(expiry.timestamp())

        payload = {
            'user_id': user_id,
            'exp': expiry_timestamp
        }

        token = jwt.encode(payload, secret_key, algorithm='HS256')

        return token

    def reissue_token(self, user_id):

        # Correct expiry handling
        expiry = datetime.now() + timedelta(days=5)
        expiry_timestamp = int(expiry.timestamp())

        payload = {
            'user_id': user_id,
            'exp': expiry_timestamp  # Using standard JWT expiry field
        }

        token = jwt.encode(payload, self.secret_key, algorithm='HS256')

        try:
            self.db_cursor.execute(
                'UPDATE tokens SET token = ? WHERE user_id = ?', (
                    token, user_id)
            )
            print('succesfully issuded a token')
            self.db_conn.commit()

        except Exception as e:
            # Handle or log the exception
            print(f"Database error: {e}")
            self.db_conn.rollback()

    def verify_token(self, user_id):
        try:
            data = self.db_cursor.execute(
                'SELECT token FROM tokens WHERE user_id = ?', (user_id,)
            ).fetchone()

            print(data)
            # If no token for user
            if not data:
                print('No token registed for this user')
                return

            if data[0]:
                payload = jwt.decode(
                    data[0], self.secret_key, algorithms=['HS256'])
                stored_exp = payload['exp']
                time_now = datetime.now().timestamp()

                print(
                    f'the timestamp now is {time_now} and the token expiration date is {stored_exp}')
                # Check if stored token is expired
                if stored_exp > time_now:
                    print('Token is good')
                    return True
                else:
                    print('Token is expired')
                    return False

            else:
                print(f'This token has been revoked')
                return False
        except Exception as e:
            print(
                f'Error during attempt to verify token of user_id: {user_id}: {e}')
            return False

    def delete_user(self, user_id):
        try:
            self.db_cursor.execute(
                'SELECT * FROM users WHERE user_id = ?', (user_id,)
            )

            if self.db_cursor.fetchone():
                self.db_cursor.execute(
                    'DELETE FROM users WHERE user_id =?', (user_id,)
                )

                self.db_cursor.execute(
                    'DELETE FROM tokens WHERE user_id =?', (user_id,)
                )

                self.db_conn.commit()
                print(f'succesfully deleted user: {user_id}')

            else:
                print('User is not existing')

        except Exception as e:
            print(f'Error during attempt to delete user_id: {user_id}: {e}')
            return False

    def revoke_token(self, user_id):
        try:
            self.db_cursor.execute(
                'UPDATE tokens SET token = ? WHERE user_id = ?', (
                    None, user_id)
            )

            self.db_conn.commit()
        except Exception as e:
            print(f'Error: {e}')

    def show_users(self):
        res = self.db_conn.execute('SELECT * FROM users')
        print(res.fetchall())

    def show_tokens(self):
        res = self.db_conn.execute('SELECT * FROM tokens')
        print(res.fetchall())

    def load_jwt_secret_key(self):
        load_dotenv()
        hex_key = os.getenv('JWT_SECRET_HEX_KEY')
        secret_key = bytes.fromhex(hex_key)
        return secret_key


