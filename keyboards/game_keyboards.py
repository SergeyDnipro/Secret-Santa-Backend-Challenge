from telebot import types
from telebot.types import Message
from config import buttons, states
from keyboards.common_keyboards import get_back_button


def my_games_keyboard(ctx):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    new_game_button = types.KeyboardButton(text=buttons.NEW_GAME_BUTTON)
    join_game_button = types.KeyboardButton(text=buttons.JOIN_GAME_BUTTON)
    keyboard.add(new_game_button, join_game_button)

    back_button = get_back_button()
    keyboard.add(back_button)

    return keyboard


def new_game_creating_keyboard(ctx):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = get_back_button()
    keyboard.add(back_button)

    return keyboard


def new_game_confirmation_keyboard(ctx):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    new_game_confirm_button = types.KeyboardButton(text=buttons.CONFIRM_BUTTON)
    back_button = get_back_button()
    keyboard.add(new_game_confirm_button, back_button)

    return keyboard
