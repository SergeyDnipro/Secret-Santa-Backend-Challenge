import keyboards
from config import states, misc
from core.context import RequestContext
from models import StateDefinition


def welcome_game_renderer(ctx: RequestContext, state_data: StateDefinition, msg=None):
    # username = ctx.message.from_user.username or ctx.message.from_user.first_name
    #
    # message_text = msg or f"Welcome to Secret Santa Game, {username}"

    # state = ctx.session.get_state()
    message = state_data.default_message(ctx) or msg
    keyboard = state_data.keyboard(ctx)
    ctx.bot.send_message(
        ctx.message.chat.id,
        message,
        reply_markup=keyboard
    )


def not_valid_input_renderer(ctx: RequestContext, msg=None):
    error_message = msg or "Unexpected input values..."
    state = ctx.session.get_state()

    ctx.bot.send_message(
        ctx.message.chat.id,
        error_message,
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )
