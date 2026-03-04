import chess
import random
import hashlib

class BoardState:
    def __init__(self, board=None):
        self.board = board if board else chess.Board()
        # Zobrist Hash init
        self.zobrist_table = self.init_zobrist()
        self.current_hash = self.compute_hash()

        # Transposition table: zobrist hash -> (depth, score, flag, best_move)
        self.transposition_table = {}

    def init_zobrist(self):
        # Create random 64-bit numbers for each piece on each square
        table = {}
        for piece_type in range(1, 7):
            for color in [chess.WHITE, chess.BLACK]:
                for square in chess.SQUARES:
                    table[(piece_type, color, square)] = random.getrandbits(64)
        # Castling rights: 16 possible states
        for cr in range(16):
            table[('castling', cr)] = random.getrandbits(64)
        # En passant files 8 possible
        for file in range(8):
            table[('enpassant', file)] = random.getrandbits(64)
        # Side to move
        table['black_to_move'] = random.getrandbits(64)
        return table

    def compute_hash(self):
        h = 0
        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if piece:
                h ^= self.zobrist_table[(piece.piece_type, piece.color, sq)]
        # Castling rights
        cr = self.board.castling_rights
        h ^= self.zobrist_table[('castling', cr)]
        # En passant
        ep = self.board.ep_square
        if ep is not None:
            file = chess.square_file(ep)
            h ^= self.zobrist_table[('enpassant', file)]
        # Side to move
        if self.board.turn == chess.BLACK:
            h ^= self.zobrist_table['black_to_move']
        return h

    def update_hash(self, move):
        # Instead of full recompute, incrementally update (complex, skipping here)
        self.current_hash = self.compute_hash()

    def push(self, move):
        self.board.push(move)
        self.update_hash(move)

    def pop(self):
        move = self.board.pop()
        self.update_hash(move)
        return move

    def is_game_over(self):
        return self.board.is_game_over()

    def legal_moves(self):
        return list(self.board.legal_moves)

    def fen(self):
        return self.board.fen()

    def reset(self):
        self.board.reset()
        self.current_hash = self.compute_hash()
print('yes')