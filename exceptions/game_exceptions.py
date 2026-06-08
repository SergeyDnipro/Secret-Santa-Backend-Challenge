class GameAppException(Exception):
    default_error = "Unknown error"

    def __init__(self):
        super().__init__(self.default_error)


class GameFullError(GameAppException):
    default_error = "Game already full of players"


class PlayerAlreadyJoinedError(GameAppException):
    default_error = "You can't join a game twice"


class GameLockedError(GameAppException):
    default_error = "Game already locked for accepting new players"


class GameNotFoundError(Exception):
    default_error = "Game not found for ID/passcode"
