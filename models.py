from dataclasses import dataclass, fields
from datetime import datetime
from symtable import Class
from typing import Any, TypeVar, Type, Union

T = TypeVar('T')


def class_repr_converter(cls: Type[T], data, temp_data=None, many=True) -> Union[T, list[T]]:
    """ Convert data to dataclass objects. """

    result_list = temp_data if temp_data is not None else []

    if isinstance(data, list):
        for element in data:
            class_repr_converter(cls=cls, data=element, temp_data=result_list)

    elif hasattr(data, "keys"):
        record_dict = {}
        for field in fields(cls):
            if field.name not in data.keys():
                raise ValueError("missing required field '%s'" % field.name)
            if field.type is datetime:
                value = data[field.name]
                if isinstance(value, str):
                    value = datetime.fromisoformat(value)
                record_dict[field.name] = value
            else:
                record_dict[field.name] = data[field.name]
        result_list.append(cls(**record_dict))

    else:
        raise ValueError("data must be a list or dict")

    if not many and len(result_list) == 1:
        return result_list[0]

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


@dataclass
class ServiceResponse:
    success: bool
    message: str
    data: Any = None
