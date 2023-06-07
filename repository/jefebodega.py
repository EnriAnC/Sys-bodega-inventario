from database.postgre_db import CursorPG


class JefeBodegaRepository(CursorPG):

    @classmethod
    def create(cls, id_usuario: int, nombre: str, apellido_p: str, apellido_m: str, rol: str):
        query = """
            INSERT INTO jefebodega (id_usuario, nombre, apellido_p, apellido_m, rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_usuario, nombre, apellido_m, rol;
        """
        return cls._query(query, (id_usuario, nombre, apellido_p, apellido_m, rol))

    @classmethod
    def read(cls, id_usuario: int):
        query = """
            SELECT * FROM jefebodega 
            WHERE id_usuario = %s
        """
        return cls._query(query, (id_usuario,))

    @classmethod
    def update_fecha_contrato(cls, id_usuario: int, fecha_contrato: str):
        query = """
            UPDATE jefebodega 
            SET fecha_contrato = %s
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre_usuario, email, fecha_contrato;
        """
        return cls._query(query, (fecha_contrato, id_usuario))

    @classmethod
    def delete(cls, id_usuario: int):
        query = """
            DELETE FROM jefebodega 
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return cls._query(query, (id_usuario,))
