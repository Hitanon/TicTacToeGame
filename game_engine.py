class GameEngine:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.history = []

    def display_moves(self):
        for player, position in self.history:
            symbol = "X" if player == self.player1 else "O"
            print(f"{player}: {symbol} at position {position}")
