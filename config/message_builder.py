from core.context import RequestContext
from config import message_templates


def welcome_message(ctx: RequestContext):
    return message_templates.WELCOME_MESSAGE.format(username=ctx.message.from_user.username)
