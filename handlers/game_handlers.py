import models
import renderers
from handlers import common_handlers
from config import states, buttons, misc
from service import state, game
# from service.game import RequestContext


def my_games_menu_handler(ctx):
    command = ctx.message.text.strip().lower()

    if command == buttons.NEW_GAME_BUTTON.lower():
        new_state = ctx.session.go_forward(states.NEW_GAME_STARTS)
    elif command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return
    else:
        new_state = states.NOT_VALID_INPUT

    renderer = renderers.STATE_RENDERERS.get(new_state)
    renderer(ctx)


def new_game_creating_handler(ctx):
    command = ctx.message.text.strip().lower()

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return

    try:
        value = int(command)
        if 30 >= value >= 3:
            ctx.session.set_data(misc.MAX_PLAYERS_KEY, value)
            new_state = ctx.session.go_forward(states.NEW_GAME_CREATED)
            msg = f"Creating game with {value} max players."
        else:
            new_state = states.NOT_VALID_INPUT
            msg = f"Players quantity must be between 3 and 30. Current value is: {value}"
    except ValueError:
        new_state = states.NOT_VALID_INPUT
        msg = "Only digits allowed"

    renderer = renderers.STATE_RENDERERS.get(new_state)
    renderer(ctx, msg=msg)


def new_game_confirmation_handler(ctx: models.RequestContext):
    max_players_qty = ctx.session.get_data(misc.MAX_PLAYERS_KEY)
    command = ctx.message.text.strip().lower()
    msg = None

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return

    elif command == buttons.CONFIRM_BUTTON.lower():
        creator_username = ctx.message.from_user.username or ' '.join(ctx.message.from_user.first_name)
        response = ctx.game_service.create_new_game(
            creator_id=ctx.message.from_user.id,
            creator_username=ctx.message.from_user.username,
            max_players_qty=max_players_qty
        )
        msg = response.message
        ctx.session.clear_state()
    else:


    current_state = ctx.session.get_state()
    renderer = renderers.STATE_RENDERERS.get(current_state)
    renderer(ctx, msg=msg)


def incorrect_input_handler(bot, message, session: state.UserState):
    pass
