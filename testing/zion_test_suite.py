import sys
import traceback
from engine.board import Board
from engine.ai import get_best_move, evaluate_board  # assume evaluate_board returns evaluation score

def run_test_case(name, func):
    print(f"\n--- Running test: {name} ---")
    try:
        func()
        print(f"[PASS] {name}")
    except AssertionError as e:
        print(f"[FAIL] {name} - AssertionError: {e}")
    except Exception as e:
        print(f"[FAIL] {name} - Exception occurred:")
        traceback.print_exc(file=sys.stdout)

# --------- Scenario 1: AI Move Selection ---------
def test_ai_move_selection():
    # Base Case: Opening position, depth=1, expect legal move
    def base():
        board = Board()
        move = get_best_move(board, max_depth=1)
        assert move in [m.uci() for m in board.board.legal_moves], "Move not legal in base case"

    # Mid Case: Midgame simple position, depth=3
    def mid():
        board = Board()
        # Apply some moves to reach midgame (simple)
        moves = ["e4", "e5", "Nf3", "Nc6", "Bc4", "Nf6"]
        for m in moves:
            board.board.push_san(m)
        move = get_best_move(board, max_depth=3)
        assert move in [m.uci() for m in board.board.legal_moves], "Move not legal in mid case"

    # Top Case: Complex middle game position, depth=5
    def top():
        board = Board()
        # Complex position (custom FEN or moves)
        fen = "r1bq1rk1/ppp1bppp/2n2n2/2bp4/4P3/2NP1N2/PPP2PPP/R1BQ1RK1 w - - 0 8"
        board.board.set_fen(fen)
        move = get_best_move(board, max_depth=5, max_time=10.0)
        assert move in [m.uci() for m in board.board.legal_moves], "Move not legal in top case"

    base()
    mid()
    top()

# --------- Scenario 2: Resignation Logic ---------
def test_resignation_logic():
    # Base: Obviously losing position for white (e.g. mate in 1 for black)
    def base():
        board = Board()
        # Fool's mate position, white about to be checkmated
        fen = "rnb1kbnr/ppppqppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 3"
        board.board.set_fen(fen)
        move = get_best_move(board, max_depth=3)
        assert move == "resign", "Base resignation not detected"

    # Mid: Material heavily down for white, no mate but hopeless
    def mid():
        board = Board()
        fen = "rnbq1rk1/pppp1ppp/4pn2/8/2B1P3/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 0 7"
        board.board.set_fen(fen)
        move = get_best_move(board, max_depth=4)
        assert move == "resign", "Mid resignation not detected"

    # Top: Near hopeless position with severe material disadvantage
    def top():
        board = Board()
        fen = "8/8/8/8/8/8/7k/6KR w - - 0 1"  # White king cornered badly, losing badly
        board.board.set_fen(fen)
        move = get_best_move(board, max_depth=6)
        assert move == "resign", "Top resignation not detected"

    base()
    mid()
    top()

# --------- Scenario 3: Draw Offer Handling ---------
def test_draw_offer_handling():
    # Base: Balanced position, expect 'offer_draw' or a non-losing move
    def base():
        board = Board()
        fen = "8/8/8/8/8/8/7k/6KR w - - 0 1"  # Almost equal material, just example
        board.board.set_fen(fen)
        move = get_best_move(board, max_depth=3)
        assert move in ["offer_draw"] + [m.uci() for m in board.board.legal_moves], "Base draw offer missing"

    # Mid: Balanced midgame position
    def mid():
        board = Board()
        fen = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/2N5/PPPP1PPP/R1BQKBNR w KQkq - 0 4"
        board.board.set_fen(fen)
        move = get_best_move(board, max_depth=4)
        assert move in ["offer_draw"] + [m.uci() for m in board.board.legal_moves], "Mid draw offer missing"

    # Top: Complex balanced endgame position
    def top():
        board = Board()
        fen = "8/8/8/8/8/8/6k1/7K w - - 50 50"  # Draw by 50-move rule, balanced
        board.board.set_fen(fen)
        move = get_best_move(board, max_depth=5)
        assert move in ["offer_draw"] + [m.uci() for m in board.board.legal_moves], "Top draw offer missing"

    base()
    mid()
    top()

