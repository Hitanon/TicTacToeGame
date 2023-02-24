from datetime import datetime


class GameEngine:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.history = []
        self.date_start = None
        self.date_end = None
        self.game_state = -1

    def display_moves(self):
        for player, position in self.history:
            symbol = "X" if player == self.player1 else "O"
            print(f"{player}: {symbol} at position {position}")

    def set_date_start(self):
        self.date_start = datetime.now()

    def set_date_end(self):
        self.date_end = datetime.now()
