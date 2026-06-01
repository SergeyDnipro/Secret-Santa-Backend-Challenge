import secrets
import string
from typing import List, Tuple, Union
from models import Game, Player


def serialize_game_list(game_list: List[Game]) -> str:
    """ Create output string for displaying the list of games in Telegram """

    if not game_list:
        return "No games found"

    final_row = ""
    for game_data in game_list:
        if not game_data.game_locked and not game_data.game_completed:
            game_status = "Open"
        elif game_data.game_locked and not game_data.game_completed:
            game_status = "Closed"
        else:
            game_status = "Completed"

        game_date = game_data.created_at.strftime("%B %d, %Y")
        game_name = game_data.game_name
        game_passcode = game_data.game_passcode
        players_qty = game_data.players_count
        max_players_qty = game_data.max_players_qty

        final_row += (
            f"Date: {game_date}\n"
            f"ID: {game_name} | "
            f"Passcode: {game_passcode}\n"
            f"Players: {players_qty}/{max_players_qty} | "
            f"Status: {game_status}\n\n"
        )

    return final_row


def serialize_game(game_data: Game, players: List[Player]) -> Union[dict, str]:
    """ Create output string to display extended info for game """

    locked = "Yes" if game_data.game_locked else "No"
    completed = "Yes" if game_data.game_completed else "No"
    game_date = game_data.created_at.strftime("%B %d, %Y")

    msg = (
        f"ID: {game_data.game_name}\n\n"
        f"Created: {game_date}\n"
        f"Locked: {locked}\n"
        f"Completed: {completed}\n"
        f"Total players: {game_data.players_count}\n"
        f"Max players: {game_data.max_players_qty}\n\n"
        f"Players:\n"
    )

    for number, player in enumerate(players, start=1):

        receiver = player.player_receiver or "None"
        msg += f"{number}. {player.player_name} -> giver to: {receiver}\n"

    return msg


def generate_passcode(passcode_length: int = 6) -> str:
    """ Generate random passcode for game join allowing. """
    passcode_symbols = string.ascii_letters + string.digits

    passcode = ''.join(secrets.choice(passcode_symbols) for _ in range(passcode_length))

    return passcode
