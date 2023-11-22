import socket

class ConnectionBlock():
    def __init__(self):
        self.client = self._connect_to_server('10.0.0.164', 5000)
        
    def send_payload(self, payload_obj):
        # Sends metadata first
        # then send payload
        self.client.sendall(payload_obj['metadata'])
        self.client.sendall(payload_obj['payload'])


    def clear_payload(self):
        pass

    def disconnect(self):
        self.client.close()

    def _connect_to_server(self, server_ip, server_port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, server_port))
        print(f'established connection')

        return client
