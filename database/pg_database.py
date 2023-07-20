from uuid import uuid4
from psycopg2 import pool


class PGDatabase:
    
    def __init__(self, config):
        self.__host = config['host']
        self.__port = config['port']
        self.__database = config['database']
        self.__user = config['user']
        self.__password = config['password']
        self.__pool: pool.ThreadedConnectionPool = None

    def connect(self):
        try:
            self.__pool = pool.ThreadedConnectionPool(
                host=self.__host,
                port=self.__port,
                database=self.__database,
                user=self.__user,
                password=self.__password,
                minconn=1,
                maxconn=5
            )
            print("Conectado a la base de datos!")
        except pool.PoolError as e:
            print(f"Error de conexión a la base de datos: {e}")

    def get_connection(self, key='sistema-bodega'):
        print('Nueva conexión')
        return self.__pool.getconn(key=key)

    def release_connection(self, key='sistema-bodega'):
        conn = self.__pool.getconn(key=key)
        if conn is not None and not conn.closed:
            self.__pool.putconn(conn, key=key)
            print(f"Conexión con clave {key} liberada")

    def commit(self, conn):
        conn.commit()
        print("Commit realizado a la base de datos")

    def rollback(self, conn):
        conn.rollback()
        print("Rollback realizado a la base de datos")

    def execute_query(self, *args, key='sistema-bodega'):
        conn = self.__pool.getconn(key=key)
        try:
            result = self.transaction_query(*args, conn=conn)
            conn.commit()
            print('Se ha realizado correctamente')
            return result
        except pool.PoolError as e:
            conn.rollback()
            print(f"Error al ejecutar consulta SQL: {e}")
        finally:
            self.__pool.putconn(conn, key=key)

    def transaction_query(self, *args, conn=None, key='sistema-bodega'):
        if conn is None:
            conn = self.__pool.getconn(key=key)
        try:
            cur = conn.cursor()

            cur.execute(*args)
            results = cur.fetchall()

            # Creación de diccionario clave-valor (objeto) con los valores consultados a la db.
            columns = [desc[0] for desc in cur.description]
            rows = [dict(zip(columns, row)) for row in results]

            cur.close()
            return rows
        except pool.PoolError as e:
            conn.rollback()
            print(f"Error al ejecutar consulta SQL: {e}") 
            
