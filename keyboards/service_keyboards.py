from telebot import types
from telebot.types import Message
from config import buttons, states
from core.context import RequestContext
from keyboards.common_keyboards import get_back_button


def my_service_keyboard(ctx: RequestContext):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    get_game_data_button = types.KeyboardButton(text=buttons.GET_GAME_DATA_BUTTON)
    list_games_button = types.KeyboardButton(text=buttons.LIST_GAMES_BUTTON)
    keyboard.add(list_games_button, get_game_data_button)

    if ctx.game_service.permission.is_admin(ctx.message.from_user.id):
        purge_database_button = types.KeyboardButton(text=buttons.CLEAR_DATABASE_BUTTON)
        keyboard.add(purge_database_button)

    back_button = get_back_button()
    keyboard.add(back_button)

    return keyboard
