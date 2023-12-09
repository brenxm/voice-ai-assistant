import socket
import struct
import json


class CreatePayloadData():

    def create_header(self, method, token):
        METHOD_SIZE = 20  # Max of 20 characters
        TOKEN_SIZE = 40  # Max of 40 characters token
        PAYLOAD_BYTES_SIZE = 4  # In bytes for payload size (integer)
        HEADER_BYTES = 64  # Total and expected bytes of each request header

        # Pad and truncate to ensure fixed size
        method_fixed = method.ljust(METHOD_SIZE)[:METHOD_SIZE]
        token_fixed = token.ljust(TOKEN_SIZE)[:TOKEN_SIZE]

        # Header format must match the parsing header method on server end
        header_format = f'>{METHOD_SIZE}s{TOKEN_SIZE}sI'
        # The size parsed from payload is in bytes format
        header = struct.pack(header_format, method_fixed.encode(),token_fixed.encode(), len(self.payload))

        self.header = header

    def create_payload(self, payload):
        payload_str = json.dumps(payload)
        self.payload = payload_str.encode()


class ConnectionBlock():
    def __init__(self, ip='10.0.0.164', port=5000):
        self.client = self._connect_to_server(ip, port)

    def send_payload(self, data: CreatePayloadData):
        self.client.sendall(data.header)
        self.client.sendall(data.payload)
        print('payload sent')

        # Blocking, wait for servers response
        response = self.response()

    def _connect_to_server(self, server_ip, server_port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, server_port))
        print(f'established connection')

        return client

    def response(self):
        # TODO: Come up with strucutre on how server sends data back
        # etc: like payload size, type of data received etc
        pass


# Test
conn = ConnectionBlock()

data = CreatePayloadData()

payload = {
    'username': "colleenross",
    'password': 'ehehe'
}
data.create_payload(payload)
data.create_header('AUTH/registration', '23434343344')

conn.send_payload(data)
