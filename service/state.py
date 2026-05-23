from core.db_redis import get_redis
from config import states
from functools import wraps
from typing import Callable


class UserState:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_state_store = get_redis()


    @property
    def state_key(self):
        return f"bot:user:{self.user_id}:state"


    @property
    def history_key(self):
        return f"bot:user:{self.user_id}:history"


    def get_state(self):
        return self.user_state_store.get(self.state_key) or states.MAIN_MENU


    def set_state(self, state):
        self.user_state_store.set(self.state_key, state)


    def go_forward(self, new_state):
        current_state = self.get_state()
        self.user_state_store.rpush(self.history_key, current_state)
        self.set_state(new_state)
        return new_state


    def go_back(self):
        previous_state = self.user_state_store.rpop(self.history_key) or states.MAIN_MENU
        self.set_state(previous_state)
        return previous_state


    def clear_state(self):
        self.user_state_store.delete(self.state_key)
        self.user_state_store.delete(self.history_key)


    def reset_workflow(self, state=states.MAIN_MENU):
        self.user_state_store.delete(self.history_key)
        self.set_state(state)


""" Get UserState session """
def session(handler: Callable) -> Callable:
    @wraps(handler)
    def wrapper(message):
        user_session = UserState(message.from_user.id)
        return handler(message, user_session)
    return wrapper
