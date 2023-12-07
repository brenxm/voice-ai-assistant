import socket
import struct
import json


class ConnectionBlock():
    def __init__(self, ip='10.0.0.164', port=5000):
        self.client = self._connect_to_server(ip, port)

    def send_payload(self, header, payload):
        # Check if payload is formatted to string to be sent
        if not isinstance(payload, bytes):
            payload = json.dumps(payload).encode()

        self.client.sendall(payload)

    def disconnect(self):
        self.client.close()

    def _connect_to_server(self, server_ip, server_port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, server_port))
        print(f'established connection')

        return client

    def response(self):
        pass

    class CreatePayloadData():

        def create_header(self, method, token, payload_bytes_size):
            METHOD_SIZE = 20  # Max of 20 characters
            TOKEN_SIZE = 40  # Max of 40 characters token
            PAYLOAD_BYTES_SIZE = 4  # In bytes for payload size (integer)
            HEADER_BYTES = 64 # Total and expected bytes of each request header

            # Pad and truncate to ensure fixed size
            method_fixed = method.ljust(METHOD_SIZE)[:METHOD_SIZE]
            token_fixed = token.ljust(TOKEN_SIZE)[:TOKEN_SIZE]

            header_format = f'>{METHOD_SIZE}s{TOKEN_SIZE}sI'

            header = struct.pack(header_format, method_fixed.encode(),
                                token_fixed.encode(), payload_bytes_size)
            
            self.header = header


        def create_payload(self, payload):
            pass
        

        

        
