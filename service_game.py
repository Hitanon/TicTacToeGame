from repository_game import RepositoryGame
from enum import Enum


class Point(Enum):
    WIN = 1
    LOSE = 0
    DRAW = 0.5


class ServiceGame:
    def __init__(self):
        self.repository = RepositoryGame("test.db")
        self.ratio = 40
        self.math_expect = 0

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
        if self.repository.save_game(player1['id'], player2['id'], engine.game_state,
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

    def calculate_rating(self, rating1, rating2, point):
        self.math_expect = 1 / (1 + 10 ** (rating1 - rating2 / 400))
        return rating1 + self.ratio * (self.math_expect - point)

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
                'date_first': self.repository.get_player_date_first_game(player)['date_start'],
                'date_last': self.repository.get_player_date_last_game(player)['date_start'],
                'rating': player['rating']
            }
            statistics['percentage'] = statistics['wins'] / statistics['games'] * 100 \
                if statistics['wins'] != 0 and statistics['games'] != 0 else 0
        return statistics

    def close_db(self):
        self.repository.close_connection()
