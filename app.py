import types
import os
import telebot
import keyboards
import queue, threading
from dotenv import load_dotenv
from db_driver import db
from config import buttons, misc
from tools import serialize_game_list, serialize_game
from service import game_service, notification_service, export_result_service


BASE_DIR = os.path.dirname(__file__) # project/
ENV_PATH = os.path.join(BASE_DIR, "config", ".env")

load_dotenv(ENV_PATH)

TOKEN = os.getenv("TG_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split(',')))
msg_queue = queue.Queue()
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    # New user start logging
    # main_logger.info(f"Start chat with user: {message.from_user.first_name} ({message.from_user.id})")

    bot.send_message(
        message.chat.id,
        "Welcome to SecretSanta game",
        reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == buttons.NEW_GAME_BUTTON:
        new_game_str = db.new_game(game_name=misc.BASE_GAME_NAME)
        bot.send_message(message.chat.id, f"New game created: {new_game_str}")
    elif message.text == buttons.LIST_GAMES_BUTTON:
        all_games = db.get_all_games()
        all_games_str = serialize_game_list(all_games)
        bot.send_message(message.chat.id, f"GAMES LIST:\n\n{all_games_str}")
    elif message.text == buttons.JOIN_GAME_BUTTON:
        bot.send_message(message.chat.id, f"Enter GameID for join:")
        bot.register_next_step_handler(message, choice_game)
    elif message.text == buttons.LOCK_GAME_BUTTON:
        bot.send_message(message.chat.id, f"Enter GameID for locking: ")
        bot.register_next_step_handler(message, lock_game)
    elif message.text == buttons.GET_GAME_DATA_BUTTON:
        bot.send_message(message.chat.id, f"Enter GameID for display game data:")
        bot.register_next_step_handler(message, get_game_data)
    elif message.text == buttons.START_GAME_BUTTON:
        bot.send_message(message.chat.id, f"Enter GameID for start game:")
        bot.register_next_step_handler(message, run_game_by_name)
    elif message.text == buttons.CLEAR_DATABASE_BUTTON:
        bot.send_message(message.chat.id, f"Confirm your choice", reply_markup=keyboards.clear_database_keyboard())
        bot.register_next_step_handler(message, clear_database)
    elif message.text == buttons.EXPORT_GAME_BUTTON:
        bot.send_message(message.chat.id, f"Enter GameID for results:")
        bot.register_next_step_handler(message, export_results)


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
    """ Handle entering 'full name' after Joining Game """
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
    output_msg = serialize_game(result)
    bot.send_message(
        message.chat.id,
        output_msg,
        reply_markup=keyboards.get_main_interface_keyboard(message=message, ids=ADMIN_IDS)
    )
    bot.register_next_step_handler(message, handle_message)


def run_game_by_name(message):
    """ Handle 'run game' button. Draw Santa's Game due to the existing players """

    game_data = db.get_players_by_game_name(message.text)
    game_result = game_service.draw_the_game(game_data)
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
        target=export_result_service.export_xls_worker,
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
        target=notification_service.send_notification_worker,
        args=(bot, msg_queue),
        daemon=True
    ).start()

    bot.infinity_polling()