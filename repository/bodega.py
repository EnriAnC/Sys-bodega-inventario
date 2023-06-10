from database.cursor_pg import CursorPG


class BodegaRepository(CursorPG):

    @classmethod
    def create(cls, id_usuario: int, nombre_bodega: str, direccion_bodega: str, conn=None):
        query = """
            INSERT INTO bodega (id_bodega, id_usuario, nombre_bodega, direccion_bodega)
            VALUES (default, %s, %s, %s)
            RETURNING id_bodega, id_usuario, nombre_bodega, direccion_bodega;
        """
        return cls._query(query, (id_usuario, nombre_bodega, direccion_bodega), conn=conn)

    @classmethod
    def read(cls, id_bodega: int, conn=None):
        query = """
            SELECT * FROM bodega 
            WHERE id_bodega = %s
        """
        return cls._query(query, (id_bodega, ), conn=conn)

    @classmethod
    def readNRows(cls, n = 10, conn=None):
        query = """
            SELECT * FROM bodega
            FETCH FIRST %s ROWS ONLY
        """
        return cls._query(query, (n,), conn=conn)

    @classmethod
    def getByUsuarioId(cls, id_usuario, conn=None):
        query = """
            SELECT * FROM bodega 
            WHERE id_usuario = %s
        """
        return cls._query(query, (id_usuario,), conn=conn)

    @classmethod
    def delete(cls, id_usuario: int, conn=None):
        query = """
            DELETE FROM bodega 
            WHERE id_bodega = %s
            RETURNING id_bodega, id_usuario, nombre_bodega, direccion_bodega;
        """
        return cls._query(query, (id_usuario,), conn=conn)
