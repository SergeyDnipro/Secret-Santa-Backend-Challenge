from handlers import service_handlers, game_handlers, common_handlers
from config import states


handlers_mapping = {
    states.MAIN_MENU: common_handlers.main_page_handler,
    states.MY_GAMES_MENU: game_handlers.my_games_menu_handler,
    states.SERVICE_MENU: game_handlers.my_services_menu_handler,
    states.NEW_GAME: game_handlers.new_game_handler,
}