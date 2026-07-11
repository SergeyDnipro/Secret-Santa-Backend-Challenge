import renderers
from config import states, buttons, message_templates
from core.context import RequestContext


def welcome_menu_handler(ctx: RequestContext):
    ctx.session.set_state(states.START_APP)
    ctx.session.go_forward(states.MAIN_MENU)
    keyboard_state = ctx.session.get_state()
    print(ctx.session.get_states())
    username = ctx.message.from_user.username or ctx.message.from_user.first_name
    msg = message_templates.WELCOME_MESSAGE(username=username)
    renderer = renderers.STATE_RENDERERS.get(keyboard_state)
    renderer(ctx, msg=msg)


def main_page_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()

    if command == buttons.GAME_MENU_BUTTON.lower():
        new_state = ctx.session.go_forward(states.MY_GAMES_MENU)
        print(ctx.session.get_states())
    elif command == buttons.SERVICE_MENU.lower():
        new_state = ctx.session.go_forward(states.SERVICE_MENU)
    else:
        new_state = states.NOT_VALID_INPUT

    renderer = renderers.STATE_RENDERERS.get(new_state)
    renderer(ctx)


# def backward_handler(ctx: RequestContext):
#     previous_state = ctx.session.go_back()
#     new_handler = handlers_mapping.get(previous_state, welcome_menu_handler)
#     new_handler(ctx)
#     # renderer = renderers.STATE_RENDERERS.get(previous_state)
#     # renderer(ctx)
