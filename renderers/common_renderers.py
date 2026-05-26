import keyboards
from config import states, misc
from core.context import RequestContext


def welcome_game_renderer(ctx: RequestContext, msg=None):

    message_text = msg or f"Welcome to Secret Santa Game, {ctx.message.from_user.username}"

    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        message_text,
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )


def not_valid_input_renderer(ctx: RequestContext, msg=None):
    error_message = msg or "Unexpected input values..."
    state = ctx.session.get_state()

    ctx.bot.send_message(
        ctx.message.chat.id,
        error_message,
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )
