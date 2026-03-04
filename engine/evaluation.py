import chess
import random

# Base piece values (scaled by 100)
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Piece-square tables (simplified; mirror for black)
PAWN_PST = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10,-20,-20, 10, 10,  5,
     5, -5,-10,  0,  0,-10, -5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_PST = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_PST = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_PST = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_PST = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_MID_PST = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]

KING_END_PST = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

CENTER_SQUARES = [chess.D4, chess.D5, chess.E4, chess.E5]

def piece_square_table(piece_type, square, color, endgame=False):
    if piece_type == chess.PAWN:
        val = PAWN_PST[square if color == chess.WHITE else chess.square_mirror(square)]
    elif piece_type == chess.KNIGHT:
        val = KNIGHT_PST[square if color == chess.WHITE else chess.square_mirror(square)]
    elif piece_type == chess.BISHOP:
        val = BISHOP_PST[square if color == chess.WHITE else chess.square_mirror(square)]
    elif piece_type == chess.ROOK:
        val = ROOK_PST[square if color == chess.WHITE else chess.square_mirror(square)]
    elif piece_type == chess.QUEEN:
        val = QUEEN_PST[square if color == chess.WHITE else chess.square_mirror(square)]
    elif piece_type == chess.KING:
        if endgame:
            val = KING_END_PST[square if color == chess.WHITE else chess.square_mirror(square)]
        else:
            val = KING_MID_PST[square if color == chess.WHITE else chess.square_mirror(square)]
    else:
        val = 0
    return val

def evaluate_board(board: chess.Board):
    """
    Composite evaluation function.
    Positive means advantage for White, negative for Black.
    """
    score = 0
    # Detect endgame by material threshold
    endgame = is_endgame(board)

    # Material + PST
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            val = PIECE_VALUES[piece.piece_type]
            pst_val = piece_square_table(piece.piece_type, sq, piece.color, endgame)
            total_val = val + pst_val
            if piece.color == chess.WHITE:
                score += total_val
            else:
                score -= total_val

    # King safety
    score += evaluate_king_safety(board)

    # Center control
    score += evaluate_center_control(board)

    # Mobility
    score += evaluate_mobility(board)

    # Pawn structure
    score += evaluate_pawn_structure(board)

    # Threats and good trades
    score += evaluate_threats_and_captures(board)

    return score

def is_endgame(board):
    """
    Determine if position is in endgame.
    Simple heuristic: If both sides have queens off OR
    total material less than a threshold.
    """
    queens = sum(len(board.pieces(chess.QUEEN, c)) for c in [chess.WHITE, chess.BLACK])
    total_material = sum(len(board.pieces(pt, chess.WHITE)) + len(board.pieces(pt, chess.BLACK)) for pt in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT])
    if queens == 0 or total_material <= 6:
        return True
    return False

def evaluate_king_safety(board):
    # Penalize king exposed to attacks or weak pawn shield
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        if king_square is None:
            continue
        # Count pawns around king
        pawns_around = 0
        for sq in chess.SQUARES:
            if board.piece_at(sq) and board.piece_at(sq).piece_type == chess.PAWN and board.piece_at(sq).color == color:
                if chess.square_distance(sq, king_square) <= 2:
                    pawns_around += 1
        # King safety bonus if many pawns nearby, penalty if few
        val = (pawns_around - 2) * 15  # -30 if less than 2 pawns near king, +15 if more
        if color == chess.WHITE:
            score += val
        else:
            score -= val
    return score

def evaluate_center_control(board):
    score = 0
    for sq in CENTER_SQUARES:
        piece = board.piece_at(sq)
        if piece:
            if piece.color == chess.WHITE:
                score += 20
            else:
                score -= 20
    # Also add a bit for attacks on center squares
    for sq in CENTER_SQUARES:
        attackers_white = board.attackers(chess.WHITE, sq)
        attackers_black = board.attackers(chess.BLACK, sq)
        score += 5 * (len(attackers_white) - len(attackers_black))
    return score

def evaluate_mobility(board):
    # Mobility = number of legal moves (normalized)
    white_moves = len(list(board.legal_moves)) if board.turn == chess.WHITE else len(list(board.legal_moves))
    board.push(chess.Move.null())
    black_moves = len(list(board.legal_moves))
    board.pop()
    mobility_score = 10 * (white_moves - black_moves)
    return mobility_score

def evaluate_pawn_structure(board):
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        pawns = board.pieces(chess.PAWN, color)
        files = [chess.square_file(sq) for sq in pawns]
        file_counts = {}
        for f in files:
            file_counts[f] = file_counts.get(f, 0) + 1

        # Penalty for doubled pawns
        doubled = sum([count - 1 for count in file_counts.values() if count > 1])
        val = -20 * doubled
        if color == chess.WHITE:
            score += val
        else:
            score -= val

        # Isolated pawns penalty
        isolated = 0
        for f in file_counts:
            if (f-1 not in file_counts) and (f+1 not in file_counts):
                isolated += file_counts[f]
        val2 = -15 * isolated
        if color == chess.WHITE:
            score += val2
        else:
            score -= val2
    return score

def evaluate_threats_and_captures(board):
    # Reward for pieces attacking higher value targets
    score = 0
    for sq in chess.SQUARES:
        attacker = board.piece_at(sq)
        if attacker is None:
            continue
        for target_sq in board.attacks(sq):
            target = board.piece_at(target_sq)
            if target and target.color != attacker.color:
                # Basic MVV-LVA: Most Valuable Victim - Least Valuable Attacker
                victim_val = PIECE_VALUES[target.piece_type]
                attacker_val = PIECE_VALUES[attacker.piece_type]
                gain = victim_val - attacker_val
                # Only count if gain is positive (good trade)
                if gain > 0:
                    if attacker.color == chess.WHITE:
                        score += gain // 2
                    else:
                        score -= gain // 2
    return score
print('yes')