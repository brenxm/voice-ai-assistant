from utils.thread_manager import on_thread
from time import sleep
import sys
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

        payload = client_socket.recv(payload_size)

        data = {
            'payload': payload,
            'header': {
                "method": method,
                "token": token
            },
            'client_socket': client_socket
        }

        router(data)


@on_thread
def handle_request(client_socket, message):
    decoded_message = message.decode()
    print(decoded_message)
    client_socket.sendall(b'received your message. bye!')

@on_thread
def router(data):

    method = data['header']['method']

    method_type = method.split('/')[0]
    method_path = method.split('/')[1]

    print(f"method type: {method_type}\nmethod_path: {method_path}")
    

if __name__ == '__main__':
    start_server('10.0.0.164', 5000)
