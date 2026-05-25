import renderers
from handlers import common_handlers
from config import states, buttons, misc
from service import state


def my_services_menu_handler(ctx):
    command = ctx.message.text.strip().lower()

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
