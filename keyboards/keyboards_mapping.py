from config import states, buttons
from keyboards import game_keyboards, service_keyboards, common_keyboards


STATE_KEYBOARDS = {
    states.MAIN_MENU: common_keyboards.main_menu_keyboard,
    states.MY_GAMES_MENU: game_keyboards.my_games_keyboard,
    states.NEW_GAME_STARTS: game_keyboards.new_game_creating_keyboard,
    states.NEW_GAME_CREATED: game_keyboards.new_game_confirmation_keyboard,
    states.SERVICE_MENU: service_keyboards.my_service_keyboard,
}