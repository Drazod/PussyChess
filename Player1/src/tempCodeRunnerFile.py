import socket
import threading
from const import *
from game import Game

class ChessServer:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5050  # Port number
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.game = Game()  # Initialize the game

    def handle_client(self, client_socket, addr):
        while True:
            try:
                data = client_socket.recv(1024).decode()  # Receive data from client
                if not data:
                    break
                # Process the move received from the client and update the game state
                # You need to implement this part based on your game logic
                # After updating the game state, send the updated game state to all clients
                for c in self.clients:
                    c.sendall(data.encode())
            except Exception as e:
                print(f"Error handling client {addr}: {e}")
                break

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print("Server started, waiting for connections...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Client {addr} connected")
            self.clients.append(client_socket)
            thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            thread.start()

if __name__ == "__main__":
    server = ChessServer()
    server.start()
