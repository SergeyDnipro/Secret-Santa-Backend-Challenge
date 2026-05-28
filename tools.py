import secrets
import string
from typing import List, Tuple, Union
from models import Game


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


def serialize_game(game_result: Game):
    """ Create output string to display extended info for game """

    if not game_result:
        return "No game found"

    game_data = game_result["game"]
    players_data = game_result["players"]
    locked = "Yes" if game_data[3] else "No"
    completed = "Yes" if game_data[4] else "No"

    msg = (
        f"Game: {game_data[2]}\n\n"
        f"Created: {game_data[1]}\n"
        f"Locked: {locked}\n"
        f"Completed: {completed}\n\n"
        f"Players:\n"
    )

    for number, player in enumerate(players_data, start=1):

        receiver = player[3] if player[3] else "None"
        msg += f"{number}. {player[1]} -> giver to: {receiver}\n"

    return msg


def generate_passcode(passcode_length: int = 6) -> str:
    """ Generate random passcode for game join allowing. """
    passcode_symbols = string.ascii_letters + string.digits

    passcode = ''.join(secrets.choice(passcode_symbols) for _ in range(passcode_length))

    return passcode
