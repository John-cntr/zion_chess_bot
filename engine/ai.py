import chess
import time
from engine.board import BoardState
from engine.evaluation import evaluate_board

INFINITY = 1000000

class SearchFlags:
    EXACT = 0
    LOWERBOUND = 1
    UPPERBOUND = 2

class AIPlayer:
    def __init__(self, color=chess.WHITE, max_depth=7, war_mode=False, difficulty='medium'):
        self.color = color
        self.max_depth = max_depth
        self.war_mode = war_mode
        self.difficulty = difficulty
        self.nodes_searched = 0
        self.transposition_table = {}
        self.tt_hits = 0
        self.tt_misses = 0

        # Difficulty tuning parameters
        self.depth_lookup = {'easy': 4, 'medium': 7, 'hard': 10}
        self.max_depth = self.depth_lookup.get(difficulty, 7)

    def choose_move(self, board_state: BoardState, time_limit=None):
        # Iterative deepening
        best_move = None
        start_time = time.time()
        for depth in range(1, self.max_depth + 1):
            self.nodes_searched = 0
            score, move = self.alphabeta(board_state, depth, -INFINITY, INFINITY, True)
            if move is not None:
                best_move = move
            if time_limit and (time.time() - start_time) > time_limit:
                break
        return best_move

    def alphabeta(self, board_state, depth, alpha, beta, maximizing_player):
        if depth == 0 or board_state.is_game_over():
            return self.quiescence(board_state, alpha, beta), None

        self.nodes_searched += 1

        board = board_state.board

        # Transposition Table lookup
        hash_key = board_state.current_hash
        if hash_key in self.transposition_table:
            entry = self.transposition_table[hash_key]
            if entry['depth'] >= depth:
                flag = entry['flag']
                score = entry['score']
                if flag == SearchFlags.EXACT:
                    return score, entry['best_move']
                elif flag == SearchFlags.LOWERBOUND:
                    alpha = max(alpha, score)
                elif flag == SearchFlags.UPPERBOUND:
                    beta = min(beta, score)
                if alpha >= beta:
                    return score, entry['best_move']

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            # Checkmate or stalemate
            if board.is_check():
                return (-INFINITY if maximizing_player else INFINITY), None
            else:
                return 0, None  # Draw

        best_move = None

        if maximizing_player:
            max_eval = -INFINITY
            for move in legal_moves:
                board.push(move)
                board_state.update_hash(move)
                eval_score, _ = self.alphabeta(board_state, depth - 1, alpha, beta, False)
                board.pop()
                board_state.update_hash(move)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            self.store_tt_entry(hash_key, depth, max_eval, best_move, alpha, beta)
            return max_eval, best_move
        else:
            min_eval = INFINITY
            for move in legal_moves:
                board.push(move)
                board_state.update_hash(move)
                eval_score, _ = self.alphabeta(board_state, depth - 1, alpha, beta, True)
                board.pop()
                board_state.update_hash(move)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            self.store_tt_entry(hash_key, depth, min_eval, best_move, alpha, beta)
            return min_eval, best_move

    def quiescence(self, board_state, alpha, beta):
        stand_pat = evaluate_board(board_state.board)
        if self.war_mode:
            # In war mode, be more aggressive on eval
            stand_pat += random.randint(-15, 15)

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        board = board_state.board
        for move in board.legal_moves:
            # Only consider captures and checks for quiescence search
            if board.is_capture(move) or board.gives_check(move):
                board.push(move)
                board_state.update_hash(move)
                score = -self.quiescence(board_state, -beta, -alpha)
                board.pop()
                board_state.update_hash(move)

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

    def store_tt_entry(self, hash_key, depth, score, best_move, alpha, beta):
        flag = SearchFlags.EXACT
        if score <= alpha:
            flag = SearchFlags.UPPERBOUND
        elif score >= beta:
            flag = SearchFlags.LOWERBOUND
        self.transposition_table[hash_key] = {
            'depth': depth,
            'score': score,
            'best_move': best_move,
            'flag': flag
        }

    def should_resign(self, eval_score, threshold=-900):
        """
        AI resigns if eval is worse than threshold
        """
        return eval_score < threshold

    def should_offer_draw(self, board_state, eval_score):
        """
        Offer draw if evaluation close to zero and repetitions or 50-move rule
        """
        if abs(eval_score) < 50 and (board_state.board.can_claim_fifty_moves() or board_state.board.is_repetition(3)):
            return True
        return False
print('yes')