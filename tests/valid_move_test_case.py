import unittest

import parameterized as p

from engine.tic_tac_toe_engine import TicTacToeEngine


class ValidMoveTestCase(unittest.TestCase):

    @p.parameterized.expand([
        ([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 1, "first", "second"),
        (['X', '0', ' ', 'X', 'X', '0', '0', ' ', ' '], 3, "second", "first"),
        (['X', '0', ' 0', 'X', 'X', '0', '0', 'X', ' '], 9, "first", "second"),
    ])
    def test_is_valid_move(self, board, move, player1, player2):
        engine = TicTacToeEngine(player1, player2)
        engine.board = board

        result = engine.make_move(player1, move)

        self.assertTrue(result, f"test_is_valid_move: board: {engine.board}; "
                                f"move: {move}; player1: {player1}; player2: {player2}")

    @p.parameterized.expand([
        ([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], "invalid_move", "first", "second"),
        (['X', '0', ' ', 'X', 'X', '0', '0', ' ', ' '], -2, "second", "first"),
        (['X', '0', ' ', 'X', 'X', '0', '0', ' ', ' '], 0, "second", "first"),
        (['X', '0', ' ', 'X', 'X', '0', '0', ' ', ' '], 10, "second", "first"),
        (['X', '0', ' 0', 'X', 'X', '0', '0', 'X', ' '], 1, "first", "second"),
        (['X', '0', ' ', 'X', 'X', '0', '0', ' ', ' '], 6, "second", "first"),
    ])
    def test_is_invalid_move(self, board, move, player1, player2):
        engine = TicTacToeEngine(player1, player2)
        engine.board = board

        result = engine.make_move(player1, move)

        self.assertFalse(result, f"test_is_invalid_move: board: {engine.board}; "
                                 f"move: {move}; player1: {player1}; player2: {player2}")


if __name__ == "__main__":
    unittest.main()
