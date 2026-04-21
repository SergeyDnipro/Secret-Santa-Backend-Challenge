from dataclasses import dataclass, fields
from datetime import datetime


def class_repr_converter(cls, data, temp_data=None):
    """ Convert data to dataclass objects. """

    result_list = temp_data if temp_data is not None else []

    if not isinstance(data, list) and not hasattr(data, 'keys'):
        raise ValueError("data must be a list or dict")

    if isinstance(data, list):
        for element in data:
            class_repr_converter(cls, element, result_list)
            return result_list

    record_dict = {}
    for field in fields(cls):
        if field.name not in data.keys():
            raise ValueError("missing required field '%s'" % field.name)
        record_dict[field.name] = data[field.name]
    result_list.append(cls(**record_dict))

    return result_list


@dataclass
class Game:
    id: int
    created_at: datetime
    creator_telegram_id: int
    game_name: str
    game_passcode: str
    game_locked: int
    game_completed: int
    players_count: int

@dataclass
class Player:
    player_id: int
    game_id: int
    created_at: datetime
    player_name: str
    player_telegram_id: int
    player_giver: str
    player_receiver: str
