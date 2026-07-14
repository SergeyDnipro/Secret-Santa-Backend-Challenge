import os
import telebot
import keyboards
import queue, threading
from dotenv import load_dotenv
from core.db_driver import db
from core.context import RequestContext
from config import buttons, state_instances
from service import game, notification, export, state, permission


BASE_DIR = os.path.dirname(__file__) # project/
ENV_PATH = os.path.join(BASE_DIR, "config", ".env")

load_dotenv(ENV_PATH)

TOKEN = os.getenv("TG_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split(',')))
msg_queue = queue.Queue()
bot = telebot.TeleBot(TOKEN)


game_service = game.GameService(
    permission=permission.PermissionService(admin_ids=ADMIN_IDS)
)


def build_context(*, message, session):
    return RequestContext(
        bot=bot,
        message=message,
        session=session,
        game_service=game_service
    )


@bot.message_handler(commands=['start'])
@state.session
def start(message, session: state.UserState):
    # New user start logging
    # main_logger.info(f"Start chat with user: {message.from_user.first_name} ({message.from_user.id})")

    session.clear_state()
    current_state = session.get_state()
    ctx = build_context(message=message, session=session)

    # handlers.common_handlers.welcome_menu_handler(ctx)
    handler = state_instances.STATE_DEFINITIONS.get(current_state).handler
    handler(ctx)


@bot.message_handler(func=lambda message: True)
@state.session
def handle_message(message, session: state.UserState):

    current_state = session.get_state()
    ctx = build_context(message=message, session=session)
    handler = state_instances.STATE_DEFINITIONS.get(current_state).handler
    handler(ctx)

    # if message.text == buttons.NEW_GAME_BUTTON:
    #     response = game.create_new_game(creator_id=message.from_user.id, is_admin=user_role)
    #     bot.send_message(message.chat.id, response.message)
    #
    # elif message.text == buttons.LIST_GAMES_BUTTON:
    #     all_games = db.get_all_games()
    #     all_games = class_repr_converter(
    #         cls=Game,
    #         data=all_games,
    #         many=True
    #     )
    #     all_games_str = serialize_game_list(all_games)
    #     bot.send_message(message.chat.id, f"GAMES LIST:\n\n{all_games_str}")
    #
    # elif message.text == buttons.JOIN_GAME_BUTTON:
    #     bot.send_message(message.chat.id, f"Enter GameID for join:")
    #     bot.register_next_step_handler(message, choice_game)
    # elif message.text == buttons.LOCK_GAME_BUTTON:
    #     bot.send_message(message.chat.id, f"Enter GameID for locking: ")
    #     bot.register_next_step_handler(message, lock_game)
    # elif message.text == buttons.GET_GAME_DATA_BUTTON:
    #     bot.send_message(message.chat.id, f"Enter GameID for display game data:")
    #     bot.register_next_step_handler(message, get_game_data)
    # elif message.text == buttons.START_GAME_BUTTON:
    #     bot.send_message(message.chat.id, f"Enter GameID for start game:")
    #     bot.register_next_step_handler(message, run_game_by_name)
    # elif message.text == buttons.CLEAR_DATABASE_BUTTON:
    #     bot.send_message(message.chat.id, f"Confirm your choice", reply_markup=keyboards.clear_database_keyboard())
    #     bot.register_next_step_handler(message, clear_database)
    # elif message.text == buttons.EXPORT_GAME_BUTTON:
    #     bot.send_message(message.chat.id, f"Enter GameID for results:")
    #     bot.register_next_step_handler(message, export_results)


def choice_game(message):
    """ Handle 'join game' button """
    game = db.get_game(message.text)
    if game["status"]:
        game_name = message.text
        msg = "Enter your full name"
        bot.send_message(message.chat.id, msg)
        bot.register_next_step_handler(message, join_game, game_name)
    else:
        bot.send_message(
            message.chat.id,
            game["message"],
            reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
        )
        bot.register_next_step_handler(message, handle_message)


def join_game(message, game_name=None):
    """ Handle entering 'full name' after Joining the Game """
    game_name = game_name
    player_name = message.text
    player_telegram_id = message.chat.id
    result = db.join_game_by_name(game_name=game_name, player_name=player_name, player_telegram_id=player_telegram_id)
    bot.send_message(
        message.chat.id,
        result,
        reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
    )
    bot.register_next_step_handler(message, handle_message)


def lock_game(message):
    """ Handle 'lock game' button """
    result = db.lock_game_by_name(message.text)
    bot.send_message(
        message.chat.id,
        result,
        reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
    )
    bot.register_next_step_handler(message, handle_message)


def get_game_data(message):
    """ Handle 'game info' button """

    result = db.get_players_by_game_name(message.text)
    output_msg = serialize_game_data(result)
    bot.send_message(
        message.chat.id,
        output_msg,
        reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
    )
    bot.register_next_step_handler(message, handle_message)


def run_game_by_name(message):
    """ Handle the 'run game' button. Draw Santa's Game due to the existing players """

    game_data = db.get_players_by_game_name(message.text)
    game_result = game.draw_the_game(game_data)
    msg = db.bulk_update_game_and_players(game_result)

    for player_data in game_data["players"]:
        msg_queue.put((player_data["user_chat_id"], player_data["receiver"]))

    bot.send_message(
        message.chat.id,
        msg,
        reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
    )


def clear_database(message):
    """ Handle 'clear database' button """

    if message.text == buttons.YES_BUTTON:
        msg = db.delete_all_records()
        bot.send_message(
            message.chat.id,
            msg,
            reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
        )
    elif message.text == buttons.NO_BUTTON:
        bot.send_message(
            message.chat.id,
            "Return to the main menu",
            reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
        )
        bot.register_next_step_handler(message, handle_message)


def export_results(message):
    """ Handle 'export results' button """

    game_data = db.get_players_by_game_name(message.text)

    threading.Thread(
        target=export.export_xls_worker,
        args=(bot, message.chat.id, game_data),
        daemon=True
    ).start()

    bot.send_message(
        message.chat.id,
        "Results ready to use",
        reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
    )


if __name__ == '__main__':

    threading.Thread(
        target=notification.send_notification_worker,
        args=(bot, msg_queue),
        daemon=True
    ).start()

    bot.infinity_polling()


#TODO: Logger configuration