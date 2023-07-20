from uuid import uuid4

from database.pg_database import PGDatabase
        
class CursorPG:
    
    def __init__(self, postgreDatabase: PGDatabase) -> None:
        self.postgreDatabase = postgreDatabase

    def open_transaction(self, key='sistema-bodegas'):
        return self.postgreDatabase.get_connection(key=key)

    def release(self, key='sistema-bodegas'):
        self.postgreDatabase.release_connection(key=key)

    def _execute_query(self, *args):
        key = str(uuid4())
        return self.postgreDatabase.execute_query(*args, key=key)

    def _transaction_query(self, *args, conn=None, key='sistema-bodega'):
        return self.postgreDatabase.transaction_query(*args, conn=conn, key=key)

    def query(self, *args, conn=None):
        if conn is None:
            print('Ejecutando consulta...')
            return self._execute_query(*args)
        print('Ejecutando transacción...')
        return self._transaction_query(*args, conn=conn)

    def commit(self, conn):
        self.postgreDatabase.commit(conn)

    def rollback(self, conn):
        self.postgreDatabase.rollback(conn)



        


