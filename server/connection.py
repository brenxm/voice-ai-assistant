from utils.thread_manager import on_thread
from authentication import authentication
import json
import struct
import socket


@on_thread
def start_server(ip_address, port, max_request=10):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_address, port))

    server.listen(max_request)

    print(f'Server started on {ip_address} and port {port}')

    while True:
        # Each client request (chunks/single)
        client_socket, addr = server.accept()

        # Parse header
        header = client_socket.recv(64)

        # Header format must match the senders format
        METHOD_SIZE = 20
        TOKEN_SIZE = 40
        header_format = f'>{METHOD_SIZE}s{TOKEN_SIZE}sI'

        unpacked_header = struct.unpack(header_format, header)

        method, token, payload_size = unpacked_header

        method = method.decode().strip()
        token = token.decode().strip()

        # Receives payload
        payload = client_socket.recv(payload_size)
        payload = json.loads(payload)

        data = {
            'payload': payload,
            'header': {
                "method": method,
                "token": token
            },
            'client_socket': client_socket,
        }

        authenticate_request(data)\



@on_thread
def handle_request(client_socket: socket, message):
    decoded_message = message.decode()
    print(decoded_message)
    client_socket.sendall(b'received your message. bye!')


@on_thread
def authenticate_request(data):
    authentication.add(data)
