#for testing of board printing and moaking moves
from board import zionBoard as zbn

def main():
    zb = zbn()  
    print("welcome to zion ")
    while not zb.is_game_over():
        zb.print_board()
       
        player_color = 'white' if zb.board.turn else 'black'
        move = input(f"{player_color} to move: ")
        success = zb.make_mov(move)
        if not success:
            
            print("invalid move try again")

    print("game over ")
    zb.print_board()  
    
    print("result:", zb.board.result())


if __name__ == "__main__":
    main()