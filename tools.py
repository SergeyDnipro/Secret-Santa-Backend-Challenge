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

        final_row += (
            f"Date: {game_date}\n"
            f"ID: {game_name} | "
            f"Passcode: {game_passcode}\n"
            f"Players: {players_qty} | "
            f"Status: {game_status}\n\n"
        )

    return final_row


def serialize_game_data(*, game: Game, players: List[Player]):
    """ Create output string to display extended info for game """

    game_name = game.game_name
    game_date = game.created_at.strftime("%B %d, %Y")
    game_passcode = game.game_passcode
    locked = "Yes" if game.game_locked else "No"
    completed = "Yes" if game.game_completed else "No"

    msg = (
        f"Game ID: {game_name}\n\n"
        f"Passcode: {game_passcode}\n" 
        f"Created: {game_date}\n"
        f"Locked: {locked}\n"
        f"Completed: {completed}\n\n"
        f"Players:\n"
    )

    if players:
        for number, player in enumerate(players, start=1):

            receiver = player.player_receiver or "None"
            msg += f"{number}. {player.player_name} -> giver to: {receiver}\n"
    else:
        msg += "No players in the game yet"

    return msg


def generate_passcode(passcode_length: int = 6) -> str:
    """ Generate random passcode for game join allowing. """
    passcode_symbols = string.ascii_letters + string.digits

    passcode = ''.join(secrets.choice(passcode_symbols) for _ in range(passcode_length))

    return passcode
