from typing import List, Tuple, Union


def serialize_game_list(game_list: List[tuple]):
    final_row = ""
    for game_data in game_list:
        if not game_data[3] and not game_data[4]:
            game_status = "Open"
        elif game_data[3] and not game_data[4]:
            game_status = "Closed"
        else:
            game_status = "Completed"

        game_date = game_data[1].split()[0]
        game_name = game_data[2]
        players_qty = game_data[5]

        final_row += f"Date: {game_date} | ID: {game_name} | Players: {players_qty} | Status: {game_status}\n"

    if not game_list:
        final_row = "No games found"

    return final_row


def serialize_game(game_result: Union[dict, str]):
    if isinstance(game_result, str):
        return game_result

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
        msg += f"{number}. {player[1]} -> gives to: {receiver}\n"

    return msg


def players_to_dict(game_data: dict):
    if isinstance(game_data, str):
        return game_data

    players = [
        {
            "id": player[0],
            "name": player[1],
            "giver": player[2],
            "receiver": player[3],
        } for player in game_data["players"]
    ]
    players = [
        {'id': 1, 'name': 'Sergey', 'giver': None, 'receiver': None},
        {'id': 2, 'name': 'Alex', 'giver': None, 'receiver': None},
        {'id': 3, 'name': 'Anna', 'giver': None, 'receiver': None}
    ]
    receivers = players[:]
    for i in range(len(players)):
        if players[i]["id"] == receivers[i]["id"]:
            if i < len(players) - 1:
                receivers[i], receivers[i + 1] = receivers[i + 1], receivers[i]
            else:
                receivers[i], receivers[i - 1] = receivers[i - 1], receivers[i]


    print(players)
    print(receivers)
    for giver, receiver in zip(players, receivers):
        giver["receiver"] = receiver["name"]
        receiver["giver"] = giver["name"]

    print(players)
    return players

