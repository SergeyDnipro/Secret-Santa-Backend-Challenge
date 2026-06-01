import sqlite3
from functools import wraps


def transactional(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            with sqlite3.connect(self.database_name) as db_conn:
                db_conn.execute("PRAGMA foreign_keys = ON;")
                db_conn.row_factory = sqlite3.Row
                kwargs["conn"] = db_conn
                return func(self, *args, **kwargs)
        except sqlite3.DatabaseError as e:
            # logger
            raise

    return wrapper
