import socket
import threading

class ChessServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            self.clients.append(client_socket)

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                self.broadcast(data)
            except ConnectionResetError:
                break
        client_socket.close()

    def broadcast(self, data):
        for client_socket in self.clients:
            client_socket.sendall(data)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5555
    server = ChessServer(HOST, PORT)
    server.start()
