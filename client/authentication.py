from network import ConnectionBlock, CreatePayloadData
from token_manager import load_token, write_token
from dotenv import load_dotenv
import struct
import json
import os


class Authentication():
    def __init__(self):
        self.token = load_token()

    def register(self, username, password):

        conn = ConnectionBlock()

        data = CreatePayloadData()

        payload = {
            "username": username,
            "password": password
        }

        # Follow sequence, must call create_payload first before invoking create_header. create_header is dependant on payload to identify it's payloads size for transmit
        data.create_payload(payload)
        data.create_header('AUTH/register', 'sdfasdf')

        conn.send_payload(data)

        # TODO:
        # 1. Process response from server
        # 2. Provide and update fresh token, and login

        # Data received from server;s response
        # 1. Fresh token
        # 2. GUI navigation

        # 1.
        # decoded response from bytes to string, then string to python object
        response = json.dumps(conn.response().decode())

        token = response['token']
        gui_path = response['gui_path']

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

        generated_token = conn.response()

        write_token(generated_token)

        conn.close()

        self.token = generated_token

        print(type(load_token()))


# Test
auth = Authentication()

auth.login('colleenross', 'ehehe')
