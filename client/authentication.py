from network import ConnectionBlock, CreatePayloadData
from token_manager import load_token, write_token
from dotenv import load_dotenv
import json
import os


class Authentication():
    def __init__(self):
        self.token = load_token()
    # Login
    # Registration

    def register(self, username, password):

        conn = ConnectionBlock()

        data = CreatePayloadData()

        payload = {
            "username": username,
            "password": password
        }

        # Follow sequence, must call create_payload first before invoking create_header. create_header is dependant on payload to identify it's payloads size for transmit
        data.create_payload(payload)
        data.create_header('AUTH/register', self.token)

        conn.send_payload(data)

    def login(self, username, password):
        conn = ConnectionBlock()
        data = CreatePayloadData()

        payload = {
            'username': username,
            'password': password
        }

        data.create_payload(payload)
        data.create_header('AUTH/login', '232323232')

        conn.send_payload(data)

        print(conn.response())
        conn.close()

        print('Completed login')
       

# Test

auth = Authentication()

auth.login('colleenross', 'ehehe')



