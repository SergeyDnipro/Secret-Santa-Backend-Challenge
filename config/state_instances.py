from config import message_builder, states
from handlers import common_handlers, game_handlers, service_handlers
from keyboards import common_keyboards, game_keyboards, service_keyboards
from models import StateDefinition


STATE_DEFINITIONS = {
    states.START_APP: StateDefinition(
        handler=common_handlers.welcome_menu_handler,
        keyboard=common_keyboards.main_menu_keyboard,
        default_message=message_builder.welcome_message
    ),

    states.GAMES_MENU: StateDefinition(
        handler=game_handlers.my_games_menu_handler,
        keyboard=game_keyboards.my_games_keyboard,
        default_message=message_builder.game_menu_message
    ),

    states.SERVICE_MENU: StateDefinition(
        handler=service_handlers.my_services_menu_handler,
        keyboard=service_keyboards.my_service_keyboard,
        default_message=message_builder.service_menu_message
    ),

    states.GET_GAME_DATA: StateDefinition(
        handler=service_handlers.get_game_data_handler,
        keyboard=common_keyboards.backward_keyboard,
        default_message=message_builder.get_game_data_id_message
    ),

    states.NEW_GAME_STARTS: StateDefinition(
        handler=game_handlers.new_game_creating_handler,
        keyboard=game_keyboards.new_game_creating_keyboard,
        default_message=message_builder.new_game_message
    ),

    states.NEW_GAME_DESCRIPTION: StateDefinition(
        handler=game_handlers.new_game_description_handler,
        keyboard=common_keyboards.backward_keyboard,
        default_message=message_builder.new_game_description_message
    ),

    states.NEW_GAME_CREATED: StateDefinition(
        handler=game_handlers.new_game_confirmation_handler,
        keyboard=game_keyboards.new_game_confirmation_keyboard,
        default_message=message_builder.new_game_confirmation_message
    ),

    states.JOIN_GAME_START: StateDefinition(
        handler=game_handlers.join_game_handler,
        keyboard=common_keyboards.backward_keyboard,
        default_message=message_builder.join_game_start_message
    ),

    states.JOIN_GAME_CHECK: StateDefinition(
        handler=game_handlers.join_game_check_handler,
        keyboard=common_keyboards.backward_keyboard,
        default_message=message_builder.join_game_passcode_message
    )
}