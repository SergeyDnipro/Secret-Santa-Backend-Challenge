import renderers
from config import states, buttons, state_instances, message_templates
from core.context import RequestContext


def get_user_name(ctx: RequestContext):
    pass


def welcome_menu_handler(ctx: RequestContext):

    msg = None
    current_state = ctx.session.get_state()
    command = ctx.message.text.strip().lower()

    if command == buttons.GAME_MENU_BUTTON.lower():
        current_state = ctx.session.go_forward(states.GAMES_MENU)
    elif command == buttons.SERVICE_MENU.lower():
        current_state = ctx.session.go_forward(states.SERVICE_MENU)
    elif command == buttons.BACK_BUTTON.lower() or command == "/start":
        pass
    else:
        msg = message_templates.NOT_VALID_INPUT

    state_ui_data = state_instances.STATE_DEFINITIONS[current_state]

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )


def backward_handler(ctx: RequestContext):
    previous_state = ctx.session.go_back()
    state_ui_data = state_instances.STATE_DEFINITIONS[previous_state]
    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data
    )
