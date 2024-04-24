import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
import copy




class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.loose_king = True
        self.king_pos = None
        
        self.valid_move=None

    # blit methods

    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    # print(piece)
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
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
    def ai(self,game):
        ai = AI(engine=game,depth=2,color=self.next_player,boards_explored=self.board)
        print("Begin AI")
        piece, move, score = ai.minimax_ai(depth = 2,color=self.next_player)
        print("End AI")
        print(score)
        return piece, move,score
        
class AI(): 
    def __init__(self,engine,depth,color,boards_explored):
        self.engine = engine
        self.depth = depth
        self.color = color 
        self.boards_explored = copy.deepcopy(boards_explored)
        
        self.valid_move = []
    def next_turn(self,color):
        return 'white' if color == 'black' else 'black'
    def eval(self):
        white_score = 0
        black_score = 0

        for row in range(ROWS):
            for col in range(COLS):
                if self.boards_explored.squares[row][col].has_piece():
                    piece = self.boards_explored.squares[row][col].piece
                    if piece.color == 'white':
                        white_score += piece.value  # Add the piece value to white's score
                    else:
                        black_score += piece.value  # Add the piece value to black's score

        # Calculate the overall material advantage
        material_advantage = white_score + black_score

        return material_advantage
    def game_over(self):
        return self.valid_move == []
    def collect_valid_move(self,color):
        print(color)
        valid_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.boards_explored.squares[row][col].has_piece():
                    piece = self.boards_explored.squares[row][col].piece
                    if piece.color == color:
                        self.boards_explored.calc_moves(piece, row, col)
                        for move in piece.moves:
                            valid_moves.append((piece,move))
        self.valid_move = valid_moves
    def minimax_ai(self,depth,color):
        self.collect_valid_move(color)
        # print(self.valid_move)
        print(depth)
        if depth == 0 or self.game_over():
            return None,None, self.eval()  # Return the evaluation score when depth is 0 or the game is over
        if color == self.color:
            best_move = None
            best_piece = None
            max_eval = float('-inf')  # Negative infinity
            for piece_move in self.valid_move:
                self.boards_explored.move(piece_move[0],piece_move[1])
                color = self.next_turn(color)
                _, _, eval_score = self.minimax_ai(depth=depth-1,color=color)  # Recur with depth - 1 for opponent's turn
                piece_move[1].initial, piece_move[1].final=  piece_move[1].final, piece_move[1].initial
                self.boards_explored.move(piece_move[0],piece_move[1])
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_piece = piece_move[0]
                    best_move = piece_move[1]
            print(best_move, best_piece, max_eval)

            return best_piece, best_move, max_eval
        else:
            best_move = None
            best_piece = None
            min_eval = float('inf')  # Positive infinity
            
            for piece_move in self.valid_move:
                self.boards_explored.move(piece_move[0],piece_move[1])
                color = self.next_turn(color)
                _, _, eval_score = self.minimax_ai(depth=depth-1,color=color) # Recur with depth - 1 for AI's turn
                piece_move[1].initial, piece_move[1].final=  piece_move[1].final, piece_move[1].initial
                self.boards_explored.move(piece_move[0],piece_move[1])
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_piece = piece_move[0]
                    best_move = piece_move[1]
            print(best_move, best_piece, min_eval)

            return best_piece, best_move, min_eval
    def heatmap(self):
        pass 
    def threats(self):
        pass 
    def book_move(self):
        pass 
    def get_mover(self):
        pass
    
def heuristic_gen(list):
    for num in list:
        yield num
    yield "Done generating"