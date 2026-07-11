import renderers
from core.context import RequestContext
from handlers import common_handlers
from config import states, buttons, misc
from service import state


def my_services_menu_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()
    response_msg = None

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return

    elif command == buttons.LIST_GAMES_BUTTON.lower():
        response = ctx.game_service.get_user_games(
            creator_id=ctx.message.from_user.id
        )
        response_msg = response.message
        current_state = ctx.session.get_state()

    elif command == buttons.GET_GAME_DATA_BUTTON.lower():
        current_state = ctx.session.go_forward(states.GET_GAME_DATA)
        response_msg = f"Enter game ID:"
    else:
        current_state = states.NOT_VALID_INPUT

    renderer = renderers.STATE_RENDERERS.get(current_state)
    renderer(ctx, msg=response_msg)


def get_game_data_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()
    response_msg = None

    if command == buttons.BACK_BUTTON.lower():
        common_handlers.backward_handler(ctx)
        return

    response = ctx.game_service.get_game_data(
        creator_id=ctx.message.from_user.id,
        game_name=ctx.message.text.strip().lower(),
    )
    response_msg = response.message

    if response.success:
        ctx.session.go_back()

    current_state = ctx.session.get_state()
    renderer = renderers.STATE_RENDERERS.get(current_state)
    renderer(ctx, msg=response_msg)