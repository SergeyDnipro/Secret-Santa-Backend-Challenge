from config import message_builder, states
from handlers import common_handlers
from keyboards import common_keyboards
from models import StateDefinition


STATE_DEFINITIONS = {
    states.START_APP: StateDefinition(
        handler=common_handlers.welcome_menu_handler,
        keyboard=common_keyboards.main_menu_keyboard,
        default_message=message_builder.welcome_message
    )
}