# --------- Scenario 4: Positional Evaluation ---------
def test_positional_evaluation():
    def base():
        board = Board()
        # Equal material opening position
        board.board.reset()
        eval_score = evaluate_board(board.board)
        assert abs(eval_score) < 0.1, "Base evaluation failed (should be near zero)"

    def mid():
        board = Board()
        # White up a pawn
        fen = "rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 3"
        board.board.set_fen(fen)
        eval_score = evaluate_board(board.board)
        assert eval_score > 0, "Mid evaluation failed (white should be better)"

    def top():
        board = Board()
        # Black up a rook, complicated position
        fen = "rnb1kbnr/pppp1ppp/4p3/8/3P4/2N5/PPP1PPPP/R1BQKBNR b KQkq - 0 4"
        board.board.set_fen(fen)
        eval_score = evaluate_board(board.board)
        assert eval_score < 0, "Top evaluation failed (black should be better)"

    base()
    mid()
    top()

# --------- Scenario 5: King Safety Evaluation ---------
def test_king_safety_evaluation():
    def base():
        board = Board()
        # Safe kings in opening position
        board.board.reset()
        score = evaluate_board(board.board)
        assert score is not None, "Base king safety evaluation failed"

    def mid():
        board = Board()
        # White king exposed
        fen = "rnbq1rk1/pppp1ppp/5n2/4p3/1b2P3/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 0 7"
        board.board.set_fen(fen)
        score = evaluate_board(board.board)
        # Expect penalty for white king exposed, so score should be negative if black better
        assert score < 0, "Mid king safety evaluation failed"

    def top():
        board = Board()
        # Black king badly exposed, white attacking
        fen = "rnbq1rk1/ppp2ppp/3bp3/8/3P4/2N1PN2/PPP2PPP/R1BQ1RK1 b - - 0 8"
        board.board.set_fen(fen)
        score = evaluate_board(board.board)
        assert score > 0, "Top king safety evaluation failed"

    base()
    mid()
    top()

# --------- Scenario 6: Mobility Score Evaluation ---------
def test_mobility_score_evaluation():
    def base():
        board = Board()
        board.board.reset()
        score = evaluate_board(board.board)
        assert score is not None, "Base mobility evaluation failed"

    def mid():
        board = Board()
        fen = "rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 3"
        board.board.set_fen(fen)
        score = evaluate_board(board.board)
        assert score > 0, "Mid mobility evaluation failed (white should be more mobile)"

    def top():
        board = Board()
        fen = "rnbq1rk1/pppp1ppp/5n2/4p3/1b2P3/2N2N2/PPPP1PPP/R1BQ1RK1 w - - 0 7"
        board.board.set_fen(fen)
        score = evaluate_board(board.board)
        # Assuming black has less mobility here
        assert score > 0, "Top mobility evaluation failed"

    base()
    mid()
    top()

# --------- Scenario 7: Difficulty Scaling ---------
def apply_moves(board, moves):
    for move in moves:
        board.make_move(move)  # Replace with your actual move method if it's named differently
  # assuming push_uci applies the move in UCI format

def test_ai_move_():
    print("--- Running test: AI Move Selection ---")

    # Base case (simple)
    board = Board()
    base_moves = ['e2e4', 'e7e5', 'g1f3']
    apply_moves(board, base_moves)
    ai_instance = ai.AI(board, depth=depth)  # ✅ Correct
    move = ai_instance.get_best_move()

    move = ai.get_best_move(depth=3)
    assert move in board.legal_moves(), "Base case: Move is illegal"
    
    # Mid case (2 best moves scenario)
    board = Board()
    mid_moves = ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3']
    apply_moves(board, mid_moves)
    ai_instance = ai.AI(board, depth=depth)  # ✅ Correct
    move = ai_instance.get_best_move()

    move = ai.get_best_move(depth=5)
    assert move in board.legal_moves(), "Mid case: Move is illegal"
    
    # Top case (only 1 best move)
    board = Board()
    top_moves = ['d2d4', 'd7d5', 'c1g5', 'g8f6', 'e2e3', 'c8f5', 'f1d3', 'e7e6', 
                 'g1f3', 'h7h6', 'g5h4', 'd5c4', 'd3c4', 'c7c5']
    apply_moves(board, top_moves)
    ai = ai(board)
    move = ai.get_best_move(depth=7)
    assert move in board.legal_moves(), "Top case: Move is illegal"

    print("[PASS] AI Move Selection")
# Run all tests
def run_all_tests():
    tests = [
        ("AI Move Selection", test_ai_move_selection),
        ("Resignation Logic", test_resignation_logic),
        ("Draw Offer Handling", test_draw_offer_handling),
        ("Positional Evaluation", test_positional_evaluation),
        ("King Safety Evaluation", test_king_safety_evaluation),
        ("Mobility Score Evaluation", test_mobility_score_evaluation),
        ("Difficulty Scaling", test_ai_move_),
    ]

    for name, test_func in tests:
        run_test_case(name, test_func)

if __name__ == "__main__":
    run_all_tests()

