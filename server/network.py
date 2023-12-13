import struct
import socket
from time import sleep

def send_response(client_socket: socket.socket, data: object):
    '''
    Send a response from server to client. Returns None value

    Parameters:
    client_socket (socket): Reference or connection of the client
    data (object): A fixed object schema to be sent to the client as response

    Returns:
    None
    '''
    print(f'Header size must be 24, the header size is:{len(data["header"])}')
    client_socket.sendall(data["header"])
    client_socket.sendall(data["payload"])

    print('Successfully sent response from server to client')


def create_header(method: str, payload: bytes):
    '''
    Create a header using struct module, returns the header in byte form (ready for network transmission)

    Parameters:
    method (str): The method initially used from the client
    payload (bytes): Payload to be sent back to the client

    Returns:
    bytes (packed struct): The header created
    '''

    if not isinstance(payload, bytes):
        raise ValueError(
            f'Argument payload must be in bytes format, instead {type(payload.__name__)} is given.')

    METHOD_SIZE = 20
    PAYLOAD_BYTES_SIZE = 4  # Do not use in this method, for documentation purposes only
    TOTAL_HEADER_BYTES = 24  # Do not use in this method, for documentation purposes only

    header_format = f'>{METHOD_SIZE}sI'

    # Pad and concat the method to ensure same size
    method_fixed = method.ljust(METHOD_SIZE)[:METHOD_SIZE]

    packed_header = struct.pack(
        header_format, method_fixed.encode(), len(payload))

    return packed_header
