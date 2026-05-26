import keyboards
from config import states, misc
from core.context import RequestContext


def my_services_renderer(ctx: RequestContext, msg=None):
    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        f"In this menu you can create, view and run services",
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )
