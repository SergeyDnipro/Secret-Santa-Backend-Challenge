from models import StateDefinition
from core.context import RequestContext


def common_renderer(ctx: RequestContext, state_data: StateDefinition, msg=None):
    message = state_data.default_message(ctx) if msg is None else msg
    keyboard = state_data.keyboard(ctx)
    ctx.bot.send_message(
        ctx.message.chat.id,
        message,
        reply_markup=keyboard
    )