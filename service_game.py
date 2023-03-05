from repository_game import RepositoryGame
from enum import Enum


class Point(Enum):
    WIN = 1
    LOSE = 0
    DRAW = 0.5


class ServiceGame:
    def __init__(self):
        self.repository = RepositoryGame("tic_tac_toe.db")

    def create_player(self, name):
        if self.repository.get_player(name) is None:
            self.repository.save_player(name)
            return True
        return False

    def save_result(self, engine):
        # creating players if they don't exist
        self.create_player(engine.player1)
        self.create_player(engine.player2)
        # get players from db
        player1 = self.repository.get_player(engine.player1)
        player2 = self.repository.get_player(engine.player2)
        # save result
        if player1 is not None and player2 is not None and \
                self.repository.save_game(player1['id'], player2['id'],
                                          engine.game_state,
                                          engine.date_start, engine.date_end,
                                          player1['rating'], player2['rating']):
            rating1, rating2 = self.update_players_rating(player1['rating'], player2['rating'], engine)
            if self.repository.update_player(player1['name'], rating1) \
                    and self.repository.update_player(player2['name'], rating2):
                return True
        return False

    def update_players_rating(self, rating1, rating2, engine):
        if engine.game_state == 0:
            rating1 = self.calculate_rating(rating1, rating2, Point.DRAW.value)
            rating2 = self.calculate_rating(rating2, rating1, Point.DRAW.value)
        elif engine.game_state == 1:
            rating1 = self.calculate_rating(rating1, rating2, Point.WIN.value)
            rating2 = self.calculate_rating(rating2, rating1, Point.LOSE.value)
        else:
            rating1 = self.calculate_rating(rating1, rating2, Point.LOSE.value)
            rating2 = self.calculate_rating(rating2, rating1, Point.WIN.value)
        return rating1, rating2

    @staticmethod
    def calculate_rating(rating1, rating2, point):
        math_expect = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
        return int(rating1 + 40 * (point - math_expect))

    def get_player_statistics(self, name):
        player = self.repository.get_player(name)
        statistics = None
        if player is not None:
            statistics = {
                'name': player['name'],
                'games': self.repository.get_player_games(player)['cnt'],
                'wins': self.repository.get_player_wins(player)['cnt'],
                'defeats': self.repository.get_player_defeats(player)['cnt'],
                'draws': self.repository.get_player_draws(player)['cnt'],
                'rating': player['rating']
            }
            statistics['percentage'] = statistics['wins'] / statistics['games'] * 100 \
                if statistics['wins'] != 0 and statistics['games'] != 0 else 0
        return statistics

    def get_player_last_games(self, name):
        player = self.repository.get_player(name)
        games = []
        if player is not None:
            list_games_from_p1 = self.repository.get_player1_last_games(player)
            for game in list_games_from_p1:
                games.append(f"{'Win' if game['result'] == 1 else 'Lose'}! Start date: {game['date_start'][:-7]}; "
                             f"End date: {game['date_end'][:-7]}; Rating after game: {game['rating_p1']}")
            list_games_from_p2 = self.repository.get_player2_last_games(player)
            for game in list_games_from_p2:
                games.append(f"{'Win' if game['result'] == 2 else 'Lose'}! Start date: {game['date_start'][:-7]}; "
                             f"End date: {game['date_end'][:-7]}; Rating after game: {game['rating_p2']}")
        return games

    def close_db(self):
        self.repository.close_connection()
