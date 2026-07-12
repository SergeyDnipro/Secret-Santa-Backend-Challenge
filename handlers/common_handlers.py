import renderers_storage
import renderers
from config import states, buttons, state_instances, message_templates
from core.context import RequestContext


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

    state_ui_data = state_instances.STATE_DEFINITIONS.get(current_state)

    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data,
        msg=msg
    )



def main_page_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()

    if command == buttons.GAME_MENU_BUTTON.lower():
        new_state = ctx.session.go_forward(states.GAMES_MENU)
        print(ctx.session.get_states())
    elif command == buttons.SERVICE_MENU.lower():
        new_state = ctx.session.go_forward(states.SERVICE_MENU)
    else:
        new_state = states.NOT_VALID_INPUT

    renderer = renderers_storage.STATE_RENDERERS.get(new_state)
    renderer(ctx)


def backward_handler(ctx: RequestContext):
    previous_state = ctx.session.go_back()
    state_ui_data = state_instances.STATE_DEFINITIONS.get(previous_state)
    renderers.common_renderer(
        ctx=ctx,
        state_data=state_ui_data
    )
    # new_handler = handlers_mapping.get(previous_state)
    # print(ctx.session.get_states())
    # new_handler(ctx)
    # renderer = renderers_storage.STATE_RENDERERS.get(previous_state)
    # renderer(ctx)
