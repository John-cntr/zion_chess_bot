import chess
from engine.ai import get_best_move

board = chess.Board()
print("Initial Board:")
print(board)

move = get_best_move(board, depth=2)
print(f"Best move: {move}")
