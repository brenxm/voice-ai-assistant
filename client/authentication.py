from network import ConnectionBlock
from dotenv import load_dotenv
import os

class Authentication():
    def __init__(self):
        self.token = self.load_token()
    # Login
    # Registration

    def register(self, username, password):
        
        conn = ConnectionBlock()

        payload = {
            "method": "AUTH/login",
            "token": self.token,
            "payload": {
                'username': username,
                'password': password
            }
        }

        conn.send_payload(payload)


    def load_token(self, token_file_name = 'token.env', root_folder = 'ai-assistant'):
        try:
            path = os.environ.get('LOCALAPPDATA')
            if not path:
                raise EnvironmentError('LOCALAPPDATA environment variable not found')
            
            root_path = os.path.join(path, root_folder)

            if not os.path.exists(root_path):
                raise FileNotFoundError(f"Root folder is not found at {root_path}")
            
            file_path = os.path.join(root_path, token_file_name)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f'Token file path is not found at {file_path}')
            
            load_dotenv(file_path)
            self.token = os.getenv('TOKEN')

            if not self.token:
                raise ValueError("Token not found in the environment variables")

        except FileNotFoundError as fnf_error:
            print(f'File Not Found Error: {fnf_error}')

        except EnvironmentError as env_error:
            print(f"Environemtn Error: {env_error}")

        except ValueError as val_error:
            print(f'Value Error: {val_error}')

        except Exception as e:
            print(f'Error: {e}')



