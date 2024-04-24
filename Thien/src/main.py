import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
import random
import copy

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.player_vs_player = False
        self.radom = False
        self.depth = 2
        self.maximizing_player = True

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            # show methods
            if self.player_vs_player:
                print(dragger)
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():

                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        # if clicked square has a piece ?
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            # valid piece (color) ?
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # show methods 
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                    
                    # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)
                    
                    # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        # print(game.collect_valid_move())
                        print('\n')
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)
                            # print(dragger.piece)
                            # valid move ?
                            if board.valid_move(dragger.piece, move):
                                # normal capture
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)

                                board.set_true_en_passant(dragger.piece)                            

                                # sounds
                                game.play_sound(captured)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                # next turn
                                game.next_turn()
                        
                        dragger.undrag_piece()
                    
                    # key press
                    elif event.type == pygame.KEYDOWN:
                        
                        # changing themes
                        if event.key == pygame.K_t:
                            game.change_theme()

                        # changing themes
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger

                    # quit application
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                pygame.display.update()
            elif self.radom == True: 
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)
                if game.next_player == 'white':

                    for event in pygame.event.get():

                        # click
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            dragger.update_mouse(event.pos)

                            clicked_row = dragger.mouseY // SQSIZE
                            clicked_col = dragger.mouseX // SQSIZE

                            # if clicked square has a piece ?
                            if board.squares[clicked_row][clicked_col].has_piece():
                                piece = board.squares[clicked_row][clicked_col].piece
                                # valid piece (color) ?
                                if piece.color == game.next_player:
                                    board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                    dragger.save_initial(event.pos)
                                    dragger.drag_piece(piece)
                                    # show methods 
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_moves(screen)
                                    game.show_pieces(screen)
                        
                        # mouse motion
                        elif event.type == pygame.MOUSEMOTION:
                            motion_row = event.pos[1] // SQSIZE
                            motion_col = event.pos[0] // SQSIZE

                            game.set_hover(motion_row, motion_col)

                            if dragger.dragging:
                                dragger.update_mouse(event.pos)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                                game.show_hover(screen)
                                dragger.update_blit(screen)
                        
                        # click release
                        elif event.type == pygame.MOUSEBUTTONUP:
                            # print(game.collect_valid_move())
                            print('\n')
                            if dragger.dragging:
                                dragger.update_mouse(event.pos)

                                released_row = dragger.mouseY // SQSIZE
                                released_col = dragger.mouseX // SQSIZE

                                # create possible move
                                initial = Square(dragger.initial_row, dragger.initial_col)
                                final = Square(released_row, released_col)
                                move = Move(initial, final)
                                # print(dragger.piece)
                                # valid move ?
                                if board.valid_move(dragger.piece, move):
                                    # normal capture
                                    captured = board.squares[released_row][released_col].has_piece()
                                    board.move(dragger.piece, move)

                                    board.set_true_en_passant(dragger.piece)                            

                                    # sounds
                                    game.play_sound(captured)
                                    # show methods
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_pieces(screen)
                                    # next turn
                                    game.next_turn()
                                    
                            
                            
                            dragger.undrag_piece()
                        
                        # key press
                        elif event.type == pygame.KEYDOWN:
                            
                            # changing themes
                            if event.key == pygame.K_t:
                                game.change_theme()

                            # changing themes
                            if event.key == pygame.K_r:
                                game.reset()
                                game = self.game
                                board = self.game.board
                                dragger = self.game.dragger

                        # quit application
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    game.collect_valid_move()
                    if game.game_over():
                        print('Checkmate')
                        break
                    pygame.display.update()
                else:
                    
                # print(game.collect_valid_move())
                # print(valid_move)
                # King = True
                # for i in valid_move:
                #     if i[0].name == 'king':
                #         King = False
                #         break
                # if King:
                #     time.sleep(100)
                    game.collect_valid_move()
                    valid_move = game.valid_move
                    if game.loose_king:
                        print('lost king')
                        break
                    if game.game_over():
                        print('Checkmate')
                        break
                    random_move = random.choice(valid_move)
                    dragger_piece = random_move[0]
                    move = random_move[1]
                    print(dragger_piece,move)
                    board.move(dragger_piece, move)

                    board.set_true_en_passant(dragger_piece)                            

                # sounds
                # show methods
                    game.show_bg(screen)
                    game.show_last_move(screen)
                    game.show_pieces(screen)
                    # next turn
                    game.next_turn()
                    pygame.display.update()
            else:
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)
                if game.next_player == 'white':

                    for event in pygame.event.get():

                        # click
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            dragger.update_mouse(event.pos)

                            clicked_row = dragger.mouseY // SQSIZE
                            clicked_col = dragger.mouseX // SQSIZE

                            # if clicked square has a piece ?
                            if board.squares[clicked_row][clicked_col].has_piece():
                                piece = board.squares[clicked_row][clicked_col].piece
                                # valid piece (color) ?
                                if piece.color == game.next_player:
                                    board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                    dragger.save_initial(event.pos)
                                    dragger.drag_piece(piece)
                                    # show methods 
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_moves(screen)
                                    game.show_pieces(screen)
                        
                        # mouse motion
                        elif event.type == pygame.MOUSEMOTION:
                            motion_row = event.pos[1] // SQSIZE
                            motion_col = event.pos[0] // SQSIZE

                            game.set_hover(motion_row, motion_col)

                            if dragger.dragging:
                                dragger.update_mouse(event.pos)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                                game.show_hover(screen)
                                dragger.update_blit(screen)
                        
                        # click release
                        elif event.type == pygame.MOUSEBUTTONUP:
                            # print(game.collect_valid_move())
                            print('\n')
                            if dragger.dragging:
                                dragger.update_mouse(event.pos)

                                released_row = dragger.mouseY // SQSIZE
                                released_col = dragger.mouseX // SQSIZE

                                # create possible move
                                initial = Square(dragger.initial_row, dragger.initial_col)
                                final = Square(released_row, released_col)
                                move = Move(initial, final)
                                # print(dragger.piece)
                                # valid move ?
                                if board.valid_move(dragger.piece, move):
                                    # normal capture
                                    captured = board.squares[released_row][released_col].has_piece()
                                    board.move(dragger.piece, move)

                                    board.set_true_en_passant(dragger.piece)                            

                                    # sounds
                                    game.play_sound(captured)
                                    # show methods
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_pieces(screen)
                                    # next turn
                                    game.next_turn()
                                    
                            
                            
                            dragger.undrag_piece()
                        
                        # key press
                        elif event.type == pygame.KEYDOWN:
                            
                            # changing themes
                            if event.key == pygame.K_t:
                                game.change_theme()

                            # changing themes
                            if event.key == pygame.K_r:
                                game.reset()
                                game = self.game
                                board = self.game.board
                                dragger = self.game.dragger

                        # quit application
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    game.collect_valid_move()
                    if game.game_over():
                        print('Checkmate')
                        break
                    pygame.display.update()
                else:
                    
                # print(game.collect_valid_move())
                # print(valid_move)
                # King = True
                # for i in valid_move:
                #     if i[0].name == 'king':
                #         King = False
                #         break
                # if King:
                #     time.sleep(100)
                    if game.loose_king:
                        print('lost king')
                        break
                    if game.game_over():
                        print('Checkmate')
                        break
                    dragger_piece, move, eval = game.ai()
                    board.move(dragger_piece, move)
                    
                    board.set_true_en_passant(dragger_piece)                            

                # sounds
                # show methods
                    game.show_bg(screen)
                    game.show_last_move(screen)
                    game.show_pieces(screen)
                    # next turn
                    game.next_turn()
                    pygame.display.update()
                    
                    
    def minimax(self,depth,maximizing_player):
        if depth == 0 or self.explored_board.game_over():
            return None, None, self.explored_board.eval()  # Return the evaluation score when depth is 0 or the game is over
        
        if maximizing_player:
            best_piece = None
            best_move = None
            max_eval = float('-inf')  # Negative infinity
            
            for piece_move in self.explored_board.valid_move:
                self.explored_board.board.move(piece_move[0],piece_move[1])
                _, eval_score = self.minimax_ai(depth - 1, False)  # Recur with depth - 1 for opponent's turn
                self.explored_board.board.undo_move()
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = piece_move[1]
                    best_piece = piece_move[0]

            return best_piece,best_move, max_eval
        else:
            best_piece = None
            best_move = None
            min_eval = float('inf')  # Positive infinity
            
            for piece_move in self.explored_board.valid_move:
                self.explored_board.board.move(piece_move[0],piece_move[1])
                _, eval_score = self.minimax_ai(depth - 1, True)  # Recur with depth - 1 for AI's turn
                self.explored_board.board.undo_move()
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_piece = piece_move[0]
                    best_move = piece_move[1]

            return best_piece,best_move, min_eval
                


main = Main()
main.mainloop()