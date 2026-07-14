import renderers
from handlers import common_handlers
from config import states, buttons, misc, state_instances, message_templates
from core.context import RequestContext


def my_games_menu_handler(ctx: RequestContext):

    command = ctx.message.text.strip().lower()
    current_state = ctx.session.get_state()
    msg = None

    if command == buttons.NEW_GAME_BUTTON.lower():
        current_state = ctx.session.go_forward(states.NEW_GAME_STARTS)
    elif command == buttons.JOIN_GAME_BUTTON.lower():
        current_state = ctx.session.go_forward(states.JOIN_GAME_START)
    elif command == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return
    else:
        msg = states.NOT_VALID_INPUT

    state_ui_data = state_instances.STATE_DEFINITIONS[current_state]

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )


def new_game_creating_handler(ctx: RequestContext):

    command = ctx.message.text.strip().lower()
    current_state = ctx.session.get_state()
    msg = None

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return

    elif command == buttons.DEFAULT_PLAYERS_QTY.lower():

        ctx.session.set_data(misc.MAX_PLAYERS_KEY, misc.MAX_PLAYERS)
        current_state = ctx.session.go_forward(states.NEW_GAME_DESCRIPTION)

    else:

        try:
            value = int(command)
            if misc.MAX_PLAYERS >= value >= 3:
                ctx.session.set_data(misc.MAX_PLAYERS_KEY, value)
                current_state = ctx.session.go_forward(states.NEW_GAME_DESCRIPTION)

            else:
                msg = message_templates.NEW_GAME_PLAYERS_QTY_ERROR_MESSAGE.format(
                    max_players=misc.MAX_PLAYERS,
                    current_players_qty=value
                )

        except ValueError:
            msg = message_templates.ONLY_DIGITS

    state_ui_data = state_instances.STATE_DEFINITIONS[current_state]

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )


def new_game_description_handler(ctx: RequestContext):

    command = ctx.message.text.strip().lower()
    msg = None

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return

    ctx.session.set_data(misc.GAME_INFO_KEY, command)
    current_state = ctx.session.go_forward(states.NEW_GAME_CREATED)

    state_ui_data = state_instances.STATE_DEFINITIONS[current_state]

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )


def new_game_confirmation_handler(ctx: RequestContext):
    max_players_qty = ctx.session.get_data(misc.MAX_PLAYERS_KEY)
    game_description = ctx.session.get_data(misc.GAME_INFO_KEY)
    command = ctx.message.text.strip().lower()
    current_state = ctx.session.get_state()
    msg = None

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return

    elif command == buttons.CONFIRM_BUTTON.lower():
        tg_username = ctx.message.from_user.username
        tg_first_name = ctx.message.from_user.first_name
        creator_username = tg_username or tg_first_name

        response = ctx.game_service.create_new_game(
            creator_id=ctx.message.from_user.id,
            game_description=game_description,
            creator_username=creator_username,
            max_players_qty=max_players_qty
        )

        msg = response.message
        ctx.session.clear_state()
        current_state = ctx.session.get_state()

    else:
        msg = states.NOT_VALID_INPUT

    state_ui_data = state_instances.STATE_DEFINITIONS[current_state]

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )


def join_game_handler(ctx: RequestContext):
    command = ctx.message.text.strip()
    msg = None

    if command.lower() == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return

    ctx.session.set_data(misc.GAME_NAME_KEY, command)
    current_state = ctx.session.go_forward(states.JOIN_GAME_CHECK)

    state_ui_data = state_instances.STATE_DEFINITIONS[current_state]

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )


def join_game_check_handler(ctx: RequestContext):
    command = ctx.message.text.strip()

    if command.lower() == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return

    # ctx.session.set_data(misc.GAME_PASSWORD_KEY, command)
    # msg = f"game joined with name: {ctx.session.get_data(misc.GAME_NAME_KEY)}, passcode: {ctx.session.get_data(misc.GAME_PASSWORD_KEY)}"

    game_name = ctx.session.get_data(misc.GAME_NAME_KEY)
    game_password = command
    # game_password = ctx.session.get_data(misc.GAME_PASSWORD_KEY)
    player_name = ctx.message.from_user.first_name or "N/A" + ctx.message.from_user.last_name or "N/A"
    player_id = ctx.message.from_user.id

    response = ctx.game_service.join_game(
        game_name=game_name,
        game_passcode=game_password,
        player_name=player_name,
        player_telegram_id=player_id,
    )

    msg = response.message
    ctx.session.clear_state()
    current_state = ctx.session.get_state()

    state_ui_data = state_instances.STATE_DEFINITIONS[current_state]

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )
