import keyboards
from config import states, misc
from core.context import RequestContext


def my_services_renderer(ctx: RequestContext, msg=None):
    state = ctx.session.get_state()
    msg = msg or (f"Service menu allow to view, delete own games, "
                  f"export results.")
    ctx.bot.send_message(
        ctx.message.chat.id,
        msg,
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )


def get_game_data_renderer(ctx: RequestContext, msg=None):
    state = ctx.session.get_state()