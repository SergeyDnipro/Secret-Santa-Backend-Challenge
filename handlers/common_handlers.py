import renderers
from config import states, buttons
from core.context import RequestContext


def welcome_menu_handler(ctx: RequestContext):
    keyboard_state = ctx.session.get_state()
    renderer = renderers.STATE_RENDERERS.get(keyboard_state)
    renderer(ctx)


def main_page_handler(ctx: RequestContext):
    command = ctx.message.text.strip().lower()

    if command == buttons.GAME_MENU_BUTTON.lower():
        new_state = ctx.session.go_forward(states.MY_GAMES_MENU)
    elif command == buttons.SERVICE_MENU.lower():
        new_state = ctx.session.go_forward(states.SERVICE_MENU)
    else:
        new_state = states.NOT_VALID_INPUT

    renderer = renderers.STATE_RENDERERS.get(new_state)
    renderer(ctx)


def fallback_handler(ctx: RequestContext):
    previous_state = ctx.session.go_back()
    renderer = renderers.STATE_RENDERERS.get(previous_state)
    renderer(ctx)
