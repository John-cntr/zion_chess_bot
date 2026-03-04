import chess
from engine.ai import evaluate_board
from engine.evaluation import is_war_mode

def test_war_mode_case(fen, description, expected_war_mode):
    board = chess.Board(fen)
    print(f"\n🔍 Testing: {description}")
    triggered = is_war_mode(board)

    if triggered == expected_war_mode:
        print(f"✅ War Mode Trigger: {triggered}")
    else:
        print(f"❌ War Mode Trigger Mismatch: Expected {expected_war_mode}, Got {triggered}")

    score = evaluate_board(board, chess.WHITE)
    print(f"🧠 Eval Score (White): {score}")


# 🧪 BASE: Trigger war mode with simple pawn + king vs king
fen_base = "8/8/8/8/8/4K3/8/4k3 w - - 0 1"

# 🧪 MID: Endgame with passed pawn and centralized king
fen_mid = "8/4k3/8/4P3/8/8/8/4K3 w - - 0 1"

# 🧪 TOP: Complex late game with both sides having pieces
fen_top = "8/1p3pk1/2p2np1/2P5/4P3/1P1K1P2/6P1/8 w - - 0 1"

if __name__ == "__main__":
    test_war_mode_case(fen_base, "Base: King vs King", expected_war_mode=True)
    test_war_mode_case(fen_mid, "Mid: Passed pawn + active king", expected_war_mode=True)
    test_war_mode_case(fen_top, "Top: Advanced endgame complexity", expected_war_mode=True)
