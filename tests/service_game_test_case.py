import unittest
import parameterized as p
from unittest.mock import Mock, patch
from service_game import ServiceGame


class ServiceTicTacToeGameTestCase(unittest.TestCase):

    @patch('service_game.RepositoryGame')
    def test_save_game_exist_players_successful(self, mock_instance):
        # Arrange
        # Stub game engine
        mock_engine = Mock(player1='test1', player2='test2', game_state=1,
                           date_start='2022-01-02 22:33:05', date_end='2022-01-02 22:35:12')
        # Mock repository methods
        mock_repository = mock_instance.return_value
        mock_repository.get_player.side_effect = lambda name: \
            {'id': 1, 'name': 'test1', 'rating': 500} if name == 'test1' else {'id': 2, 'name': 'test2', 'rating': 500}
        mock_repository.save_game.return_value = True
        mock_repository.update_player.return_value = True
        # Create ServiceGame
        service_game = ServiceGame()
        service_game.create_player = Mock(return_value=True)
        service_game.update_players_rating = Mock(return_value=(520, 481))

        # Act
        result = service_game.save_result(mock_engine)

        # Assert
        self.assertTrue(result)
        mock_repository.get_player.assert_any_call('test1')
        mock_repository.get_player.assert_any_call('test2')
        mock_repository.save_game.assert_called_once_with(1, 2, 1, '2022-01-02 22:33:05',
                                                          '2022-01-02 22:35:12', 500, 500)
        mock_repository.update_player.assert_any_call('test1', 520)
        mock_repository.update_player.assert_any_call('test2', 481)

    @patch('service_game.RepositoryGame')
    def test_save_game_players_unsuccessful(self, mock_instance):
        # Arrange
        # Stub game engine
        mock_engine = Mock(player1='test1', player2='test2', game_state=1,
                           date_start='2022-01-02 22:33:05', date_end='2022-01-02 22:35:12')
        # Mock repository methods
        mock_repository = mock_instance.return_value
        mock_repository.get_player.return_value = None
        # Create ServiceGame
        service_game = ServiceGame()
        service_game.create_player = Mock(return_value=False)

        # Act
        result = service_game.save_result(mock_engine)

        # Assert
        self.assertFalse(result)
        mock_repository.get_player.assert_any_call('test1')
        mock_repository.get_player.assert_any_call('test2')
        mock_repository.save_game.assert_not_called()
        mock_repository.update_player.assert_not_called()

    @patch('service_game.RepositoryGame')
    def test_try_to_create_exist_player(self, mock_instance):
        # Arrange
        # Mock repository methods
        mock_repository = mock_instance.return_value
        mock_repository.get_player.return_value = {'id': 1, 'name': 'test1', 'rating': 500}
        # Create ServiceGame
        service_game = ServiceGame()

        # Act
        result = service_game.create_player('test1')

        # Assert
        self.assertFalse(result)
        mock_repository.get_player.assert_called_with("test1")
        mock_repository.save_player.assert_not_called()

    @p.parameterized.expand([
        (500, 500, 520, 481),
        (1000, 500, 1002, 497),
        (500, 1000, 537, 962),
    ])
    @patch('service_game.RepositoryGame')
    def test_update_player_rating_when_player1_win(self, p1_before, p2_before, rating1, rating2, mock_repository):
        # Arrange
        # Stub game engine
        mock_engine = Mock(player1='test1', player2='test2', game_state=1,
                           date_start='2022-01-02 22:33:05', date_end='2022-01-02 22:35:12')
        # Create ServiceGame
        service_game = ServiceGame()

        # Act
        result1, result2 = service_game.update_players_rating(p1_before, p2_before, mock_engine)

        # Assert
        self.assertEqual(result1, rating1, f"({p1_before}, {p2_before}, {rating1}, {rating2})")
        self.assertEqual(result2, rating2, f"({p1_before}, {p2_before}, {rating1}, {rating2})")

    @p.parameterized.expand([
        (500, 500, 480, 518),
        (1000, 500, 962, 537),
        (500, 1000, 497, 1002),
    ])
    @patch('service_game.RepositoryGame')
    def test_update_player_rating_when_player2_win(self, p1_before, p2_before, rating1, rating2, mock_repository):
        # Arrange
        # Stub game engine
        mock_engine = Mock(player1='test1', player2='test2', game_state=2,
                           date_start='2022-01-02 22:33:05', date_end='2022-01-02 22:35:12')
        # Create ServiceGame
        service_game = ServiceGame()

        # Act
        result1, result2 = service_game.update_players_rating(p1_before, p2_before, mock_engine)

        # Assert
        self.assertEqual(result1, rating1, f"({p1_before}, {p2_before}, {rating1}, {rating2})")
        self.assertEqual(result2, rating2, f"({p1_before}, {p2_before}, {rating1}, {rating2})")

    @p.parameterized.expand([
        (500, 500, 500, 500),
        (1000, 500, 982, 517),
        (500, 1000, 517, 982),
    ])
    @patch('service_game.RepositoryGame')
    def test_update_player_rating_when_is_draw(self, p1_before, p2_before, rating1, rating2, mock_repository):
        # Arrange
        # Stub game engine
        mock_engine = Mock(player1='test1', player2='test2', game_state=0,
                           date_start='2022-01-02 22:33:05', date_end='2022-01-02 22:35:12')
        # Create ServiceGame
        service_game = ServiceGame()

        # Act
        result1, result2 = service_game.update_players_rating(p1_before, p2_before, mock_engine)

        # Assert
        self.assertEqual(result1, rating1, f"({p1_before}, {p2_before}, {rating1}, {rating2})")
        self.assertEqual(result2, rating2, f"({p1_before}, {p2_before}, {rating1}, {rating2})")

    @patch('service_game.RepositoryGame')
    def test_get_non_exist_player_statistics(self, mock_instance):
        # Arrange
        # Mock repository methods
        mock_repository = mock_instance.return_value
        mock_repository.get_player.return_value = None
        # Create ServiceGame
        service_game = ServiceGame()

        # Act
        result = service_game.get_player_statistics('test1')

        # Assert
        self.assertFalse(result)
        mock_repository.get_player.assert_called_once_with('test1')

    @patch('service_game.RepositoryGame')
    def test_get_exist_player_statistics(self, mock_instance):
        # Arrange
        player = {'id': 1, 'name': 'test1', 'rating': 500}
        # Mock repository methods
        mock_repository = mock_instance.return_value
        mock_repository.get_player.return_value = player
        mock_repository.get_player_games.return_value = {'cnt': 10}
        mock_repository.get_player_wins.return_value = {'cnt': 5}
        mock_repository.get_player_defeats.return_value = {'cnt': 4}
        mock_repository.get_player_draws.return_value = {'cnt': 1}
        # Create ServiceGame
        service_game = ServiceGame()

        # Act
        result = service_game.get_player_statistics('test1')

        # Assert
        self.assertEqual(result, {'name': 'test1',
                                  'games': 10,
                                  'wins': 5,
                                  'defeats': 4,
                                  'draws': 1,
                                  'rating': 500,
                                  'percentage': 50})
        mock_repository.get_player.assert_called_once_with('test1')
        mock_repository.get_player_games.assert_called_once_with(player)
        mock_repository.get_player_wins.assert_called_once_with(player)
        mock_repository.get_player_defeats.assert_called_once_with(player)
        mock_repository.get_player_draws.assert_called_once_with(player)

    @patch('service_game.RepositoryGame')
    def test_get_non_exist_player_last_games(self, mock_instance):
        # Arrange
        # Mock repository methods
        mock_repository = mock_instance.return_value
        mock_repository.get_player.return_value = None
        # Create ServiceGame
        service_game = ServiceGame()

        # Act
        result = service_game.get_player_last_games('test1')

        # Assert
        self.assertFalse(result)
        mock_repository.get_player.assert_called_once_with('test1')

    @patch('service_game.RepositoryGame')
    def test_get_exist_player_last_games(self, mock_instance):
        # Arrange
        player = {'id': 1, 'name': 'test1', 'rating': 500}
        # Mock repository methods
        mock_repository = mock_instance.return_value
        mock_repository.get_player.return_value = player
        mock_repository.get_player1_last_games.return_value = \
            [{'result': 1,
              'date_start': '2022-01 22:33:05',
              'date_end': '2022-01 22:35:12',
              'rating_p1': 520}]
        mock_repository.get_player2_last_games.return_value = \
            [{'result': 1,
              'date_start': '2022-01-03 22:33:05',
              'date_end': '2022-01-03 22:35:12',
              'rating_p2': 500}]
        # Create ServiceGame
        service_game = ServiceGame()

        # Act
        result = service_game.get_player_last_games('test1')

        # Assert
        self.assertEqual(len(result), 2)
        mock_repository.get_player.assert_called_once_with('test1')
        mock_repository.get_player1_last_games.assert_called_once_with(player)
        mock_repository.get_player2_last_games.assert_called_once_with(player)


if __name__ == "__main__":
    unittest.main()
