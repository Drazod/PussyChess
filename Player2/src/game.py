import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # blit methods
    def game_over(self):
        return self.valid_move == []
    def collect_valid_move(self):
        self.loose_king = True
        valid_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece.color == self.next_player:
                        self.board.calc_moves(piece, row, col)
                        
                        if piece.name == 'king':
                            self.loose_king = False
                            # self.king_pos = (row, col)
                            # print(piece,(row, col))
                        for move in piece.moves:
                            valid_moves.append((piece,move))
        self.valid_move = valid_moves
        # return valid_moves
    def eval(self):
        white_score = 0
        black_score = 0

        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece.color == 'white':
                        white_score += piece.value  # Add the piece value to white's score
                    else:
                        black_score += piece.value  # Add the piece value to black's score
        # Calculate the overall material advantage
        material_advantage = white_score + black_score
        return material_advantage
    
    def minimax_ai(self,depth, maximizing_player):
        if depth == 0 or self.game_over():
            return None, self.eval()  # Return the evaluation score when depth is 0 or the game is over
        
        if maximizing_player:
            best_move = None
            max_eval = float('-inf')  # Negative infinity
            
            for piece_move in self.collect_valid_move():
                self.board.move(piece_move[0],piece_move[1])
                _, eval_score = self.minimax_ai(depth - 1, False)  # Recur with depth - 1 for opponent's turn
                self.board.undo_move()
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = piece_move[1]

            return best_move, max_eval
        else:
            best_move = None
            min_eval = float('inf')  # Positive infinity
            
            for piece_move in self.collect_valid_move():
                self.board.move(piece_move[0],piece_move[1])
                _, eval_score = self.minimax_ai(depth - 1, True)  # Recur with depth - 1 for AI's turn
                self.board.undo_move()
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = piece_move[1]

            return best_move, min_eval

    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                # Load the image based on whether the square is light or dark
                if (row + col) % 2 == 0:
                    img = pygame.image.load("../assets/images/light_square_image.png")
                else:
                    img = pygame.image.load("../assets/images/dark_square_image.png")

                # Scale the image to match the size of a square
                img = pygame.transform.scale(img, (SQSIZE, SQSIZE))

                # Calculate the position of the square
                square_pos = (col * SQSIZE, row * SQSIZE)

                # Blit the image onto the surface
                surface.blit(img, square_pos)

                # Add row and column coordinates if necessary
                if col == 0:
                    # label
                    lbl = self.config.font.render(str(ROWS-row), 1, theme.bg.dark if row % 2 == 0 else theme.bg.light)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    surface.blit(lbl, lbl_pos)

                if row == 7:
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(lbl, lbl_pos)


    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        # Update the piece's current frame
                        piece.next_frame()
                        # Set the texture based on the current frame
                        piece.set_texture(size=80)
                        
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)


    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        if col > 7 or row > 7:
            return
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()