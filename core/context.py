import telebot
from dataclasses import dataclass, fields
from telebot.types import Message
from service.game import GameService
from service.state import UserState


@dataclass
class RequestContext:
    bot: telebot.TeleBot
    message: Message
    session: UserState
    game_service: GameService
