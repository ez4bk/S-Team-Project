from config.sql_query.client_query import show_top_game
from lib.base_lib.sql.sql_utils import SqlUtils
from src.model.store_game import StoreGame

sql_utils = SqlUtils()


def get_top_game_query():
    res = None
    games = []

    try:
        res = sql_utils.sql_exec(show_top_game.format(10), 1)
    except Exception as e:
        return 'Fetch game store failed!'
    if res is None or res == []:
        return games
    try:
        for a in res:
            game = StoreGame(a[0], a[1], a[2], a[3], a[4], a[5])
            games.append(game)
        # self.top_games = games
        return games
    except Exception:
        return "Game initialization failed!"
