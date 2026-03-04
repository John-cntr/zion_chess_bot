import sys
from engine.ai import get_best_move
from engine.board import zionBoard

def main():
    zb = zionBoard()
    print("Welcome to Zion Chess (You are White)")

    while not zb.is_game_over():
        zb.print_board()

        if zb.board.turn:  # Human's turn
            move = input("Your move (or 'r' to resign, 'q' to quit): ").strip().lower()

            if move == 'r':
                print("You resigned. Zion wins!")
                break
            elif move == 'q':
                print("Game exited by user.")
                sys.exit()  # Properly exits the game

            if not zb.make_move(move):
                print("Invalid move! Try again.")
        else:  # AI's turn
            print("Zion is thinking...")
            ai_move = get_best_move(zb.board, depth=2)
            print(f"Zion plays: {ai_move}")
            zb.make_move(ai_move)

    zb.print_board()
    print("Game Over! Result:", zb.board.result())

if __name__ == "__main__":
    main()