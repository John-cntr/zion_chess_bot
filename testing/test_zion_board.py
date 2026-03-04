import chess
from engine.board import zionBoard
from engine.ai import get_best_move

def test_basic_moves():
    zb = zionBoard()

    result = zb.make_move("e2e4")
    assert result is True, "Legal move should be accepted"

    result = zb.make_move("e9e5")
    assert result.startswith("invalid") or result == "illegal move", "Invalid move should be rejected"
def test_resignation():
    print("\nRunning Zion resignation test...")

    zb = zionBoard()

    # Create a position where Zion is clearly losing
    # For example: remove all Zion's pieces
    zb.board.set_fen("8/8/8/8/8/8/8/k6K w - - 0 1")

    # Now it's white to move, but white has only king. If Zion is white, he's doomed
    zb.turn = zb.board.turn  # Sync turn

    resigned = zb.zion_considers_resignation()
    print("Resignation returned:", resigned)
    print("Zion resigned flag:", zb.zion_resigned)

    assert resigned is True, "Zion should resign on bad evaluation"
    print("Resignation test passed")



def test_draw_offer_acceptance():
    zb = zionBoard()

    response = zb.make_move("d")
    assert response == "user offered draw", "User should be able to offer draw"
    assert zb.user_offered_draw is True, "user_offered_draw flag should be True"

    import engine.evaluation
    original_eval = engine.evaluation.evaluate_board
    engine.evaluation.evaluate_board = lambda b: 0

    response = zb.zion_considers_user_draw_offer()
    assert response == "zion accepted draw", "Zion should accept draw offer in balanced position"
    assert zb.user_offered_draw is False, "user_offered_draw flag reset after acceptance"
    assert zb.zion_accepted_draw is True, "zion_accepted_draw flag should be set"

    engine.evaluation.evaluate_board = original_eval

def test_ai_move_generation():
    zb = zionBoard()
    move = get_best_move(zb, depth=1)
    assert move is not None, "AI should return a move"
    if move not in ["resign", "offer_draw"]:
        assert chess.Move.from_uci(move) in zb.legal_moves, "AI move should be legal"

def run_all_tests():
    test_basic_moves()
    print("Basic moves test passed")

    # test_resignation()
    # print("Resignation test passed")

    test_draw_offer_acceptance()
    print("Draw offer/acceptance test passed")

    test_ai_move_generation()
    print("AI move generation test passed")

if __name__ == "__main__":
    run_all_tests()
