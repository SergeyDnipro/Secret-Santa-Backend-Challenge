from core.context import RequestContext
from config import message_templates


def welcome_message(ctx: RequestContext):
    return message_templates.WELCOME_MESSAGE.format(username=ctx.message.from_user.username)


def game_menu_message(ctx: RequestContext):
    return message_templates.GAME_MENU_MESSAGE


def service_menu_message(ctx: RequestContext):
    return message_templates.SERVICE_MENU_MESSAGE