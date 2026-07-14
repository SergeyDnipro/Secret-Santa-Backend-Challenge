import renderers
from core.context import RequestContext
from handlers import common_handlers
from config import states, buttons, misc, state_instances
from service import state


def my_services_menu_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()
    current_state = ctx.session.get_state()
    msg = None

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return

    elif command == buttons.LIST_GAMES_BUTTON.lower():
        response = ctx.game_service.get_user_games(
            creator_id=ctx.message.from_user.id
        )
        msg = response.message

    elif command == buttons.GET_GAME_DATA_BUTTON.lower():
        current_state = ctx.session.go_forward(states.GET_GAME_DATA)

    else:
        msg = states.NOT_VALID_INPUT

    state_ui_data = state_instances.STATE_DEFINITIONS[current_state]

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )


def get_game_data_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()
    msg = None

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return

    response = ctx.game_service.get_game_data(
        creator_id=ctx.message.from_user.id,
        game_name=ctx.message.text.strip().lower(),
    )
    msg = response.message

    if response.success:
        ctx.session.go_back()

    current_state = ctx.session.get_state()

    state_ui_data = state_instances.STATE_DEFINITIONS[current_state]

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )
