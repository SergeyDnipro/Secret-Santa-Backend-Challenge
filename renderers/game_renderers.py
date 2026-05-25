import keyboards
from config import states, misc


def my_games_renderer(ctx, msg=None):
    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        f"In this menu you can create, view and run games",
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )


def new_game_creating_renderer(ctx, msg=None):
    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        f"Enter max players quantity from 3 to 30 (default {misc.MAX_PLAYERS})",
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )


def new_game_created_renderer(ctx, msg=None):
    msg = msg
    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        msg,
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )
