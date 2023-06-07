from database.database import Database
from config.database import POSTGRE_DATABASE_CONFIG


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class CursorPG(metaclass=SingletonMeta):
    _pool = Database(POSTGRE_DATABASE_CONFIG)
    _pool.connect()

    @classmethod
    def open_transaction(cls):
        cls._pool.get_connection()

    @classmethod
    def _execute_query(cls, *args):
        return cls._pool.execute_query(*args)

    @classmethod
    def _transaction_query(cls, *args):
        return cls._pool.transaction_query(*args)

    @classmethod
    def _query(cls, *args):
        if cls._pool.conn is None:
            return cls._execute_query(*args)
        return cls._transaction_query(*args)

    @classmethod
    def commit(cls):
        cls._pool.commit()

    @classmethod
    def rollback(cls):
        cls._pool.rollback()
