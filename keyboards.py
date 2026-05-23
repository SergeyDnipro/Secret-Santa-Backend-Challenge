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


def my_service_keyboard(ctx):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    get_game_data_button = types.KeyboardButton(text=buttons.GET_GAME_DATA_BUTTON)
    list_games_button = types.KeyboardButton(text=buttons.LIST_CREATORS_BUTTON)
    keyboard.add(list_games_button, get_game_data_button)

    if ctx.game_service.permission.is_admin(ctx.message.from_user.id):
        purge_database_button = types.KeyboardButton(text=buttons.CLEAR_DATABASE_BUTTON)
        keyboard.add(purge_database_button)

    back_button = get_back_button()
    keyboard.add(back_button)

    return keyboard


def get_main_interface_keyboard(message:Message, ids=None):
    if ids is None:
        ids = []

    admin_role = message.from_user.id in ids
    keyboard = admin_main_keyboard() if admin_role else user_main_keyboard()
    return keyboard


def admin_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    new_game_button = types.KeyboardButton(text=buttons.NEW_GAME_BUTTON)
    join_game_button = types.KeyboardButton(text=buttons.JOIN_GAME_BUTTON)
    lock_game_button = types.KeyboardButton(text=buttons.LOCK_GAME_BUTTON)
    keyboard.add(new_game_button, join_game_button, lock_game_button)

    start_game_button = types.KeyboardButton(text=buttons.START_GAME_BUTTON)
    keyboard.add(start_game_button)

    get_game_data_button = types.KeyboardButton(text=buttons.GET_GAME_DATA_BUTTON)
    list_games_button = types.KeyboardButton(text=buttons.LIST_CREATORS_BUTTON)
    keyboard.add(list_games_button, get_game_data_button)

    export_results_button = types.KeyboardButton(text=buttons.EXPORT_GAME_BUTTON)
    keyboard.add(export_results_button)

    purge_database_button = types.KeyboardButton(text=buttons.CLEAR_DATABASE_BUTTON)
    keyboard.add(purge_database_button)

    return keyboard


def user_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    join_game = types.KeyboardButton(text=buttons.JOIN_GAME_BUTTON)
    keyboard.add(join_game)
    return keyboard


def clear_database_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    confirm_button = types.KeyboardButton(text=buttons.YES_BUTTON)
    reject_button = types.KeyboardButton(text=buttons.NO_BUTTON)
    keyboard.add(confirm_button, reject_button)
    return keyboard


STATE_KEYBOARDS = {
    states.MAIN_MENU: main_menu_keyboard,
    states.MY_GAMES_MENU: my_games_keyboard,
    states.SERVICE_MENU: my_service_keyboard,
    states.NEW_GAME: new_game_creating_keyboard,
}