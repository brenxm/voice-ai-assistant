import sqlite3
import uuid
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

    # Login
    # 1. Check if in the system
    # 2. Provide fresh token
    def login(self, username, password):
        user_data = self.db_cursor.execute(
            'SELECT password_hash, salt FROM users WHRE username = ?', (username,)).fetchone()

        if user_data:
            stored_hash = user_data[0]
            # Verify the password
            if bcrypt.checkpw(password.encode(), stored_hash):
                # Password is correct; geneerate and return a token
                token = str(uuid.uuid4())
                print(f'Login succesful. Tken: {token}')
                return token

            else:
                # Password is incorrect
                print('Invalid password.')
                return None

        else:
            # User does not exist
            print('User not found.')
            return None

    def grant_token(self, user_id):
        pass
        

    def verify_token(self):
        pass

    def show_users(self):
        res = self.db_conn.execute('SELECT * FROM users')
        print(res.fetchall())


auth = Authentication()
auth.register_user('colleenross', 'heheh')
