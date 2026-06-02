import renderers
from handlers import common_handlers
from config import states, buttons, misc
from service import state
from core.context import RequestContext


def my_games_menu_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()
    msg = None

    if command == buttons.NEW_GAME_BUTTON.lower():
        new_state = ctx.session.go_forward(states.NEW_GAME_STARTS)
    elif command == buttons.JOIN_GAME_BUTTON.lower():
        new_state = ctx.session.go_forward(states.JOIN_GAME_START)
        msg = f"Enter game name: "
    elif command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return
    else:
        new_state = states.NOT_VALID_INPUT

    renderer = renderers.STATE_RENDERERS.get(new_state)
    renderer(ctx, msg=msg)


def new_game_creating_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return

    try:
        value = int(command)
        if 30 >= value >= 3:
            ctx.session.set_data(misc.MAX_PLAYERS_KEY, value)
            new_state = ctx.session.go_forward(states.NEW_GAME_CREATED)
            response_msg = f"Creating game with {value} max players."
        else:
            new_state = states.NOT_VALID_INPUT
            response_msg = f"Players quantity must be between 3 and 30. Current value is: {value}"
    except ValueError:
        new_state = states.NOT_VALID_INPUT
        response_msg = "Only digits allowed"

    renderer = renderers.STATE_RENDERERS.get(new_state)
    renderer(ctx, msg=response_msg)


def new_game_confirmation_handler(ctx: RequestContext):
    max_players_qty = ctx.session.get_data(misc.MAX_PLAYERS_KEY)
    command = ctx.message.text.strip().lower()
    response_msg = None

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return

    elif command == buttons.CONFIRM_BUTTON.lower():
        tg_username = ctx.message.from_user.username
        tg_first_name = ctx.message.from_user.first_name
        creator_username = tg_username or tg_first_name
        response = ctx.game_service.create_new_game(
            creator_id=ctx.message.from_user.id,
            creator_username=creator_username,
            max_players_qty=max_players_qty
        )
        response_msg = response.message
        ctx.session.clear_state()
        current_state = ctx.session.get_state()
    else:
        current_state = states.NOT_VALID_INPUT

    renderer = renderers.STATE_RENDERERS.get(current_state)
    renderer(ctx, msg=response_msg)


def join_game_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return

    ctx.session.set_data(misc.GAME_NAME_KEY, command)
    new_state = ctx.session.go_forward(states.JOIN_GAME_START)
    msg = f"Enter passcode: "



def join_game_passcode_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.fallback_handler(ctx)
        return

    ctx.session.set_data(misc.GAME_NAME_KEY, command)

def incorrect_input_handler(bot, message, session: state.UserState):
    pass
