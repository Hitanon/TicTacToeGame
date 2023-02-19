from tic_tac_toe_engine import TicTacToeEngine


class Game:
    def __init__(self):
        player1_name = input("Enter player 1's name: ")
        player2_name = input("Enter player 2's name: ")
        self.engine = TicTacToeEngine(player1_name, player2_name)

    def play(self):
        current_player = self.engine.player1
        while True:
            self.engine.display_board()
            move = input(f"{current_player}'s turn. Enter a position (1-9): ")
            if self.engine.make_move(current_player, move):
                if self.engine.check_victory():
                    self.engine.display_board()
                    print(f"Congratulations! {current_player} wins!")
                    break
                elif self.engine.check_draw():
                    self.engine.display_board()
                    print("It's a draw!")
                    break
                else:
                    current_player = self.engine.player2 if current_player == self.engine.player1 else self.engine.player1

        self.engine.display_moves()
