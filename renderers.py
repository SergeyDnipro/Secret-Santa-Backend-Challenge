import keyboards
from config import states, misc


def welcome_game_renderer(ctx):
    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        f"Welcome to SecretSanta game, {ctx.message.from_user.first_name}",
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )


def my_games_renderer(ctx):
    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        f"In this menu you can create, view and run games",
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )


def my_services_renderer(ctx):
    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        f"In this menu you can create, view and run services",
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )


def new_game_creating_renderer(ctx):
    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        f"Enter max players quantity (default {misc.MAX_PLAYERS})",
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )


def not_valid_input_renderer(ctx):
    state = ctx.session.get_state()
    ctx.bot.send_message(
        ctx.message.chat.id,
        "You must choose an option on the following keyboard panel",
        reply_markup=keyboards.STATE_KEYBOARDS.get(state)(ctx)
    )


STATE_RENDERERS = {
    states.MAIN_MENU: welcome_game_renderer,
    states.MY_GAMES_MENU: my_games_renderer,
    states.NOT_VALID_INPUT: not_valid_input_renderer,
    states.SERVICE_MENU: my_services_renderer,
    states.NEW_GAME: new_game_creating_renderer,
}