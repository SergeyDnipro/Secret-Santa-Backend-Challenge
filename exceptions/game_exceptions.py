from config import message_templates


class GameAppException(Exception):
    default_error = message_templates.GAME_DEFAULT_ERROR

    def __init__(self):
        super().__init__(self.default_error)


class GameFullError(GameAppException):
    default_error = message_templates.GAME_FULL_ERROR


class PlayerAlreadyJoinedError(GameAppException):
    default_error = message_templates.PLAYER_ALREADY_JOIN_ERROR


class GameLockedError(GameAppException):
    default_error = message_templates.GAME_LOCKED_ERROR


class GameNotFoundError(GameAppException):
    default_error = message_templates.GAME_NOT_FOUND_ERROR
