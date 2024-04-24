import os
import time

class Piece:

    def __init__(self, name, color, value, animation_frames=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.animation_frames = animation_frames
        self.current_frame = 0
        self.texture_rect = texture_rect

    def set_animation_frames(self, frames):
        self.animation_frames = frames

    def next_frame(self):
        if self.animation_frames is not None:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

    def set_texture(self, size=80):
        if self.animation_frames is None:
            self.texture = os.path.join(
                f'../assets/images/imgs-{size}px/{self.color}_{self.name}.png')
        else:
            # Use the current frame from the animation frames
            self.texture = self.animation_frames[self.current_frame]

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class AnimatedPiece(Piece):

    def __init__(self, name, color, value, animation_frames=None, texture_rect=None):
        super().__init__(name, color, value, animation_frames, texture_rect)



class Pawn(AnimatedPiece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        if color == 'white':
            super().__init__('pawn', color, 1.0, ['../assets/images/pawn_idle.png', '../assets/images/pawn_active.png'])
        else:
            super().__init__('pawn', color, 1.0, ['../assets/images/bpawn_idle.png', '../assets/images/bpawn_active.png'])


class Knight(AnimatedPiece):

    def __init__(self, color):
        if color == 'white':
            super().__init__('knight', color, 3.0, ['../assets/images/knight_idle.png', '../assets/images/knight_active.png'])
        else:
            super().__init__('knight', color, 3.0, ['../assets/images/bknight_idle.png', '../assets/images/bknight_active.png'])

class Bishop(AnimatedPiece):

    def __init__(self, color):
        if color == 'white':
            super().__init__('bishop', color, 3.0001, ['../assets/images/bishop_idle.png', '../assets/images/bishop_active.png'])
        else:
            super().__init__('bishop', color, 3.0001, ['../assets/images/bbishop_idle.png', '../assets/images/bbishop_active.png'])

class Rook(AnimatedPiece):

    def __init__(self, color):
        if color == 'white':
            super().__init__('rook', color, 5.0, ['../assets/images/rook_idle.png', '../assets/images/rook_active.png'])
        else:
            super().__init__('rook', color, 5.0, ['../assets/images/brook_idle.png', '../assets/images/brook_active.png'])

class Queen(AnimatedPiece):

    def __init__(self, color):
        if color == 'white':
            super().__init__('queen', color, 9.0, ['../assets/images/queen_idle.png', '../assets/images/queen_active.png'])
        else:
            super().__init__('queen', color, 9.0, ['../assets/images/bqueen_idle.png', '../assets/images/bqueen_active.png'])

class King(AnimatedPiece):

    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        if color == 'white':
            super().__init__('king', color, 10000.0, ['../assets/images/king_idle.png', '../assets/images/king_active.png'])
        else:
            super().__init__('king', color, 10000.0, ['../assets/images/bking_idle.png', '../assets/images/bking_active.png'])
