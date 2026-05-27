from handlers import service_handlers, game_handlers, common_handlers
from config import states


handlers_mapping = {
    states.MAIN_MENU: common_handlers.main_page_handler,
    states.MY_GAMES_MENU: game_handlers.my_games_menu_handler,
    states.NEW_GAME_STARTS: game_handlers.new_game_creating_handler,
    states.NEW_GAME_CREATED: game_handlers.new_game_confirmation_handler,
    states.SERVICE_MENU: service_handlers.my_services_menu_handler,
    states.GET_GAME_DATA: service_handlers.get_game_data_handler,
}
