from thread_manager import on_thread
import socket

@on_thread
def start_server(ip_address, port, max_request = 10):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_address, port))

    server.listen(max_request)

    print(f'Server started on {ip_address} and port {port}')

    while True:
        client_socket, addr = server.accept()

        message = client_socket.recv(1026)

        handle_request(client_socket, message)
        

@on_thread
def handle_request(client_socket, message):
    decoded_message = message.decode()
    print(decoded_message)
    client_socket.sendall(b'received your message. bye!')
