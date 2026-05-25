from telebot import types
from telebot.types import Message
from config import buttons, states


def get_back_button():
    return types.KeyboardButton(text=buttons.BACK_BUTTON)


def main_menu_keyboard(ctx):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    games_button = types.KeyboardButton(text=buttons.GAME_MENU_BUTTON)
    service_button = types.KeyboardButton(text=buttons.SERVICE_MENU_BUTTON)
    keyboard.add(games_button, service_button)

    return keyboard