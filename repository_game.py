import sqlite3 as sq

script_creating_players_table = \
    """
    CREATE TABLE IF NOT EXISTS players
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rating INTEGER DEFAULT 100)
    """

script_creating_games_table = \
    """
    CREATE TABLE IF NOT EXISTS games
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_p1 INTEGER NOT NULL,
    id_p2 INTEGER NOT NULL,
    result INTEGER NOT NULL DEFAULT 0,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    rating_p1 INTEGER NOT NULL DEFAULT 0,
    rating_p2 INTEGER NOT NULL DEFAULT 0)
    """


class RepositoryGame:
    def __init__(self, db_file):
        self.db = db_file
        self.conn = None
        self.cur = None
        self.conn = self.create_connection()
        try:
            self.conn.row_factory = sq.Row
            self.cur = self.conn.cursor()
            self.cur.execute(script_creating_players_table)
            self.cur.execute(script_creating_games_table)
        except sq.Error as e:
            print(f"Error creating tables: {e}")

    def create_connection(self):
        try:
            conn = sq.connect(self.db)
            print(f"Connection to SQLite database {self.db} successful")
            return conn
        except sq.Error as e:
            print(f"Error connecting to SQLite database {self.db}: {e}")
            return None

    def save_player(self, name):
        try:
            self.cur.execute("INSERT INTO players (name) VALUES(?)", (name,))
            self.conn.commit()
        except sq.Error as e:
            print(f"Error saving player {name}: {e}")
            return False
        return True

    def save_game(self, id_p1, id_p2, result, date_start, date_end, rating1, rating2):
        try:
            self.cur.execute("""
            INSERT INTO games (id_p1, id_p2, result, date_start, date_end, rating_p1, rating_p2)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """, (id_p1, id_p2, result, date_start, date_end, rating1, rating2))
            self.conn.commit()
        except sq.Error as e:
            print(f"Error saving game: {e}")
            return False
        print("Saving game result successful")
        return True

    def get_player(self, name):
        self.cur.execute("SELECT * from players WHERE name = ?", (name,))
        return self.cur.fetchone()

    def update_player(self, name, rating):
        try:
            self.cur.execute("""
            UPDATE players SET rating = ? WHERE name == ?
            """, (rating, name))
            self.conn.commit()
        except sq.Error as e:
            print(f"Error updating rating of player {name}: {e}")
            return False
        print(f"Update player {name} rating to {rating}")
        return True

    def get_player_games(self, player):
        self.cur.execute("""SELECT count() AS cnt from games 
                            WHERE id_p1 == ? or id_p2 == ?""", (player['id'], player['id']))
        return self.cur.fetchone()

    def get_player_wins(self, player):
        self.cur.execute("""SELECT count() AS cnt from games 
                            WHERE id_p1 == ? AND result == 1
                            OR id_p2 == ? AND result == 2""", (player['id'], player['id']))
        return self.cur.fetchone()

    def get_player_defeats(self, player):
        self.cur.execute("""SELECT count() AS cnt from games 
                            WHERE id_p1 == ? AND result == 2
                            OR id_p2 == ? AND result == 1""", (player['id'], player['id']))
        return self.cur.fetchone()

    def get_player_draws(self, player):
        self.cur.execute("""SELECT count() AS cnt from games 
                            WHERE id_p1 == ? AND result == 0
                            OR id_p2 == ? AND result == 0""", (player['id'], player['id']))
        return self.cur.fetchone()

    def get_player_date_first_game(self, player):
        self.cur.execute("""SELECT date_start FROM games
                            WHERE id_p1 == ? or id_p2 == ?
                            ORDER BY date_start
                            LIMIT 1""", (player['id'], player['id']))
        return self.cur.fetchone()

    def get_player_date_last_game(self, player):
        self.cur.execute("""SELECT date_start FROM games
                            WHERE id_p1 == ? or id_p2 == ?
                            ORDER BY date_start DESC
                            LIMIT 1""", (player['id'], player['id']))
        return self.cur.fetchone()

    def close_connection(self):
        self.conn.close()
