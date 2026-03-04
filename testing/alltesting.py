print("== alltesting.py started ==")

import sys
import os
print("sys.path =", sys.path)

# Add root to module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("✅ sys.path updated")

try:
    from engine.board import zionBoard
    print("✅ zionBoard imported")
    from engine.ai import get_best_move
    print("✅ get_best_move imported")
except Exception as e:
    print(f"❌ Import failed: {e}")
    exit()

test_cases = [
    {
        "name": "Start Pos",
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    },
    {
        "name": "Midgame Position",
        "fen": "r2q1rk1/ppp2ppp/2n2n2/3pp3/3P4/2P1PN2/PP3PPP/RNBQ1RK1 w - - 0 10"
    },
    {
        "name": "Endgame Position",
        "fen": "8/5k2/6p1/8/8/6K1/8/8 w - - 0 1"
    }
]


for case in test_cases:
    print(f"\n=== Test: {case['name']} ===")
    board = zionBoard()
    board.set_fen(case["fen"])
    board.print_board()
    move = get_best_move(board)
    print(f"Best move: {move}")

print("== alltesting.py ended ==")
