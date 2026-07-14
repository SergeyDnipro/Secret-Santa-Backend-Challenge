from core.context import RequestContext
from config import message_templates, misc


def welcome_message(ctx: RequestContext):
    return message_templates.WELCOME_MESSAGE.format(username=ctx.message.from_user.username)


def game_menu_message(ctx: RequestContext):
    return message_templates.GAME_MENU_MESSAGE


def new_game_message(ctx: RequestContext):
    return message_templates.NEW_GAME_MESSAGE.format(
        max_players=misc.MAX_PLAYERS,
        default_max_players=misc.DEFAULT_MAX_PLAYERS
    )

def new_game_description_message(ctx: RequestContext):
    return message_templates.NEW_GAME_DESCRIPTION_MESSAGE


def new_game_confirmation_message(ctx: RequestContext):
    return message_templates.NEW_GAME_CONFIRMATION_MESSAGE


def join_game_start_message(ctx: RequestContext):
    return message_templates.JOIN_GAME_ID_MESSAGE


def join_game_passcode_message(ctx: RequestContext):
    return message_templates.JOIN_GAME_PASSCODE_MESSAGE


def service_menu_message(ctx: RequestContext):
    return message_templates.SERVICE_MENU_MESSAGE


def get_game_data_id_message(ctx: RequestContext):
    return message_templates.GET_GAME_ID_MESSAGE
