import sqlite3
from datetime import datetime
from core.db_tools import transactional
from typing import List, Union
from dataclasses import dataclass, fields
from exceptions.game_exceptions import PlayerAlreadyJoinedError, GameFullError


class SQLiteDatabaseConnection:
    def __init__(self, *, database_name: str):
        self.database_name = database_name
        self.create_check_table()

    @staticmethod
    def execute_query(*, conn: sqlite3.Connection, query: str, params=None, many=False, fetchone_result=False):
        """Execute the SQL query with optional parameters and return results if available."""
        cursor = conn.cursor()
        if many:
            cursor.executemany(query, params)
        elif params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()

        if cursor.description:
            if fetchone_result:
                return cursor.fetchone()
            return cursor.fetchall()
        return cursor.lastrowid


    @transactional
    def create_check_table(self, *, conn: sqlite3.Connection):
        """Create the games and players tables if it does not exist."""

        query = """
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            creator_telegram_id INTEGER,
            creator_name TEXT,
            game_name TEXT NOT NULL UNIQUE,
            game_passcode TEXT NOT NULL,
            game_locked INTEGER DEFAULT 0,
            game_completed INTEGER DEFAULT 0,
            players_count INTEGER DEFAULT 0,
            max_players_qty INTEGER DEFAULT 10
         );
        """
        self.execute_query(conn=conn, query=query)

        query = """
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            player_name TEXT NOT NULL,
            player_telegram_id INTEGER NOT NULL,
            player_giver TEXT DEFAULT NULL,
            player_receiver TEXT DEFAULT NULL,
            FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
            UNIQUE (game_id, player_name),
            UNIQUE (game_id, player_telegram_id)
         );
        """
        self.execute_query(conn=conn, query=query)


    def delete_all_records(self):
        """ Purge 'games' tables (and related 'players') """

        query = """
        DELETE FROM games;
        """
        self.execute_query(query)
        return "DB cleared"


    @transactional
    def new_game(
            self,
            *,
            game_name: str,
            creator_id: int,
            creator_name: str,
            game_passcode: str,
            max_players_qty: int,
            conn: sqlite3.Connection,
    ):
        """ Create the new game and return its name_id to telegram """

        query = """
        INSERT INTO games (game_name, creator_telegram_id, creator_name, game_passcode, max_players_qty)
        VALUES (:game_name, :creator_telegram_id, :creator_name, :game_passcode, :max_players_qty);
        """

        params = {
            "game_name": game_name,
            "creator_telegram_id": creator_id,
            "creator_name": creator_name,
            "game_passcode": game_passcode,
            "max_players_qty": max_players_qty,
        }

        game_id = self.execute_query(conn=conn, query=query, params=params)

        # Update record (with following 'game_id') with 'new_game_name'
        new_game_name = f"{game_name}_{game_id}"
        update_query = """
        UPDATE games
        SET game_name = :new_game_name
        WHERE id = :game_id;
        """

        update_params = {"new_game_name": new_game_name, "game_id": game_id}
        self.execute_query(conn=conn, query=update_query, params=update_params, fetchone_result=True)

        get_new_game_query = """
        SELECT games.* FROM games
        WHERE id = :game_id;
        """
        new_game_instance = self.execute_query(conn=conn, query=get_new_game_query, params={"game_id": game_id})

        return new_game_instance


    def get_all_games(self) -> List[tuple]:
        """ Get all games in DB, including qty of players in every game (Admin role needed) """

        query = """
        SELECT games.*, COUNT(players.player_id) AS players_count
        FROM games
        LEFT JOIN players ON games.id = players.game_id
        GROUP BY games.id;
        """

        result = self.execute_query(query)
        return result


    @transactional
    def get_games_by_creator(self, creator_id: int, conn: sqlite3.Connection) -> List[tuple]:
        """ Get all games in DB, including qty of players in every game (for requested creator ID) """

        query = """
        SELECT games.*, COUNT(players.player_id) AS players_count
        FROM games
        LEFT JOIN players ON games.id = players.game_id
        WHERE games.creator_telegram_id = :creator_id
        GROUP BY games.id;
        """

        params = {"creator_id": creator_id}

        result = self.execute_query(conn=conn, query=query, params=params)
        return result


    @transactional
    def get_game_by_passcode(self, game_name: str, game_passcode: str, conn: sqlite3.Connection):
        """ Get game data by game name and passcode """
        query = """
        SELECT games.*
        FROM games
        WHERE game_name = :game_name AND game_passcode = :game_passcode;
        """

        params = {"game_name": game_name, "game_passcode": game_passcode}

        result = self.execute_query(conn=conn, query=query, params=params)

        return result


    @transactional
    def get_game(self, game_name: str, conn: sqlite3.Connection) -> Union[dict, None]:
        """ Get game data """
        query = """
        SELECT games.*
        FROM games
        WHERE game_name = :game_name;
        """

        params = {"game_name": game_name}

        result = self.execute_query(conn=conn, query=query, params=params)

        return result


    @transactional
    def get_players_by_game_name(self, game_name: str, conn: sqlite3.Connection) -> Union[dict, None]:
        """ Get players data regarding game name """


        query = """
        SELECT players.*
        FROM players
        LEFT JOIN games ON players.game_id = games.id
        WHERE games.game_name = :game_name
        GROUP BY players.player_id;
        """

        get_params = {"game_name": game_name}
        players_list = self.execute_query(conn=conn, query=query, params=get_params)

        return players_list
        # return {"game": game["result"], "players": players_list}


    def lock_game_by_name(self, game_name: str) -> str:
        """ Lock game for new player registration """

        game = self.get_game(game_name)

        if not game["status"]:
            return game["message"]

        query = """
        UPDATE games
        SET game_locked = 1
        WHERE game_name = :game_name;
        """

        update_params = {"game_name": game_name}
        self.execute_query(query, update_params)

        return f"Game: {game_name} has been locked"





    def join_game_by_name(self, game_name: str, player_name: str, player_telegram_id: int) -> str:
        """ Join open for registration game. Check constraints """

        game = self.get_game(game_name)
        if not game["status"]:
            return game["message"]

        game_id = game["result"][0]

        try:
            query = """
            INSERT INTO players (game_id, player_name, player_telegram_id)
            VALUES (:game_id, :player_name, :player_telegram_id);
            """

            insert_params = {
                "game_id": game_id,
                "player_name": player_name,
                "player_telegram_id": player_telegram_id
            }

            self.execute_query(query, insert_params)
            return f"Player: {player_name} joined game: {game_name}"

        except sqlite3.IntegrityError as e:
            return f"You can join a game: {game_name} only once"


    def bulk_update_game_and_players(self, game_data: dict):
        """ Bulk update 'games' and 'players' tables due the drawing results """

        query = """
                UPDATE games
                SET
                    game_locked = :locked,
                    game_completed = :completed
                WHERE id = :id;
                """

        game_id = game_data["game"]["id"]
        locked = game_data["game"]["game_locked"]
        completed = game_data["game"]["game_completed"]

        params = {"id": game_id, "locked": locked, "completed": completed}
        self.execute_query(query, params)

        query = """
                UPDATE players
                SET
                    player_giver = :giver,
                    player_receiver = :receiver
                WHERE player_id = :id;
                """

        self.execute_query(query, game_data["players"], many=True)

        return {"message": "Game drawn successfully"}


db = SQLiteDatabaseConnection(database_name='santa.sqlite3')
