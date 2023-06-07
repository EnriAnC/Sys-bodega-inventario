from psycopg2 import pool


class Database:
    def __init__(self, config):
        self.__host = config['host']
        self.__port = config['port']
        self.__database = config['database']
        self.__user = config['user']
        self.__password = config['password']
        self.__pool = None
        self.conn = None

    def connect(self):
        try:
            self.__pool = pool.ThreadedConnectionPool(
                host=self.__host,
                port=self.__port,
                database=self.__database,
                user=self.__user,
                password=self.__password,
                minconn=1,
                maxconn=10
            )
            print("Conectado a la base de datos!")
        except pool.PoolError as e:
            print(f"Error de conexión a la base de datos: {e}")

    def get_connection(self):
        if self.conn is not None:
            print('Reutilizando conexión')
            return self.conn
        self.conn = self.__pool.getconn(key='sistema-bodega')
        print('Nueva conexión')
        return self.conn

    def release_connection(self):
        if self.conn is not None:
            self.__pool.putconn(self.conn, key='sistema-bodega')
            self.conn = None
            print("Conexión liberada")

    def commit(self):
        conn = self.get_connection()
        try:
            conn.commit()
            print("Commit realizado a la base de datos")
        except pool.PoolError as e:
            conn.rollback()
            print(f"Error al hacer commit: {e}")
        finally:
            self.release_connection()

    def rollback(self):
        conn = self.get_connection()
        try:
            conn.rollback()
            print("Rollback realizado a la base de datos")
        finally:
            self.release_connection()

    def execute_query(self, *args):
        try:
            result = self.transaction_query(*args)
            self.commit()
            return result
        except pool.PoolError as e:
            self.rollback()
            print(f"Error al ejecutar consulta SQL: {e}")

    def transaction_query(self, *args):
        conn = self.get_connection()
        try:
            cur = conn.cursor()

            cur.execute(*args)
            results = cur.fetchall()

            # Creación de diccionario clave-valor (objeto)
            # con los valores consultados a la base
            columns = [desc[0] for desc in cur.description]
            rows = [dict(zip(columns, row)) for row in results]

            cur.close()
            return rows
        except pool.PoolError as e:
            conn.rollback()
            print(f"Error al ejecutar consulta SQL: {e}")
