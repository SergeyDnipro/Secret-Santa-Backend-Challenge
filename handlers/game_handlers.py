import renderers
from handlers import common_handlers
from config import states, buttons, misc
from service import state


def my_games_menu_handler(ctx):
    command = ctx.message.text.strip().lower()

    if command == buttons.NEW_GAME_BUTTON.lower():
        new_state = ctx.session.go_forward(states.NEW_GAME)
    elif command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return
    else:
        new_state = states.NOT_VALID_INPUT

    renderer = renderers.STATE_RENDERERS.get(new_state)
    renderer(ctx)


def new_game_handler(ctx):
    command = ctx.message.text.strip().lower()

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return

    try:
        value = int(command)
        if 30 < value < 3:
            new_state = ctx.session.go_forward(states.NEW_GAME_CREATED)
            msg = None
        else:
            new_state = states.NOT_VALID_INPUT
            msg = f"Players quantity must be between 3 and 30. Current value is: {value}"
    except ValueError:
        new_state = states.NOT_VALID_INPUT
        msg = "Only digits allowed"

    renderer = renderers.STATE_RENDERERS.get(new_state)
    renderer(ctx, msg=msg)


def new_game_created_handler(ctx):
    pass


def incorrect_input_handler(bot, message, session: state.UserState):
    pass
