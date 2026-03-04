import chess
from engine.board import BoardState
from engine.ai import AIPlayer
import sys

def print_board(board):
    print(board)
    print()

def get_user_move(board):
    while True:
        try:
            user_input = input("Your move (in UCI format, e.g. e2e4): ").strip()
            move = chess.Move.from_uci(user_input)
            if move in board.legal_moves:
                return move
            else:
                print("Illegal move. Try again.")
        except Exception:
            print("Invalid input. Use format like e2e4.")

def main():
    print("Welcome to Zion Chess AI!")
    print("Choose your color: (w)hite or (b)lack")
    choice = input("Enter w or b: ").lower().strip()

    if choice not in ['w', 'b']:
        print("Invalid choice. Defaulting to white.")
        choice = 'w'

    player_color = chess.WHITE if choice == 'w' else chess.BLACK
    ai_color = not player_color

    board_state = BoardState()
    ai = AIPlayer(color=ai_color, difficulty='medium', war_mode=True)

    print_board(board_state.board)

    while not board_state.is_game_over():
        if board_state.board.turn == player_color:
            move = get_user_move(board_state.board)
            board_state.push(move)
        else:
            print("Zion is thinking...")
            move = ai.choose_move(board_state)
            if move is None:
                print("Zion resigns!")
                break

            board_state.push(move)
            print(f"Zion played: {move.uci()}")

            eval_score = evaluate_board(board_state.board)

            if ai.should_resign(eval_score):
                print("Zion resigns based on evaluation!")
                break
            if ai.should_offer_draw(board_state, eval_score):
                print("Zion offers a draw.")

        print_board(board_state.board)

    result = board_state.board.result()
    print("Game Over. Result:", result)

if __name__ == "__main__":
    from engine.evaluation import evaluate_board
    main()
