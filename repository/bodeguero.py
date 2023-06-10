from database.cursor_pg import CursorPG


class BodegueroRepository(CursorPG):

    @classmethod
    def create(cls, id_usuario: int, nombre: str, apellido_p: str, apellido_m: str, rol: str, conn=None):
        query = """
            INSERT INTO bodeguero (id_usuario, nombre, apellido_p, apellido_m, rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_usuario, nombre, apellido_m, rol;
        """
        return cls._query(query, (id_usuario, nombre, apellido_p, apellido_m, rol), conn=conn)

    @classmethod
    def read(cls, id_usuario: int, conn=None):
        query = """
            SELECT * FROM bodeguero 
            WHERE id_usuario = %s
        """
        return cls._query(query, (id_usuario,), conn=conn)

    @classmethod
    def delete(cls, id_usuario: int, conn=None):
        query = """
            DELETE FROM bodeguero 
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return cls._query(query, (id_usuario,), conn=conn)
