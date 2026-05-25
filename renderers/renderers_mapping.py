from config import states
from renderers import game_renderers, service_renderers, common_renderers


STATE_RENDERERS = {
    states.MAIN_MENU: common_renderers.welcome_game_renderer,
    states.NOT_VALID_INPUT: common_renderers.not_valid_input_renderer,
    states.MY_GAMES_MENU: game_renderers.my_games_renderer,
    states.NEW_GAME_STARTS: game_renderers.new_game_creating_renderer,
    states.NEW_GAME_CREATED: game_renderers.new_game_created_renderer,
    states.SERVICE_MENU: service_renderers.my_services_renderer,
}