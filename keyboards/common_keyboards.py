from telebot import types
from telebot.types import Message
from config import buttons, states
from core.context import RequestContext


def get_back_button():
    return types.KeyboardButton(text=buttons.BACK_BUTTON)


def main_menu_keyboard(ctx: RequestContext):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    games_button = types.KeyboardButton(text=buttons.GAME_MENU_BUTTON)
    service_button = types.KeyboardButton(text=buttons.SERVICE_MENU_BUTTON)
    keyboard.add(games_button, service_button)

    return keyboard


def backward_keyboard(ctx: RequestContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = get_back_button()
    keyboard.add(back_button)

    return keyboard
