import unittest
from unittest.mock import patch
import sqlite3 as sq
from game import Game

DB_FILE = "test.db"
START_RATING = 500
PLAYER1 = 'test1'
PLAYER2 = 'test2'

script_deleting_players_table = "DROP TABLE IF EXISTS players"
script_deleting_games_table = "DROP TABLE IF EXISTS games"


class IntegrationRepositoryTestCase(unittest.TestCase):

    @staticmethod
    def try_get_player(name):
        try:
            conn = sq.connect(DB_FILE)
            conn.row_factory = sq.Row
            cur = conn.cursor()
            cur.execute("SELECT * from players WHERE name = ?", (name,))
            return cur.fetchone()
        except sq.Error:
            return None

    @staticmethod
    def try_get_player_id(name):
        try:
            conn = sq.connect(DB_FILE)
            conn.row_factory = sq.Row
            cur = conn.cursor()
            cur.execute("SELECT id from players WHERE name = ?", (name,))
            return cur.fetchone()
        except sq.Error:
            return None

    @staticmethod
    def try_get_game_result():
        try:
            conn = sq.connect(DB_FILE)
            conn.row_factory = sq.Row
            cur = conn.cursor()
            cur.execute("SELECT * from games")
            return cur.fetchone()
        except sq.Error:
            return None

    def assertPlayer(self, name, rating):
        player = self.try_get_player(name)

        self.assertIsNotNone(player)
        self.assertEqual(player['name'], name)
        self.assertEqual(player['rating'], rating)

    def assertGameResult(self, player1, player2, date_start, date_end, game_state, rating1, rating2):
        game_result = self.try_get_game_result()
        player1_id = self.try_get_player_id(player1)
        player2_id = self.try_get_player_id(player2)

        self.assertIsNotNone(game_result)
        self.assertEqual(game_result['id_p1'], player1_id['id'])
        self.assertEqual(game_result['id_p2'], player2_id['id'])
        self.assertEqual(game_result['result'], game_state)
        self.assertEqual(game_result['date_start'], date_start)
        self.assertEqual(game_result['date_end'], date_end)
        self.assertEqual(game_result['rating_p1'], rating1)
        self.assertEqual(game_result['rating_p2'], rating2)

    def setUp(self):
        try:
            conn = sq.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute(script_deleting_games_table)
            cur.execute(script_deleting_players_table)
            print(f"Clear SQLite database {DB_FILE} successful")
        except sq.Error as e:
            print(f"Error clearing db: {e}")

    @patch('builtins.input', side_effect=[PLAYER1, PLAYER2])
    def test_saving_game_results_new_players_when_first_player_won(self, mock_input):
        # Arrange
        game = Game(DB_FILE)
        game.engine.date_start = '2022-01-02 22:33:05'
        game.engine.date_end = '2022-01-02 22:34:02'
        game.engine.current_player = game.engine.player1
        game.engine.game_state = 1

        # Act
        result = game.service.save_result(game.engine)

        # Assert
        self.assertTrue(result)
        self.assertPlayer(PLAYER1, START_RATING + 20)
        self.assertPlayer(PLAYER2, START_RATING - 19)
        self.assertGameResult(player1=PLAYER1,
                              player2=PLAYER2,
                              date_start='2022-01-02 22:33:05',
                              date_end='2022-01-02 22:34:02',
                              game_state=1,
                              rating1=START_RATING,
                              rating2=START_RATING)


if __name__ == "__main__":
    unittest.main()
