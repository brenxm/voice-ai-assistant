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

        authenticate_request(data)


@on_thread
def handle_request(client_socket: socket, message):
    decoded_message = message.decode()
    print(decoded_message)
    client_socket.sendall(b'received your message. bye!')


@on_thread
def authenticate_request(data):
    authentication.add(data)

def send_response(client_socket: socket, data: object):
    # Data object schema for data to be sent
        # header: packed struct format
        # payload: bytes

    client_socket.sendall(data["header"])
    client_socket.sendall(data["payload"])

    # Close client
    client_socket.close()

    print('Successfully sent response from server to client')

def create_header(method: str, payload: bytes):
    # payload argument must be in bytes format

    if not isinstance(payload, bytes):
        raise ValueError(f'Argument payload must be in bytes format, instead {type(payload.__name__)} is given.')
    
    METHOD_SIZE = 20
    PAYLOAD_BYTES_SIZE = 4 # Do not use in this method, for documentation purposes only
    TOTAL_HEADER_BYTES = 64 # Do not use in this method, for documentation purposes only

    header_format = f'>{METHOD_SIZE}sI'

    # Pad and concat the method to ensure same size
    method_fixed = method.ljust(METHOD_SIZE)[:METHOD_SIZE]

    packed_header = struct.pack(header_format, method_fixed.encode(), len(payload))

    return packed_header

if __name__ == '__main__':
    start_server('10.0.0.166', 5000)
