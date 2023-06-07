from database.postgre_db import CursorPG


class BodegaRepository(CursorPG):

    @classmethod
    def create(cls, id_usuario: int, nombre_bodega: str, direccion_bodega: str):
        query = """
            INSERT INTO bodega (id_bodega, id_usuario, nombre_bodega, direccion_bodega)
            VALUES (default, %s, %s, %s)
            RETURNING id_bodega, id_usuario, nombre_bodega, direccion_bodega;
        """
        return cls._query(query, (id_usuario, nombre_bodega, direccion_bodega))

    @classmethod
    def read(cls, id_bodega: int):
        query = """
            SELECT * FROM bodega 
            WHERE id_bodega = %s
        """
        return cls._query(query, (id_bodega, ))

    @classmethod
    def delete(cls, id_usuario: int):
        query = """
            DELETE FROM bodega 
            WHERE id_bodega = %s
            RETURNING id_bodega, id_usuario, nombre_bodega, direccion_bodega;
        """
        return cls._query(query, (id_usuario,))
