from typing import Union
from models import Game, ServiceResponse, class_repr_converter, Player
from core.db_driver import db
from config import misc
from tools import generate_passcode, serialize_game_list, serialize_game
from exceptions import game_exceptions
from config import message_templates


class GameService:

    def __init__(self, permission):
        self.permission = permission


    def create_new_game(self, *, creator_id: int, creator_username: str, max_players_qty: int) -> ServiceResponse:
        success = False
        new_game_class_repr = None

        try:
            if not self.permission.is_admin(creator_id):
                creator_games = db.get_games_by_creator(creator_id=creator_id)
                if len(creator_games) >= misc.MAX_GAMES:
                    response_msg = f"Max games quantity reached ({misc.MAX_GAMES})"
                    raise ValueError(response_msg)

            new_game_response = db.new_game(
                game_name=misc.BASE_GAME_NAME.lower(),
                creator_id=creator_id,
                creator_name=creator_username,
                game_passcode=generate_passcode(),
                max_players_qty=max_players_qty,
            )

            new_game_class_repr = class_repr_converter(
                cls=Game,
                data=new_game_response,
                many=False,
            )

            success = True
            response_msg = (f"New game created: {new_game_class_repr.game_name}. \n"
                            f"Passcode: {new_game_class_repr.game_passcode}")

        except ValueError as e:
            response_msg=str(e)

        return ServiceResponse(success=success, message=response_msg, data=new_game_class_repr)


    def join_game(self, *, game_name: str, game_passcode: str, player_name: str, player_telegram_id: int) -> ServiceResponse:

        try:
            game_instance = db.get_game_by_passcode(game_name=game_name, game_passcode=game_passcode)
            game_instance_class_repr = class_repr_converter(
                cls=Game,
                data=game_instance,
                many=False,
            )

            if not game_instance:
                raise game_exceptions.GameNotFoundError()

            if game_instance_class_repr.game_locked:
                raise game_exceptions.GameLockedError()

            game_id = game_instance_class_repr.id
            db.join_game_by_player(
                game_id=game_id,
                player_name=player_name,
                player_telegram_id=player_telegram_id,
            )
            message = message_templates.JOIN_GAME_SUCCESS(game_name=game_name)

        except game_exceptions.GameAppException as exc:
            message = str(exc)

        return ServiceResponse(success=True, message=message, data=None)


    def get_user_games(self, *, creator_id: int) -> ServiceResponse:
        success = False
        user_games_class_repr = None

        try:
            user_games_response = db.get_games_by_creator(creator_id=creator_id)

            user_games_class_repr = class_repr_converter(
                cls=Game,
                data=user_games_response
            )

            response_msg = serialize_game_list(user_games_class_repr)
            success = True

        except ValueError as e:
            response_msg=str(e)

        return ServiceResponse(success=success, message=response_msg, data=user_games_class_repr)


    def get_game_data(self, *, creator_id: int, game_name: str) -> ServiceResponse:
        success = False
        game_class_repr = None

        try:
            game_response = db.get_game(game_name=game_name)
            game_class_repr = class_repr_converter(
                cls=Game,
                data=game_response,
                many=False,
            )

            players_response = db.get_players_by_game_name(game_name=game_name)
            players_class_repr = class_repr_converter(
                cls=Player,
                data=players_response,
            )

            if (isinstance(game_class_repr, Game)
                    and (creator_id == game_class_repr.creator_telegram_id or self.permission.is_admin(creator_id))
            ):
                response_msg = serialize_game(
                    game_data=game_class_repr,
                    players=players_class_repr,
                )
                success = True

            else:
                response_msg = "No game found or you don't have access to game data."
                game_class_repr = None


        except ValueError as e:
            response_msg=str(e)

        return ServiceResponse(success=success, message=response_msg, data=game_class_repr)


    def draw_the_game(self, game_data: dict) -> Union[dict, str]:
        """
        Perform a Secret Santa draw for a game.
            - Shuffles receivers so no player gives a gift to themselves.
            - Assigns 'giver' and 'receiver' fields for each player.
            - Updates the game_data dict with the drawn results.
        """

        if isinstance(game_data, str):
            return game_data

        if game_data["game"][4]:
            return f"Game: {game_data['game'][2]} is already completed."

        game = {
            "id": game_data["game"][0],
            "created_at": game_data["game"][1],
            "game_name": game_data["game"][2],
            "game_locked": game_data["game"][3] or 1,
            "game_completed": game_data["game"][4] or 1,
        }

        players = [
            {
                "id": player[0],
                "name": player[1],
                "giver": player[2],
                "receiver": player[3],
                "user_chat_id": player[4]
            } for player in game_data["players"]
        ]

        receivers = players[:]

        for i in range(len(players)):
            if players[i]["id"] == receivers[i]["id"]:
                if i < len(players) - 1:
                    receivers[i], receivers[i + 1] = receivers[i + 1], receivers[i]
                else:
                    receivers[i], receivers[i - 1] = receivers[i - 1], receivers[i]


        for giver, receiver in zip(players, receivers):
            giver["receiver"] = receiver["name"]
            receiver["giver"] = giver["name"]

        game_data["players"] = players
        game_data["game"] = game

        return game_data
