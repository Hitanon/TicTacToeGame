from game_engine import GameEngine


class TicTacToeEngine(GameEngine):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.board = [" "] * 9

    def display_board(self):
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("---+---+---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("---+---+---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")

    def make_move(self, player, position):
        try:
            position = int(position)
        except ValueError:
            print("Invalid move. Position must be a number between 1 and 9.")
            return False

        if position < 1 or position > 9:
            print("Invalid move. Position must be between 1 and 9.")
            return False
        elif self.board[position - 1] != " ":
            print("Invalid move. Position already occupied.")
            return False
        else:
            symbol = "X" if player == self.player1 else "0"
            self.board[position - 1] = symbol
            self.history.append((player, position))
            return True

    def check_victory(self):
        lines = [
            self.board[0:3], self.board[3:6], self.board[6:9],  # rows
            self.board[0::3], self.board[1::3], self.board[2::3],  # columns
            self.board[0::4], self.board[2:8:2]  # diagonals
        ]
        for line in lines:
            if len(set(line)) == 1 and line[0] != " ":
                return True
        return False

    def check_draw(self):
        return " " not in self.board
