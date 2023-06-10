from uuid import uuid4

from database.pg_database import PsycoPG2Database
from config.database import POSTGRE_DATABASE_CONFIG


class CursorPG:
    _pool = PsycoPG2Database(POSTGRE_DATABASE_CONFIG)
    _pool.connect()

    @classmethod
    def open_transaction(cls, key='sistema-bodegas'):
        return cls._pool.get_connection(key=key)

    @classmethod
    def release(cls, key='sistema-bodegas'):
        cls._pool.release_connection(key=key)

    @classmethod
    def _execute_query(cls, *args):
        key = str(uuid4())
        return cls._pool.execute_query(*args, key=key)

    @classmethod
    def _transaction_query(cls, *args, conn=None, key='sistema-bodega'):
        return cls._pool.transaction_query(*args, conn=conn, key=key)

    @classmethod
    def _query(cls, *args, conn=None):
        if conn is None:
            return cls._execute_query(*args)
        return cls._transaction_query(*args, conn=conn)

    @classmethod
    def commit(cls, conn):
        cls._pool.commit(conn)

    @classmethod
    def rollback(cls, conn):
        cls._pool.rollback(conn)


