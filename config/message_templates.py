# WELCOME GAME TEMPLATE
WELCOME_MESSAGE = "Welcome to SecretSanta Game {username}!"

# MAIN MENU TEMPLATES
GAME_MENU_MESSAGE = "You can start, join or run game"
SERVICE_MENU_MESSAGE = "You view status, maintain or delete games"


# GAME INFO
GET_GAME_ID_MESSAGE = "Enter game ID: "


# CREATING GAME
NEW_GAME_MESSAGE = "Enter max players quantity, from 3 to {max_players} (default: {default_max_players})"
NEW_GAME_DESCRIPTION_MESSAGE = "Enter additional info about the game: "
NEW_GAME_PLAYERS_QTY_ERROR_MESSAGE = "Players quantity must be between 3 and {max_players}. You entered: {current_players_qty}"
NEW_GAME_CONFIRMATION_MESSAGE = "Create creating new game"


# JOINING GAME
JOIN_GAME_ID_MESSAGE = "Enter game name: "
JOIN_GAME_PASSCODE_MESSAGE = "Enter game password: "
JOIN_GAME_SUCCESS_MESSAGE = "You've joined game: {game_name} successfully!".format


# ERRORS MESSAGES
ONLY_DIGITS = "Only digits allowed"
GAME_DEFAULT_ERROR = "Unknown error"
GAME_FULL_ERROR = "Game already full of players"
PLAYER_ALREADY_JOIN_ERROR = "You can't join a game twice"
GAME_LOCKED_ERROR = "Game already locked for accepting new players"
GAME_NOT_FOUND_ERROR = "Game not found for ID/passcode"
NOT_VALID_INPUT = "Not valid input data, try again"