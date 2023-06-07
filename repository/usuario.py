from database.postgre_db import CursorPG


class UsuarioRepository(CursorPG):

    @classmethod
    def create(cls, nombre_usuario, email, password):
        query = """
            INSERT INTO usuario (id_usuario, nombre_usuario, email, password)
            VALUES (default, %s, %s, %s)
            RETURNING id_usuario, email;
        """
        return cls._query(query, (nombre_usuario, email, password,))

    @classmethod
    def read(cls, id_usuario: int):
        query = """
            SELECT * FROM usuario 
            WHERE id_usuario = %s
        """
        return cls._query(query, (id_usuario,))

    @classmethod
    def readByEmail(cls, email: str):
        query = """
            SELECT * FROM usuario 
            WHERE email = %s
        """
        return cls._query(query, (email, ))

    @classmethod
    def updateEmail(cls, id_usuario: int, oldpassword: str, newpassword: str):
        query = """
            UPDATE usuario 
            SET password = %s
            WHERE id_usuario = %s and oldpassword = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return cls._query(query, (newpassword, id_usuario, oldpassword, ))

    @classmethod
    def delete(cls, id_usuario: int):
        query = """
            DELETE FROM usuario 
            WHERE id_usuario = %s
            RETURNING id_usuario, nombre_usuario, email;
        """
        return cls._query(query, (id_usuario,))
