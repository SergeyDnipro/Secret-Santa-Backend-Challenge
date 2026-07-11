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
    )
}