import pygame
import sys
import socket
import threading
from const import *
from game import Game
from square import Square
from move import Move
from flipbook import display_flipbook

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.font = pygame.font.SysFont(None, 30)  # Font for displaying alerts
        self.move = None
        self.client = None  # Client for multiplayer functionality
        self.player_vs_player = False
        self.radom = False

    def show_alert(self, message):
        alert_text = self.font.render(message, True, (255, 0, 0))
        alert_rect = alert_text.get_rect(center=(WIDTH // 2 + 300, HEIGHT // 2))  # Move the alert to the right by 50 pixels
        self.screen.blit(alert_text, alert_rect)

    def connect_to_server(self, host, port):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, port))
            print("Connected to server")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_move_to_server(self, move):
        if self.client:
            try:
                self.client.sendall(move.encode())  # Send move to the server
            except Exception as e:
                print(f"Error sending move to server: {e}")

    def receive_updates_from_server(self):
        while True:
            try:
                data = self.client.recv(1024).decode()  # Receive data from server (if any)
                if data:

                    # Extract move data from the received message
                    clicked_row = int(data[0])
                    clicked_col = int(data[1])
                    released_row = int(data[2])
                    released_col = int(data[3])
                    
                    # Perform the move on the game board
                    piece = self.game.board.squares[clicked_row][clicked_col].piece
                    board = self.game.board
                    board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                    initial = Square(clicked_row, clicked_col)
                    final = Square(released_row, released_col)
                    move = Move(initial, final)
                    
                    # Check if the move is valid
                    if self.game.board.valid_move(piece, move):
                        captured = self.game.board.squares[released_row][released_col].has_piece()
                        self.game.board.move(piece, move)
                        self.game.board.set_true_en_passant(piece)
                        self.game.play_sound(captured)
                        self.game.show_bg(self.screen)
                        self.game.show_last_move(self.screen)
                        self.game.show_pieces(self.screen)
                        self.game.next_turn()
                    
            except Exception as e:
                print(f"Error receiving data from server: {e}")
                break

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        # Connect to the server
        self.connect_to_server("127.0.0.1", 5555)  # Change host and port as needed

        # Start a thread to receive updates from the server
        receive_thread = threading.Thread(target=self.receive_updates_from_server)
        receive_thread.start()
        current_page = 0
        while True:
            pygame.time.Clock().tick(24)
            input_events = pygame.event.get()
            # Show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

 

            if dragger.dragging:
                dragger.update_blit(screen)
            
            # Display the flip book
            flipbook_screen, flip_duration, current_page = display_flipbook(screen, screen.get_width() - 800, 0,current_page, input_events=input_events )
            screen.blit(flipbook_screen, (screen.get_width() - 800, 0))

            for event in input_events:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE
                    if clicked_col > 7:
                        continue

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            board.set_true_en_passant(dragger.piece)
                            game.play_sound(captured)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()
                            # Send move to the server
                            move_str = f"{clicked_row}{clicked_col}{released_row}{released_col}"
                            self.send_move_to_server(move_str)
                        else:
                            self.show_alert("Invalid Move!")  

                        dragger.undrag_piece()


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()

                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()

main = Main()
main.mainloop()
