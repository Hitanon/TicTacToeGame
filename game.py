from engine.tic_tac_toe_engine import TicTacToeEngine
from service_game import ServiceGame


class Game:
    def __init__(self):
        player1_name = input("Enter player 1's name: ")
        player2_name = input("Enter player 2's name: ")
        self.engine = TicTacToeEngine(player1_name, player2_name)
        self.service = ServiceGame()

    def play(self):
        self.engine.set_date_start()
        while True:
            self.engine.display_board()
            move = input(f"{self.engine.current_player}'s turn. Enter a position (1-9): ")
            if self.engine.make_move(self.engine.current_player, move):
                if self.engine.check_victory():
                    self.engine.display_board()
                    self.engine.set_date_end()
                    self.service.save_result(self.engine)
                    print(f"Congratulations! {self.engine.current_player} wins!")
                    break
                elif self.engine.check_draw():
                    self.engine.display_board()
                    self.engine.set_date_end()
                    self.service.save_result(self.engine)
                    print("It's a draw!")
                    break
                else:
                    self.engine.current_player = self.engine.player2 \
                        if self.engine.current_player == self.engine.player1 \
                        else self.engine.player1
        self.service.close_db()
        # self.engine.display_moves()

    @staticmethod
    def show_menu():
        print("\nMenu:\n" +
              "1) Play\n" +
              "2) Show statistics\n" +
              "0) Exit\n")

    @staticmethod
    def show_player_statistics(statistics):
        if statistics is not None:
            result = f"\nPlayer \"{statistics['name']}\" statistics\n" + \
                     f"Number of games: {statistics['games']}\n" + \
                     f"Number of wins: {statistics['wins']}\n" + \
                     f"Number of defeats: {statistics['defeats']}\n" + \
                     f"Number of draws: {statistics['draws']}\n" + \
                     f"First Game: {statistics['date_first']}\n" + \
                     f"Last Game: {statistics['date_last']}\n" + \
                     f"Percentage of wins: {statistics['percentage']:.2f}%\n" + \
                     f"Rating: {statistics['rating']:.2f}"
            result.replace("None", "-")
            print(result)
        else:
            print("The player with this nickname does not exist in the database")

