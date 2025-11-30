from typing import List, Union


def draw_the_game(game_data: dict) -> Union[dict, str]:
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