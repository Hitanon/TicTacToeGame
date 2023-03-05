import unittest
import parameterized as p
from engine.tic_tac_toe_engine import TicTacToeEngine
from generator.generator_boards import *


class EndTicTacToeGameTestCase(unittest.TestCase):

    @p.parameterized.expand(generate_winning_boards())
    def test_victory_board(self, *args):
        engine = TicTacToeEngine("first", "second")
        engine.board = list(args)

        result = engine.check_victory()

        self.assertTrue(result, f"test_victory_board: board: {engine.board}")

    @p.parameterized.expand([
        (' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '),
        ('X', ' ', ' ', 'X', ' ', ' ', '0', ' ', ' '),
        ('0', ' ', ' ', ' ', '0', ' ', ' ', ' ', 'X'),
        ('0', 'X', '0', 'X', '0', 'X', 'X', '0', 'X'),
    ])
    def test_is_not_victory_board(self, *args):
        engine = TicTacToeEngine("first", "second")
        engine.board = list(args)

        result = engine.check_victory()

        self.assertFalse(result, f"test_is_not_victory_board: board: {engine.board}")

    @p.parameterized.expand(generate_draw_boards(10))
    def test_draw_board(self, *args):
        engine = TicTacToeEngine("first", "second")
        engine.board = list(args)

        result = engine.check_draw()

        self.assertTrue(result, f"test_draw_board: board: {engine.board}")

    @p.parameterized.expand(generate_not_draw_boards(10))
    def test_is_not_draw_board(self, *args):
        engine = TicTacToeEngine("first", "second")
        engine.board = list(args)

        result = engine.check_draw()

        self.assertFalse(result, f"test_is_not_draw_board: board: {engine.board}")


if __name__ == "__main__":
    unittest.main()
